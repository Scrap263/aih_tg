"""
Обработчики для рутин
"""
import json
from datetime import datetime, date
from telegram import Update
from telegram.ext import ContextTypes
from keyboards.keyboards import (
    get_routines_menu_keyboard, get_morning_routine_keyboard, get_evening_routine_keyboard,
    get_routine_setup_keyboard, get_routine_actions_keyboard, get_morning_testing_keyboard,
    get_muscle_fatigue_keyboard, get_routines_list_keyboard
)
from config import SD_MESSAGES
from states import STATES
from models import (
    get_morning_routines, get_evening_routines, create_morning_routine, create_evening_routine,
    get_routine_by_id, create_routine_progress, get_routine_progress, update_routine_progress,
    save_morning_testing, get_morning_testing, is_routine_completed_today
)


async def routines_home(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Главное меню рутин"""
    query = update.callback_query
    await query.answer()
    
    markup = get_routines_menu_keyboard()
    text = SD_MESSAGES['routines_home']
    
    await query.edit_message_text(text=text, reply_markup=markup)
    return STATES['routines_home']


async def morning_routine_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Меню утренней рутины"""
    query = update.callback_query
    await query.answer()
    
    markup = get_morning_routine_keyboard()
    text = SD_MESSAGES['morning_routine']
    
    await query.edit_message_text(text=text, reply_markup=markup)
    return STATES['morning_routine']


async def evening_routine_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Меню вечерней рутины"""
    query = update.callback_query
    await query.answer()
    
    markup = get_evening_routine_keyboard()
    text = SD_MESSAGES['evening_routine']
    
    await query.edit_message_text(text=text, reply_markup=markup)
    return STATES['evening_routine']


async def start_morning_routine(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Начать утреннюю рутину"""
    query = update.callback_query
    await query.answer()
    
    chat_id = query.from_user.id
    today = str(date.today())
    
    # Проверяем, есть ли уже тестирование на сегодня
    existing_testing = get_morning_testing(chat_id, today)
    if not existing_testing:
        # Начинаем утреннее тестирование
        context.user_data['morning_testing'] = {
            'step': 'sleep_hours',
            'data': {}
        }
        
        text = SD_MESSAGES['morning_testing'] + '\n\n' + SD_MESSAGES['sleep_hours']
        await query.edit_message_text(text=text)
        return STATES['morning_testing']
    else:
        # Переходим к выбору рутины
        routines = get_morning_routines(chat_id)
        if not routines:
            text = "У вас нет настроенных утренних рутин. Сначала создайте рутину в настройках."
            markup = get_morning_routine_keyboard()
            await query.edit_message_text(text=text, reply_markup=markup)
            return STATES['morning_routine']
        
        # Проверяем, есть ли уже завершенные рутины на сегодня
        completed_today = is_routine_completed_today(chat_id, 'morning', today)
        if completed_today:
            text = "✅ Утреннее тестирование уже пройдено сегодня!\n\nВыберите рутину для выполнения:"
        else:
            text = SD_MESSAGES['start_routine']
        
        markup = get_routines_list_keyboard(routines, 'morning')
        await query.edit_message_text(text=text, reply_markup=markup)
        return STATES['select_morning_routine']


async def start_evening_routine(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Начать вечернюю рутину"""
    query = update.callback_query
    await query.answer()
    
    chat_id = query.from_user.id
    routines = get_evening_routines(chat_id)
    
    if not routines:
        text = "У вас нет настроенных вечерних рутин. Сначала создайте рутину в настройках."
        markup = get_evening_routine_keyboard()
        await query.edit_message_text(text=text, reply_markup=markup)
        return STATES['evening_routine']
    
    markup = get_routines_list_keyboard(routines, 'evening')
    text = SD_MESSAGES['start_routine']
    await query.edit_message_text(text=text, reply_markup=markup)
    return STATES['select_evening_routine']


async def setup_morning_routine(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Настройка утренней рутины"""
    query = update.callback_query
    await query.answer()
    
    markup = get_routine_setup_keyboard('morning')
    text = SD_MESSAGES['routine_setup']
    
    await query.edit_message_text(text=text, reply_markup=markup)
    return STATES['setup_morning_routine']


async def setup_evening_routine(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Настройка вечерней рутины"""
    query = update.callback_query
    await query.answer()
    
    markup = get_routine_setup_keyboard('evening')
    text = SD_MESSAGES['routine_setup']
    
    await query.edit_message_text(text=text, reply_markup=markup)
    return STATES['setup_evening_routine']


async def create_morning_routine_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Начать создание утренней рутины"""
    query = update.callback_query
    await query.answer()
    
    context.user_data['creating_routine'] = {'type': 'morning'}
    text = SD_MESSAGES['create_routine']
    
    await query.edit_message_text(text=text)
    return STATES['create_morning_routine']


async def create_evening_routine_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Начать создание вечерней рутины"""
    query = update.callback_query
    await query.answer()
    
    context.user_data['creating_routine'] = {'type': 'evening'}
    text = SD_MESSAGES['create_routine']
    
    await query.edit_message_text(text=text)
    return STATES['create_evening_routine']


async def wait_routine_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ожидание названия рутины"""
    routine_name = update.message.text
    context.user_data['creating_routine']['name'] = routine_name
    
    text = SD_MESSAGES['routine_actions']
    await update.message.reply_text(text)
    
    routine_type = context.user_data['creating_routine']['type']
    if routine_type == 'morning':
        return STATES['wait_morning_actions']
    else:
        return STATES['wait_evening_actions']


async def wait_morning_actions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ожидание действий для утренней рутины"""
    actions_text = update.message.text
    actions = [action.strip() for action in actions_text.split(',')]
    
    chat_id = update.effective_user.id
    routine_name = context.user_data['creating_routine']['name']
    actions_json = json.dumps(actions, ensure_ascii=False)
    
    routine_id = create_morning_routine(chat_id, routine_name, actions_json)
    
    text = SD_MESSAGES['routine_created'] + f"\n\nРутина '{routine_name}' создана с {len(actions)} действиями."
    markup = get_morning_routine_keyboard()
    await update.message.reply_text(text, reply_markup=markup)
    
    # Очищаем временные данные
    context.user_data.pop('creating_routine', None)
    return STATES['morning_routine']


async def wait_evening_actions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ожидание действий для вечерней рутины"""
    actions_text = update.message.text
    actions = [action.strip() for action in actions_text.split(',')]
    
    chat_id = update.effective_user.id
    routine_name = context.user_data['creating_routine']['name']
    actions_json = json.dumps(actions, ensure_ascii=False)
    
    routine_id = create_evening_routine(chat_id, routine_name, actions_json)
    
    text = SD_MESSAGES['routine_created'] + f"\n\nРутина '{routine_name}' создана с {len(actions)} действиями."
    markup = get_evening_routine_keyboard()
    await update.message.reply_text(text, reply_markup=markup)
    
    # Очищаем временные данные
    context.user_data.pop('creating_routine', None)
    return STATES['evening_routine']


async def select_morning_routine(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Выбор утренней рутины для выполнения"""
    query = update.callback_query
    await query.answer()
    
    # Извлекаем ID рутины из callback_data
    routine_id = int(query.data.split('_')[-1])
    chat_id = query.from_user.id
    today = str(date.today())
    
    # Получаем рутину
    routine = get_routine_by_id('morning', routine_id)
    if not routine:
        text = "Рутина не найдена."
        markup = get_morning_routine_keyboard()
        await query.edit_message_text(text=text, reply_markup=markup)
        return STATES['morning_routine']
    
    # Проверяем, есть ли уже прогресс на сегодня
    progress = get_routine_progress(chat_id, 'morning', today)
    if not progress:
        # Создаем новый прогресс
        progress_id = create_routine_progress(chat_id, 'morning', routine_id, today)
        current_index = 0
    else:
        progress_id = progress.id
        current_index = progress.current_action_index
        # Если рутина уже завершена, показываем сообщение
        if progress.is_completed:
            text = "Эта рутина уже выполнена на сегодня!"
            markup = get_morning_routine_keyboard()
            await query.edit_message_text(text=text, reply_markup=markup)
            return STATES['morning_routine']
    
    # Сохраняем данные в контекст
    context.user_data['routine_progress'] = {
        'progress_id': progress_id,
        'routine_id': routine_id,
        'routine_type': 'morning',
        'current_index': current_index
    }
    
    # Парсим действия
    actions = json.loads(routine.actions)
    
    if current_index >= len(actions):
        # Рутина уже завершена
        text = "Эта рутина уже выполнена на сегодня!"
        markup = get_morning_routine_keyboard()
        await query.edit_message_text(text=text, reply_markup=markup)
        return STATES['morning_routine']
    
    # Показываем текущее действие
    current_action = actions[current_index]
    text = f"{SD_MESSAGES['routine_action']}\n\n{current_action}"
    markup = get_routine_actions_keyboard(actions, current_index)
    
    await query.edit_message_text(text=text, reply_markup=markup)
    return STATES['executing_morning_routine']


async def select_evening_routine(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Выбор вечерней рутины для выполнения"""
    query = update.callback_query
    await query.answer()
    
    # Извлекаем ID рутины из callback_data
    routine_id = int(query.data.split('_')[-1])
    chat_id = query.from_user.id
    today = str(date.today())
    
    # Получаем рутину
    routine = get_routine_by_id('evening', routine_id)
    if not routine:
        text = "Рутина не найдена."
        markup = get_evening_routine_keyboard()
        await query.edit_message_text(text=text, reply_markup=markup)
        return STATES['evening_routine']
    
    # Проверяем, есть ли уже прогресс на сегодня
    progress = get_routine_progress(chat_id, 'evening', today)
    if not progress:
        # Создаем новый прогресс
        progress_id = create_routine_progress(chat_id, 'evening', routine_id, today)
        current_index = 0
    else:
        progress_id = progress.id
        current_index = progress.current_action_index
        # Если рутина уже завершена, показываем сообщение
        if progress.is_completed:
            text = "Эта рутина уже выполнена на сегодня!"
            markup = get_evening_routine_keyboard()
            await query.edit_message_text(text=text, reply_markup=markup)
            return STATES['evening_routine']
    
    # Сохраняем данные в контекст
    context.user_data['routine_progress'] = {
        'progress_id': progress_id,
        'routine_id': routine_id,
        'routine_type': 'evening',
        'current_index': current_index
    }
    
    # Парсим действия
    actions = json.loads(routine.actions)
    
    if current_index >= len(actions):
        # Рутина уже завершена
        text = "Эта рутина уже выполнена на сегодня!"
        markup = get_evening_routine_keyboard()
        await query.edit_message_text(text=text, reply_markup=markup)
        return STATES['evening_routine']
    
    # Показываем текущее действие
    current_action = actions[current_index]
    text = f"{SD_MESSAGES['routine_action']}\n\n{current_action}"
    markup = get_routine_actions_keyboard(actions, current_index)
    
    await query.edit_message_text(text=text, reply_markup=markup)
    return STATES['executing_evening_routine']


async def routine_action_completed(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Действие рутины выполнено"""
    query = update.callback_query
    await query.answer()
    
    progress_data = context.user_data.get('routine_progress')
    if not progress_data:
        text = "Ошибка: данные прогресса не найдены."
        markup = get_routines_menu_keyboard()
        await query.edit_message_text(text=text, reply_markup=markup)
        return STATES['routines_home']
    
    # Получаем рутину
    routine = get_routine_by_id(progress_data['routine_type'], progress_data['routine_id'])
    if not routine:
        text = "Ошибка: рутина не найдена."
        markup = get_routines_menu_keyboard()
        await query.edit_message_text(text=text, reply_markup=markup)
        return STATES['routines_home']
    
    actions = json.loads(routine.actions)
    
    # Переходим к следующему действию
    next_index = progress_data['current_index'] + 1
    
    if next_index >= len(actions):
        # Рутина завершена
        update_routine_progress(progress_data['progress_id'], next_index, True)
        text = SD_MESSAGES['routine_completed']
        
        if progress_data['routine_type'] == 'morning':
            markup = get_morning_routine_keyboard()
            next_state = STATES['morning_routine']
        else:
            markup = get_evening_routine_keyboard()
            next_state = STATES['evening_routine']
    else:
        # Показываем следующее действие
        update_routine_progress(progress_data['progress_id'], next_index)
        context.user_data['routine_progress']['current_index'] = next_index
        
        current_action = actions[next_index]
        text = f"{SD_MESSAGES['routine_action']}\n\n{current_action}"
        markup = get_routine_actions_keyboard(actions, next_index)
        next_state = STATES[f'executing_{progress_data["routine_type"]}_routine']
    
    await query.edit_message_text(text=text, reply_markup=markup)
    return next_state


async def skip_routine_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Пропустить действие рутины"""
    query = update.callback_query
    await query.answer()
    
    progress_data = context.user_data.get('routine_progress')
    if not progress_data:
        text = "Ошибка: данные прогресса не найдены."
        markup = get_routines_menu_keyboard()
        await query.edit_message_text(text=text, reply_markup=markup)
        return STATES['routines_home']
    
    # Получаем рутину
    routine = get_routine_by_id(progress_data['routine_type'], progress_data['routine_id'])
    if not routine:
        text = "Ошибка: рутина не найдена."
        markup = get_routines_menu_keyboard()
        await query.edit_message_text(text=text, reply_markup=markup)
        return STATES['routines_home']
    
    actions = json.loads(routine.actions)
    
    # Переходим к следующему действию
    next_index = progress_data['current_index'] + 1
    
    if next_index >= len(actions):
        # Рутина завершена
        update_routine_progress(progress_data['progress_id'], next_index, True)
        text = SD_MESSAGES['routine_completed']
        
        if progress_data['routine_type'] == 'morning':
            markup = get_morning_routine_keyboard()
            next_state = STATES['morning_routine']
        else:
            markup = get_evening_routine_keyboard()
            next_state = STATES['evening_routine']
    else:
        # Показываем следующее действие
        update_routine_progress(progress_data['progress_id'], next_index)
        context.user_data['routine_progress']['current_index'] = next_index
        
        current_action = actions[next_index]
        text = f"{SD_MESSAGES['routine_action']}\n\n{current_action}"
        markup = get_routine_actions_keyboard(actions, next_index)
        next_state = STATES[f'executing_{progress_data["routine_type"]}_routine']
    
    await query.edit_message_text(text=text, reply_markup=markup)
    return next_state


async def cancel_routine(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отменить выполнение рутины"""
    query = update.callback_query
    await query.answer()
    
    progress_data = context.user_data.get('routine_progress')
    routine_type = progress_data['routine_type'] if progress_data else 'morning'
    
    # Очищаем данные прогресса
    context.user_data.pop('routine_progress', None)
    
    if routine_type == 'morning':
        markup = get_morning_routine_keyboard()
        text = "Выполнение утренней рутины отменено."
        next_state = STATES['morning_routine']
    else:
        markup = get_evening_routine_keyboard()
        text = "Выполнение вечерней рутины отменено."
        next_state = STATES['evening_routine']
    
    await query.edit_message_text(text=text, reply_markup=markup)
    return next_state


async def routines_chart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """График рутин"""
    query = update.callback_query
    await query.answer()
    
    text = SD_MESSAGES['routines_chart']
    markup = get_routines_menu_keyboard()
    
    await query.edit_message_text(text=text, reply_markup=markup)
    return STATES['routines_home']


async def view_morning_routines(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Просмотр утренних рутин"""
    query = update.callback_query
    await query.answer()
    
    chat_id = query.from_user.id
    routines = get_morning_routines(chat_id)
    
    if not routines:
        text = "У вас нет настроенных утренних рутин."
        markup = get_morning_routine_keyboard()
    else:
        text = "📋 Ваши утренние рутины:\n\n"
        for i, routine in enumerate(routines, 1):
            actions = json.loads(routine.actions)
            text += f"{i}. {routine.name}\n"
            text += f"   Действий: {len(actions)}\n"
            text += f"   Создана: {routine.created_at.strftime('%d.%m.%Y')}\n\n"
        
        markup = get_morning_routine_keyboard()
    
    await query.edit_message_text(text=text, reply_markup=markup)
    return STATES['morning_routine']


async def view_evening_routines(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Просмотр вечерних рутин"""
    query = update.callback_query
    await query.answer()
    
    chat_id = query.from_user.id
    routines = get_evening_routines(chat_id)
    
    if not routines:
        text = "У вас нет настроенных вечерних рутин."
        markup = get_evening_routine_keyboard()
    else:
        text = "📋 Ваши вечерние рутины:\n\n"
        for i, routine in enumerate(routines, 1):
            actions = json.loads(routine.actions)
            text += f"{i}. {routine.name}\n"
            text += f"   Действий: {len(actions)}\n"
            text += f"   Создана: {routine.created_at.strftime('%d.%m.%Y')}\n\n"
        
        markup = get_evening_routine_keyboard()
    
    await query.edit_message_text(text=text, reply_markup=markup)
    return STATES['evening_routine']
