"""
Обработчики для спорта
"""
from telegram import Update
from telegram.ext import ContextTypes
from datetime import datetime, date
import json

from config import SD_MESSAGES, SD_CD
from keyboards.keyboards import (
    get_sport_menu_keyboard, get_workout_plan_keyboard, get_workout_journal_keyboard,
    get_workout_type_keyboard, get_exercises_keyboard, get_feeling_keyboard,
    get_add_more_sets_keyboard, get_finish_workout_keyboard, get_sport_goal_keyboard
)
from models import (
    get_sport_goal, set_sport_goal, get_all_exercises, add_exercise, get_exercise_by_id,
    create_workout_plan, add_strength_exercise_to_plan, add_cardio_details_to_plan,
    create_workout_journal_entry, add_strength_set_to_journal, get_workout_journal_by_date,
    get_strength_sets_by_journal
)
from states import STATES


async def sport_home(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Главное меню спорта"""
    query = update.callback_query
    await query.answer()
    
    # Получаем текущую спортивную цель
    goal = get_sport_goal(query.from_user.id)
    goal_text = f"\n\n🎯 Текущая цель: {goal.goal_text}" if goal else "\n\n🎯 Цель не установлена"
    
    message = SD_MESSAGES['sport_home'] + goal_text
    keyboard = get_sport_menu_keyboard()
    
    await query.edit_message_text(text=message, reply_markup=keyboard)
    return STATES['sport_home']


async def workout_plan_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Меню плана тренировок"""
    query = update.callback_query
    await query.answer()
    
    message = SD_MESSAGES['workout_plan']
    keyboard = get_workout_plan_keyboard()
    
    await query.edit_message_text(text=message, reply_markup=keyboard)
    return STATES['workout_plan']


async def workout_journal_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Меню дневника тренировок"""
    query = update.callback_query
    await query.answer()
    
    message = SD_MESSAGES['workout_journal']
    keyboard = get_workout_journal_keyboard()
    
    await query.edit_message_text(text=message, reply_markup=keyboard)
    return STATES['workout_journal']


async def add_workout_plan_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Начало добавления плана тренировки"""
    query = update.callback_query
    await query.answer()
    
    message = SD_MESSAGES['add_workout_plan']
    keyboard = get_workout_type_keyboard()
    
    await query.edit_message_text(text=message, reply_markup=keyboard)
    return STATES['select_workout_type']


async def add_workout_journal_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Начало добавления записи в дневник"""
    query = update.callback_query
    await query.answer()
    
    message = SD_MESSAGES['add_workout_journal']
    keyboard = get_workout_type_keyboard()
    
    await query.edit_message_text(text=message, reply_markup=keyboard)
    return STATES['wait_journal_workout_type']


async def select_workout_type_plan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Выбор типа тренировки для плана"""
    query = update.callback_query
    await query.answer()
    
    workout_type = query.data
    context.user_data['workout_type'] = workout_type
    
    message = SD_MESSAGES['wait_workout_date']
    keyboard = None
    
    await query.edit_message_text(text=message, reply_markup=keyboard)
    return STATES['wait_workout_date']


async def select_workout_type_journal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Выбор типа тренировки для дневника"""
    query = update.callback_query
    await query.answer()
    
    workout_type = query.data
    context.user_data['workout_type'] = workout_type
    
    message = SD_MESSAGES['wait_journal_date']
    keyboard = None
    
    await query.edit_message_text(text=message, reply_markup=keyboard)
    return STATES['wait_journal_date']


async def wait_workout_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ожидание даты тренировки для плана"""
    message = update.message
    date_text = message.text
    
    try:
        # Проверяем формат даты
        datetime.strptime(date_text, '%Y-%m-%d')
        context.user_data['workout_date'] = date_text
        
        workout_type = context.user_data.get('workout_type')
        
        if workout_type == 'strength_workout':
            message_text = SD_MESSAGES['wait_exercise_name']
        else:  # cardio_workout
            message_text = SD_MESSAGES['wait_cardio_duration']
        
        await message.reply_text(text=message_text)
        
        if workout_type == 'strength_workout':
            return STATES['wait_exercise_name']
        else:
            return STATES['wait_cardio_duration']
            
    except ValueError:
        await message.reply_text("Неверный формат даты. Используйте YYYY-MM-DD")
        return STATES['wait_workout_date']


async def wait_journal_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ожидание даты тренировки для дневника"""
    message = update.message
    date_text = message.text
    
    try:
        # Проверяем формат даты
        datetime.strptime(date_text, '%Y-%m-%d')
        context.user_data['journal_date'] = date_text
        
        message_text = SD_MESSAGES['wait_journal_duration']
        await message.reply_text(text=message_text)
        
        return STATES['wait_journal_duration']
            
    except ValueError:
        await message.reply_text("Неверный формат даты. Используйте YYYY-MM-DD")
        return STATES['wait_journal_date']


async def wait_exercise_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ожидание названия упражнения"""
    message = update.message
    exercise_name = message.text
    
    # Добавляем упражнение в базу, если его нет
    exercise_id = add_exercise(exercise_name)
    context.user_data['current_exercise_id'] = exercise_id
    
    message_text = SD_MESSAGES['wait_sets']
    await message.reply_text(text=message_text)
    
    return STATES['wait_sets']


async def wait_sets(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ожидание количества подходов"""
    message = update.message
    sets = int(message.text)
    
    context.user_data['sets'] = sets
    
    message_text = SD_MESSAGES['wait_weight']
    await message.reply_text(text=message_text)
    
    return STATES['wait_weight']


async def wait_weight(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ожидание веса"""
    message = update.message
    weight = float(message.text)
    
    context.user_data['weight'] = weight
    
    message_text = SD_MESSAGES['wait_reps']
    await message.reply_text(text=message_text)
    
    return STATES['wait_reps']


async def wait_reps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ожидание количества повторений"""
    message = update.message
    reps = int(message.text)
    
    # Создаем план тренировки
    workout_plan_id = create_workout_plan(
        chat_id=message.from_user.id,
        date=context.user_data['workout_date'],
        workout_type='strength'
    )
    
    # Добавляем упражнение в план
    add_strength_exercise_to_plan(
        workout_plan_id=workout_plan_id,
        exercise_id=context.user_data['current_exercise_id'],
        sets=context.user_data['sets'],
        weight=context.user_data['weight'],
        reps=reps
    )
    
    message_text = SD_MESSAGES['workout_plan_created']
    keyboard = get_workout_plan_keyboard()
    
    await message.reply_text(text=message_text, reply_markup=keyboard)
    
    # Очищаем данные
    context.user_data.clear()
    
    return STATES['workout_plan']


async def wait_cardio_duration(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ожидание продолжительности кардио"""
    message = update.message
    duration = int(message.text)
    
    context.user_data['cardio_duration'] = duration
    
    message_text = SD_MESSAGES['wait_cardio_distance']
    await message.reply_text(text=message_text)
    
    return STATES['wait_cardio_distance']


async def wait_cardio_distance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ожидание расстояния кардио"""
    message = update.message
    distance = float(message.text)
    
    context.user_data['cardio_distance'] = distance
    
    message_text = SD_MESSAGES['wait_cardio_intensity']
    await message.reply_text(text=message_text)
    
    return STATES['wait_cardio_intensity']


async def wait_cardio_intensity(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ожидание интенсивности кардио"""
    message = update.message
    intensity = message.text
    
    # Создаем план тренировки
    workout_plan_id = create_workout_plan(
        chat_id=message.from_user.id,
        date=context.user_data['workout_date'],
        workout_type='cardio'
    )
    
    # Добавляем детали кардио
    add_cardio_details_to_plan(
        workout_plan_id=workout_plan_id,
        duration=context.user_data['cardio_duration'],
        distance=context.user_data['cardio_distance'],
        target_intensity=intensity
    )
    
    message_text = SD_MESSAGES['workout_plan_created']
    keyboard = get_workout_plan_keyboard()
    
    await message.reply_text(text=message_text, reply_markup=keyboard)
    
    # Очищаем данные
    context.user_data.clear()
    
    return STATES['workout_plan']


async def wait_journal_duration(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ожидание продолжительности тренировки в дневнике"""
    message = update.message
    duration = int(message.text)
    
    context.user_data['journal_duration'] = duration
    
    workout_type = context.user_data.get('workout_type')
    
    if workout_type == 'cardio_workout':
        message_text = SD_MESSAGES['wait_journal_activity']
        await message.reply_text(text=message_text)
        return STATES['wait_journal_activity']
    else:
        # Для силовой тренировки показываем клавиатуру самочувствия
        message_text = SD_MESSAGES['wait_journal_feeling']
        keyboard = get_feeling_keyboard()
        await message.reply_text(text=message_text, reply_markup=keyboard)
        return STATES['wait_journal_feeling']


async def wait_journal_activity(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ожидание вида активности для кардио"""
    message = update.message
    activity = message.text
    
    context.user_data['journal_activity'] = activity
    
    message_text = SD_MESSAGES['wait_journal_distance']
    await message.reply_text(text=message_text)
    
    return STATES['wait_journal_distance']


async def wait_journal_distance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ожидание расстояния для кардио"""
    message = update.message
    distance = float(message.text)
    
    context.user_data['journal_distance'] = distance
    
    message_text = SD_MESSAGES['wait_journal_heart_rate']
    await message.reply_text(text=message_text)
    
    return STATES['wait_journal_heart_rate']


async def wait_journal_heart_rate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ожидание пульса для кардио"""
    message = update.message
    heart_rate = int(message.text)
    
    context.user_data['journal_heart_rate'] = heart_rate
    
    # Показываем клавиатуру самочувствия
    message_text = SD_MESSAGES['wait_journal_feeling']
    keyboard = get_feeling_keyboard()
    await message.reply_text(text=message_text, reply_markup=keyboard)
    
    return STATES['wait_journal_feeling']


async def journal_feeling_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Выбор самочувствия в дневнике"""
    query = update.callback_query
    await query.answer()
    
    feeling = int(query.data.split('_')[1])
    context.user_data['journal_feeling'] = feeling
    
    workout_type = context.user_data.get('workout_type')
    
    if workout_type == 'cardio_workout':
        # Создаем запись в дневнике для кардио
        create_workout_journal_entry(
            chat_id=query.from_user.id,
            date=context.user_data['journal_date'],
            workout_type='cardio',
            duration=context.user_data['journal_duration'],
            overall_feeling=feeling,
            activity=context.user_data['journal_activity'],
            distance=context.user_data['journal_distance'],
            avg_heart_rate=context.user_data['journal_heart_rate']
        )
        
        message_text = SD_MESSAGES['workout_journal_created']
        keyboard = get_workout_journal_keyboard()
        
        await query.edit_message_text(text=message_text, reply_markup=keyboard)
        
        # Очищаем данные
        context.user_data.clear()
        
        return STATES['workout_journal']
    else:
        # Для силовой тренировки показываем список упражнений
        exercises = get_all_exercises()
        message_text = SD_MESSAGES['select_exercise']
        keyboard = get_exercises_keyboard(exercises)
        
        await query.edit_message_text(text=message_text, reply_markup=keyboard)
        
        return STATES['select_exercise']


async def select_exercise_for_journal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Выбор упражнения для дневника"""
    query = update.callback_query
    await query.answer()
    
    if query.data == 'add_new_exercise':
        message_text = SD_MESSAGES['wait_exercise_name']
        await query.edit_message_text(text=message_text)
        return STATES['wait_exercise_name']
    
    exercise_id = int(query.data.split('_')[2])
    context.user_data['current_exercise_id'] = exercise_id
    
    message_text = SD_MESSAGES['wait_set_weight']
    await query.edit_message_text(text=message_text)
    
    return STATES['wait_set_weight']


async def wait_set_weight(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ожидание веса для подхода"""
    message = update.message
    weight = float(message.text)
    
    context.user_data['set_weight'] = weight
    
    message_text = SD_MESSAGES['wait_set_reps']
    await message.reply_text(text=message_text)
    
    return STATES['wait_set_reps']


async def wait_set_reps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ожидание повторений для подхода"""
    message = update.message
    reps = int(message.text)
    
    # Создаем запись в дневнике, если еще не создана
    if 'journal_entry_id' not in context.user_data:
        journal_entry_id = create_workout_journal_entry(
            chat_id=message.from_user.id,
            date=context.user_data['journal_date'],
            workout_type='strength',
            duration=context.user_data['journal_duration'],
            overall_feeling=context.user_data['journal_feeling']
        )
        context.user_data['journal_entry_id'] = journal_entry_id
    
    # Добавляем подход
    add_strength_set_to_journal(
        workout_journal_id=context.user_data['journal_entry_id'],
        exercise_id=context.user_data['current_exercise_id'],
        weight=context.user_data['set_weight'],
        reps=reps
    )
    
    # Показываем клавиатуру для добавления еще подходов
    message_text = "Подход добавлен! Что дальше?"
    keyboard = get_add_more_sets_keyboard()
    
    await message.reply_text(text=message_text, reply_markup=keyboard)
    
    return STATES['select_exercise']


async def add_more_sets(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Добавление еще подходов"""
    query = update.callback_query
    await query.answer()
    
    if query.data == 'add_more_sets':
        # Возвращаемся к выбору веса для того же упражнения
        message_text = SD_MESSAGES['wait_set_weight']
        await query.edit_message_text(text=message_text)
        return STATES['wait_set_weight']
    elif query.data == 'finish_exercise':
        # Переходим к выбору другого упражнения
        exercises = get_all_exercises()
        message_text = SD_MESSAGES['select_exercise']
        keyboard = get_exercises_keyboard(exercises)
        await query.edit_message_text(text=message_text, reply_markup=keyboard)
        return STATES['select_exercise']
    else:  # finish_workout
        # Завершаем тренировку
        message_text = SD_MESSAGES['workout_journal_created']
        keyboard = get_workout_journal_keyboard()
        await query.edit_message_text(text=message_text, reply_markup=keyboard)
        
        # Очищаем данные
        context.user_data.clear()
        
        return STATES['workout_journal']


async def add_another_exercise(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Добавление еще одного упражнения"""
    query = update.callback_query
    await query.answer()
    
    exercises = get_all_exercises()
    message_text = SD_MESSAGES['select_exercise']
    keyboard = get_exercises_keyboard(exercises)
    await query.edit_message_text(text=message_text, reply_markup=keyboard)
    
    return STATES['select_exercise']


async def sport_goal_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Меню спортивной цели"""
    query = update.callback_query
    await query.answer()
    
    goal = get_sport_goal(query.from_user.id)
    
    if goal:
        message = f"🎯 Ваша спортивная цель:\n\n{goal.goal_text}"
    else:
        message = "🎯 Спортивная цель не установлена"
    
    keyboard = get_sport_goal_keyboard()
    
    await query.edit_message_text(text=message, reply_markup=keyboard)
    return STATES['sport_goal']


async def edit_sport_goal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Редактирование спортивной цели"""
    query = update.callback_query
    await query.answer()
    
    message_text = SD_MESSAGES['wait_sport_goal']
    await query.edit_message_text(text=message_text)
    
    return STATES['wait_sport_goal']


async def wait_sport_goal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ожидание спортивной цели"""
    message = update.message
    goal_text = message.text
    
    set_sport_goal(chat_id=message.from_user.id, goal_text=goal_text)
    
    message_text = SD_MESSAGES['sport_goal_set']
    keyboard = get_sport_goal_keyboard()
    
    await message.reply_text(text=message_text, reply_markup=keyboard)
    
    return STATES['sport_goal']
