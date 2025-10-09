from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from keyboards.sd_k import (
    nutrition_home_kb, add_meal_kb, add_another_dish_kb, 
    nutrition_chart_kb, nutrition_menu_kb, set_goals_kb,
    dishes_list_kb, meal_summary_kb
)
from config import SD_MESSAGES, SD_CD
from states import STATES
from models import (
    create_meal, get_current_meal, add_dish, get_all_dishes, 
    get_dish_by_id, add_meal_item, complete_meal, set_nutrition_goal,
    get_nutrition_goal, add_nutrition_rule, add_nutrition_note,
    get_nutrition_summary_by_date
)
from datetime import datetime

async def nutrition_home(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Главное меню питания"""
    query = update.callback_query
    await query.answer()
    
    markup = nutrition_home_kb()
    text = SD_MESSAGES['nutrition_home']
    
    await query.edit_message_text(text=text, reply_markup=markup)
    return STATES['nutrition_home']

async def add_meal_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Начало добавления приёма пищи"""
    query = update.callback_query
    await query.answer()
    
    chat_id = query.from_user.id
    today = datetime.now().strftime('%Y-%m-%d')
    
    # Создаём новый приём пищи или получаем текущий
    current_meal = get_current_meal(chat_id, today)
    if not current_meal:
        meal_id = create_meal(chat_id, today)
        context.user_data['current_meal_id'] = meal_id
    else:
        context.user_data['current_meal_id'] = current_meal.id
    
    markup = add_meal_kb()
    text = SD_MESSAGES['add_meal']
    
    await query.edit_message_text(text=text, reply_markup=markup)
    return STATES['add_meal']

async def add_dish_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Начало добавления нового блюда"""
    query = update.callback_query
    await query.answer()
    
    text = SD_MESSAGES['add_dish']
    await query.edit_message_text(text=text)
    return STATES['wait_dish_name']

async def wait_dish_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка названия блюда"""
    dish_name = update.message.text
    context.user_data['dish_name'] = dish_name
    
    text = SD_MESSAGES['wait_dish_calories']
    await update.message.reply_text(text)
    return STATES['wait_dish_calories']

async def wait_dish_calories(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка калорий блюда"""
    try:
        calories = float(update.message.text)
        context.user_data['dish_calories'] = calories
        
        text = SD_MESSAGES['wait_dish_protein']
        await update.message.reply_text(text)
        return STATES['wait_dish_protein']
    except ValueError:
        await update.message.reply_text("Пожалуйста, введите число для калорий.")
        return STATES['wait_dish_calories']

async def wait_dish_protein(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка белка блюда"""
    try:
        protein = float(update.message.text)
        context.user_data['dish_protein'] = protein
        
        text = SD_MESSAGES['wait_dish_grams']
        await update.message.reply_text(text)
        return STATES['wait_dish_grams']
    except ValueError:
        await update.message.reply_text("Пожалуйста, введите число для белка.")
        return STATES['wait_dish_protein']

async def wait_dish_grams(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка граммов блюда и добавление в приём пищи"""
    try:
        grams = float(update.message.text)
        
        # Проверяем, выбрано ли блюдо из существующего списка
        if 'selected_dish_id' in context.user_data:
            dish_id = context.user_data['selected_dish_id']
            del context.user_data['selected_dish_id']
        else:
            # Добавляем новое блюдо в базу данных
            dish_id = add_dish(
                context.user_data['dish_name'],
                context.user_data['dish_calories'],
                context.user_data['dish_protein']
            )
        
        # Добавляем блюдо в приём пищи
        meal_id = context.user_data.get('current_meal_id')
        if meal_id:
            add_meal_item(meal_id, dish_id, grams)
            
            # Получаем информацию о блюде для отображения
            dish = get_dish_by_id(dish_id)
            calories_eaten = (dish.calories_per_100g * grams) / 100
            protein_eaten = (dish.protein_per_100g * grams) / 100
            
            text = f"✅ Блюдо добавлено!\n\n"
            text += f"🍽️ {dish.name}\n"
            text += f"📊 {grams}г - {calories_eaten:.1f} ккал, {protein_eaten:.1f}г белка\n\n"
            text += "Хотите добавить ещё одно блюдо?"
            
            markup = add_another_dish_kb()
            await update.message.reply_text(text, reply_markup=markup)
            return STATES['add_meal']
        else:
            await update.message.reply_text("Ошибка: приём пищи не найден.")
            return STATES['add_meal']
            
    except ValueError:
        await update.message.reply_text("Пожалуйста, введите число для граммов.")
        return STATES['wait_dish_grams']

async def find_dishes_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показ списка всех блюд"""
    query = update.callback_query
    await query.answer()
    
    dishes = get_all_dishes()
    if not dishes:
        text = "В базе данных пока нет блюд. Добавьте первое блюдо!"
        markup = add_meal_kb()
        await query.edit_message_text(text=text, reply_markup=markup)
        return STATES['add_meal']
    
    text = SD_MESSAGES['find_dishes']
    markup = dishes_list_kb(dishes)
    
    await query.edit_message_text(text=text, reply_markup=markup)
    return STATES['find_dishes']

async def select_dish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Выбор блюда из списка"""
    query = update.callback_query
    await query.answer()
    
    dish_id = int(query.data.split('_')[-1])
    context.user_data['selected_dish_id'] = dish_id
    
    dish = get_dish_by_id(dish_id)
    text = f"Выбрано блюдо: {dish.name}\n\n{SD_MESSAGES['wait_dish_grams']}"
    
    await query.edit_message_text(text=text)
    return STATES['wait_dish_grams']

async def complete_meal_final(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Завершение приёма пищи"""
    query = update.callback_query
    await query.answer()
    
    meal_id = context.user_data.get('current_meal_id')
    if meal_id:
        # Получаем информацию о приёме пищи перед завершением
        from models import Meal
        from sqlalchemy.orm import Session
        from models import engine
        
        with Session(engine) as session:
            meal = session.query(Meal).filter(Meal.id == meal_id).first()
            if meal:
                total_calories = meal.total_calories
                total_protein = meal.total_protein
                
                # Завершаем приём пищи
                complete_meal(meal_id)
                
                # Получаем цели пользователя
                goal = get_nutrition_goal(query.from_user.id)
                
                text = f"✅ Приём пищи завершён!\n\n"
                text += f"📊 Итого в приёме пищи:\n"
                text += f"🔥 {total_calories:.1f} ккал\n"
                text += f"🥩 {total_protein:.1f}г белка\n\n"
                
                if goal:
                    calories_diff = goal.daily_calories - total_calories
                    protein_diff = goal.daily_protein - total_protein
                    
                    text += f"🎯 Цели на день:\n"
                    text += f"🔥 {goal.daily_calories} ккал "
                    if calories_diff > 0:
                        text += f"(осталось {calories_diff:.1f})\n"
                    else:
                        text += f"(перебор {abs(calories_diff):.1f})\n"
                        
                    text += f"🥩 {goal.daily_protein}г белка "
                    if protein_diff > 0:
                        text += f"(осталось {protein_diff:.1f})\n"
                    else:
                        text += f"(перебор {abs(protein_diff):.1f})\n"
                else:
                    text += "💡 Установите цели по питанию для отслеживания прогресса!"
            else:
                text = "Ошибка: приём пищи не найден."
    else:
        text = "Ошибка: приём пищи не найден."
    
    markup = nutrition_home_kb()
    await query.edit_message_text(text=text, reply_markup=markup)
    return STATES['nutrition_home']

async def nutrition_chart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """График питания"""
    query = update.callback_query
    await query.answer()
    
    markup = nutrition_chart_kb()
    text = SD_MESSAGES['nutrition_chart']
    
    await query.edit_message_text(text=text, reply_markup=markup)
    return STATES['nutrition_chart']

async def nutrition_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Меню питания"""
    query = update.callback_query
    await query.answer()
    
    markup = nutrition_menu_kb()
    text = SD_MESSAGES['nutrition_menu']
    
    await query.edit_message_text(text=text, reply_markup=markup)
    return STATES['nutrition_menu']

async def add_rule_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Начало добавления правила питания"""
    query = update.callback_query
    await query.answer()
    
    text = SD_MESSAGES['add_rule']
    await query.edit_message_text(text=text)
    return STATES['wait_rule_text']

async def wait_rule_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка текста правила"""
    rule_text = update.message.text
    context.user_data['rule_text'] = rule_text
    
    from telegram import InlineKeyboardButton, InlineKeyboardMarkup
    text = SD_MESSAGES['wait_reminder_time']
    markup = InlineKeyboardMarkup([[InlineKeyboardButton(text="Пропустить", callback_data="skip_reminder")]])
    await update.message.reply_text(text, reply_markup=markup)
    return STATES['wait_reminder_time']

async def wait_reminder_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка времени напоминания"""
    reminder_time = update.message.text
    context.user_data['reminder_time'] = reminder_time
    
    text = SD_MESSAGES['wait_exceptions']
    markup = InlineKeyboardMarkup([[InlineKeyboardButton(text="Пропустить", callback_data="skip_exceptions")]])
    await update.message.reply_text(text, reply_markup=markup)
    return STATES['wait_exceptions']

async def wait_exceptions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка исключений и сохранение правила"""
    exceptions = update.message.text
    context.user_data['exceptions'] = exceptions
    
    # Сохраняем правило
    add_nutrition_rule(
        update.message.from_user.id,
        context.user_data['rule_text'],
        context.user_data.get('reminder_time'),
        exceptions
    )
    
    text = "✅ Правило питания добавлено!"
    markup = nutrition_menu_kb()
    await update.message.reply_text(text, reply_markup=markup)
    return STATES['nutrition_menu']

async def skip_reminder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Пропуск времени напоминания"""
    query = update.callback_query
    await query.answer()
    
    context.user_data['reminder_time'] = None
    
    text = SD_MESSAGES['wait_exceptions']
    markup = InlineKeyboardMarkup([[InlineKeyboardButton(text="Пропустить", callback_data="skip_exceptions")]])
    await query.edit_message_text(text=text, reply_markup=markup)
    return STATES['wait_exceptions']

async def skip_exceptions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Пропуск исключений и сохранение правила"""
    query = update.callback_query
    await query.answer()
    
    context.user_data['exceptions'] = None
    
    # Сохраняем правило
    add_nutrition_rule(
        query.from_user.id,
        context.user_data['rule_text'],
        context.user_data.get('reminder_time'),
        None
    )
    
    text = "✅ Правило питания добавлено!"
    markup = nutrition_menu_kb()
    await query.edit_message_text(text=text, reply_markup=markup)
    return STATES['nutrition_menu']

async def set_goals_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Начало установки целей"""
    query = update.callback_query
    await query.answer()
    
    markup = set_goals_kb()
    text = SD_MESSAGES['set_goals']
    
    await query.edit_message_text(text=text, reply_markup=markup)
    return STATES['set_goals']

async def set_calories_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Установка цели по калориям"""
    query = update.callback_query
    await query.answer()
    
    text = SD_MESSAGES['set_calories']
    await query.edit_message_text(text=text)
    return STATES['set_calories']

async def set_protein_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Установка цели по белку"""
    query = update.callback_query
    await query.answer()
    
    text = SD_MESSAGES['set_protein']
    await query.edit_message_text(text=text)
    return STATES['set_protein']

async def wait_calories_goal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка цели по калориям"""
    try:
        calories = float(update.message.text)
        context.user_data['calories_goal'] = calories
        
        # Проверяем, есть ли уже цель по белку
        goal = get_nutrition_goal(update.message.from_user.id)
        if goal:
            set_nutrition_goal(update.message.from_user.id, calories, goal.daily_protein)
            text = f"✅ Цель по калориям обновлена: {calories} ккал/день"
        else:
            text = f"✅ Цель по калориям установлена: {calories} ккал/день\n\nТеперь установите цель по белку."
            markup = set_goals_kb()
            await update.message.reply_text(text, reply_markup=markup)
            return STATES['set_goals']
        
        markup = nutrition_menu_kb()
        await update.message.reply_text(text, reply_markup=markup)
        return STATES['nutrition_menu']
        
    except ValueError:
        await update.message.reply_text("Пожалуйста, введите число для калорий.")
        return STATES['set_calories']

async def wait_protein_goal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка цели по белку"""
    try:
        protein = float(update.message.text)
        
        # Проверяем, есть ли уже цель по калориям
        goal = get_nutrition_goal(update.message.from_user.id)
        if goal:
            set_nutrition_goal(update.message.from_user.id, goal.daily_calories, protein)
            text = f"✅ Цель по белку обновлена: {protein}г/день"
        else:
            text = f"✅ Цель по белку установлена: {protein}г/день\n\nТеперь установите цель по калориям."
            markup = set_goals_kb()
            await update.message.reply_text(text, reply_markup=markup)
            return STATES['set_goals']
        
        markup = nutrition_menu_kb()
        await update.message.reply_text(text, reply_markup=markup)
        return STATES['nutrition_menu']
        
    except ValueError:
        await update.message.reply_text("Пожалуйста, введите число для белка.")
        return STATES['set_protein']

async def add_note_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Начало добавления заметки"""
    query = update.callback_query
    await query.answer()
    
    text = SD_MESSAGES['add_note']
    await query.edit_message_text(text=text)
    return STATES['wait_note_text']

async def wait_note_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка текста заметки"""
    note_text = update.message.text
    today = datetime.now().strftime('%Y-%m-%d')
    
    add_nutrition_note(update.message.from_user.id, note_text, today)
    
    text = "✅ Заметка по питанию добавлена!"
    markup = nutrition_menu_kb()
    await update.message.reply_text(text, reply_markup=markup)
    return STATES['nutrition_menu']

async def view_nutrition_date_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Начало просмотра питания по дате"""
    query = update.callback_query
    await query.answer()
    
    text = "📅 <b>Просмотр питания по дате</b>\n\n"
    text += "Введите дату в формате YYYY-MM-DD\n"
    text += "Например: 2024-01-15"
    
    await query.edit_message_text(
        text=text,
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton('Назад', callback_data=SD_CD['nutrition'])
        ]])
    )
    return STATES['wait_nutrition_date']

async def wait_nutrition_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка введенной даты для просмотра питания"""
    date_text = update.message.text.strip()
    
    # Проверяем формат даты
    try:
        from datetime import datetime
        datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        await update.message.reply_text(
            "❌ Неверный формат даты. Используйте формат YYYY-MM-DD\n"
            "Например: 2024-01-15"
        )
        return STATES['wait_nutrition_date']
    
    chat_id = update.effective_user.id
    nutrition_data = get_nutrition_summary_by_date(chat_id, date_text)
    
    if nutrition_data['meals_count'] == 0:
        text = f"📅 <b>Питание за {date_text}</b>\n\n"
        text += "❌ В этот день приёмов пищи не было зафиксировано.\n\n"
        text += "💡 Добавьте приём пищи, чтобы отслеживать своё питание!"
    else:
        text = f"📅 <b>Питание за {date_text}</b>\n\n"
        text += f"🍽️ <b>Приёмов пищи:</b> {nutrition_data['meals_count']}\n"
        text += f"🔥 <b>Всего калорий:</b> {nutrition_data['total_calories']:.1f}\n"
        text += f"🥩 <b>Всего белка:</b> {nutrition_data['total_protein']:.1f}г\n\n"
        
        # Показываем детали каждого приёма пищи
        for i, meal in enumerate(nutrition_data['meals'], 1):
            meal_time = meal['created_at'].strftime('%H:%M')
            text += f"<b>🍽️ Приём пищи #{i} ({meal_time})</b>\n"
            text += f"🔥 {meal['total_calories']:.1f} ккал | 🥩 {meal['total_protein']:.1f}г белка\n"
            
            for item in meal['items']:
                text += f"  • {item['dish_name']}: {item['grams']}г "
                text += f"({item['calories']:.1f} ккал, {item['protein']:.1f}г белка)\n"
            text += "\n"
        
        # Показываем цели пользователя, если они установлены
        goal = get_nutrition_goal(chat_id)
        if goal:
            calories_diff = goal.daily_calories - nutrition_data['total_calories']
            protein_diff = goal.daily_protein - nutrition_data['total_protein']
            
            text += f"🎯 <b>Цели на день:</b>\n"
            text += f"🔥 {goal.daily_calories} ккал "
            if calories_diff > 0:
                text += f"(осталось {calories_diff:.1f})\n"
            else:
                text += f"(перебор {abs(calories_diff):.1f})\n"
                
            text += f"🥩 {goal.daily_protein}г белка "
            if protein_diff > 0:
                text += f"(осталось {protein_diff:.1f})\n"
            else:
                text += f"(перебор {abs(protein_diff):.1f})\n"
    
    await update.message.reply_text(
        text=text,
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton('📅 Другая дата', callback_data='view_nutrition_date'),
            InlineKeyboardButton('Назад', callback_data=SD_CD['nutrition'])
        ]])
    )
    return STATES['view_nutrition_date']