"""
Обработчики для дневника
"""
from telegram import Update
from telegram.ext import ContextTypes
from datetime import datetime, date
from keyboards.keyboards import get_diary_menu_keyboard, get_diary_date_keyboard
from config import SD_MESSAGES
from states import STATES
from models import (
    get_workout_journal_by_date, get_meals_by_date, get_morning_testing,
    get_routine_progress, get_tasks_by_date
)


async def diary_home(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Главное меню дневника"""
    query = update.callback_query
    await query.answer()
    
    message = "📖 Дневник\n\nЗдесь вы можете просматривать все ваши записи за определенную дату: тренировки, питание, рутины и задачи."
    keyboard = get_diary_menu_keyboard()
    
    await query.edit_message_text(text=message, reply_markup=keyboard)
    return STATES['diary_home']


async def diary_date_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Выбор даты для просмотра дневника"""
    query = update.callback_query
    await query.answer()
    
    message = "📅 Выберите дату для просмотра дневника:\n\nВведите дату в формате YYYY-MM-DD (например: 2024-01-15)"
    keyboard = None
    
    await query.edit_message_text(text=message, reply_markup=keyboard)
    return STATES['wait_diary_date']


async def wait_diary_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ожидание даты для дневника"""
    message = update.message
    date_text = message.text
    
    try:
        # Проверяем формат даты
        selected_date = datetime.strptime(date_text, '%Y-%m-%d').date()
        context.user_data['diary_date'] = date_text
        
        # Получаем все данные за эту дату
        chat_id = message.from_user.id
        
        # Получаем тренировки
        workout_journal = get_workout_journal_by_date(chat_id, date_text)
        
        # Получаем питание
        meals = get_meals_by_date(chat_id, date_text)
        
        # Получаем утреннее тестирование
        morning_testing = get_morning_testing(chat_id, date_text)
        
        # Получаем прогресс рутин
        routine_progress = get_routine_progress(chat_id, 'morning', date_text)
        evening_progress = get_routine_progress(chat_id, 'evening', date_text)
        
        # Получаем задачи
        tasks = get_tasks_by_date(chat_id, date_text)
        
        # Формируем сообщение
        diary_text = f"📖 Дневник за {date_text}\n\n"
        
        # Утреннее тестирование
        if morning_testing:
            diary_text += f"🌅 Утреннее тестирование:\n"
            diary_text += f"• Сон: {morning_testing.sleep_hours} часов\n"
            diary_text += f"• Пробуждения: {morning_testing.wake_up_count} раз\n"
            diary_text += f"• Здоровье: {morning_testing.health_condition}/10\n"
            diary_text += f"• Усталость: {morning_testing.muscle_fatigue}/10\n"
            if morning_testing.health_complaints:
                diary_text += f"• Жалобы: {morning_testing.health_complaints}\n"
            diary_text += "\n"
        
        # Рутины
        if routine_progress:
            diary_text += f"🌅 Утренняя рутина: {'✅ Завершена' if routine_progress.is_completed else '⏳ В процессе'}\n"
        if evening_progress:
            diary_text += f"🌙 Вечерняя рутина: {'✅ Завершена' if evening_progress.is_completed else '⏳ В процессе'}\n"
        if routine_progress or evening_progress:
            diary_text += "\n"
        
        # Тренировки
        if workout_journal:
            diary_text += f"🏃‍♂️ Тренировки:\n"
            for workout in workout_journal:
                diary_text += f"• {workout.workout_type.title()}: {workout.duration} мин\n"
                diary_text += f"  Самочувствие: {workout.overall_feeling}/10\n"
                if workout.activity:
                    diary_text += f"  Активность: {workout.activity}\n"
                if workout.distance:
                    diary_text += f"  Расстояние: {workout.distance} км\n"
                if workout.avg_heart_rate:
                    diary_text += f"  Пульс: {workout.avg_heart_rate} уд/мин\n"
            diary_text += "\n"
        
        # Питание
        if meals:
            diary_text += f"🍽️ Питание:\n"
            total_calories = 0
            total_protein = 0
            for meal in meals:
                total_calories += meal.total_calories
                total_protein += meal.total_protein
                diary_text += f"• Приём пищи: {meal.total_calories:.1f} ккал, {meal.total_protein:.1f}г белка\n"
            diary_text += f"Итого: {total_calories:.1f} ккал, {total_protein:.1f}г белка\n\n"
        
        # Задачи
        if tasks:
            diary_text += f"📋 Задачи:\n"
            completed_tasks = [task for task in tasks if task.completed]
            diary_text += f"• Выполнено: {len(completed_tasks)}/{len(tasks)}\n"
            for task in tasks:
                status = "✅" if task.completed else "⭕"
                diary_text += f"  {status} {task.text}\n"
            diary_text += "\n"
        
        # Если нет данных
        if not any([workout_journal, meals, morning_testing, routine_progress, evening_progress, tasks]):
            diary_text += "📝 За эту дату нет записей в дневнике."
        
        keyboard = get_diary_date_keyboard()
        await message.reply_text(text=diary_text, reply_markup=keyboard)
        
        return STATES['diary_view']
        
    except ValueError:
        await message.reply_text("Неверный формат даты. Используйте YYYY-MM-DD")
        return STATES['wait_diary_date']


async def diary_back_to_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Возврат в меню дневника"""
    query = update.callback_query
    await query.answer()
    
    message = "📖 Дневник\n\nЗдесь вы можете просматривать все ваши записи за определенную дату: тренировки, питание, рутины и задачи."
    keyboard = get_diary_menu_keyboard()
    
    await query.edit_message_text(text=message, reply_markup=keyboard)
    return STATES['diary_home']
