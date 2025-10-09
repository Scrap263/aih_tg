"""
Обработчики для утреннего тестирования
"""
from datetime import date
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from keyboards.keyboards import get_morning_testing_keyboard, get_muscle_fatigue_keyboard, get_morning_routine_keyboard
from config import SD_MESSAGES
from states import STATES
from models import save_morning_testing


async def morning_testing_sleep_hours(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка ввода часов сна"""
    try:
        sleep_hours = float(update.message.text)
        context.user_data['morning_testing']['data']['sleep_hours'] = sleep_hours
        context.user_data['morning_testing']['step'] = 'wake_up_count'
        
        text = SD_MESSAGES['wake_up_count']
        await update.message.reply_text(text)
        return STATES['morning_testing']
    except ValueError:
        text = "Пожалуйста, введите число (например: 7.5)"
        await update.message.reply_text(text)
        return STATES['morning_testing']


async def morning_testing_wake_up_count(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка ввода количества пробуждений"""
    try:
        wake_up_count = int(update.message.text)
        context.user_data['morning_testing']['data']['wake_up_count'] = wake_up_count
        context.user_data['morning_testing']['step'] = 'health_condition'
        
        text = SD_MESSAGES['health_condition']
        markup = get_morning_testing_keyboard()
        await update.message.reply_text(text, reply_markup=markup)
        return STATES['morning_testing']
    except ValueError:
        text = "Пожалуйста, введите целое число"
        await update.message.reply_text(text)
        return STATES['morning_testing']


async def morning_testing_handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Универсальный обработчик текста для утреннего тестирования"""
    testing_data = context.user_data.get('morning_testing', {})
    current_step = testing_data.get('step', 'sleep_hours')
    
    if current_step == 'sleep_hours':
        return await morning_testing_sleep_hours(update, context)
    elif current_step == 'wake_up_count':
        return await morning_testing_wake_up_count(update, context)
    elif current_step == 'health_complaints':
        return await morning_testing_health_complaints(update, context)
    else:
        # Если шаг не определен, начинаем с начала
        context.user_data['morning_testing'] = {
            'step': 'sleep_hours',
            'data': {}
        }
        text = SD_MESSAGES['sleep_hours']
        await update.message.reply_text(text)
        return STATES['morning_testing']


async def morning_testing_health_condition(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка оценки состояния здоровья"""
    query = update.callback_query
    await query.answer()
    
    health_condition = int(query.data.split('_')[1])
    context.user_data['morning_testing']['data']['health_condition'] = health_condition
    context.user_data['morning_testing']['step'] = 'muscle_fatigue'
    
    text = SD_MESSAGES['muscle_fatigue']
    markup = get_muscle_fatigue_keyboard()
    await query.edit_message_text(text=text, reply_markup=markup)
    return STATES['morning_testing']


async def morning_testing_muscle_fatigue(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка оценки мышечной усталости"""
    query = update.callback_query
    await query.answer()
    
    muscle_fatigue = int(query.data.split('_')[1])
    context.user_data['morning_testing']['data']['muscle_fatigue'] = muscle_fatigue
    context.user_data['morning_testing']['step'] = 'health_complaints'
    
    text = SD_MESSAGES['health_complaints']
    await query.edit_message_text(text=text)
    return STATES['morning_testing']


async def morning_testing_health_complaints(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка жалоб на здоровье"""
    health_complaints = update.message.text
    context.user_data['morning_testing']['data']['health_complaints'] = health_complaints
    
    # Сохраняем тестирование в базу данных
    chat_id = update.effective_user.id
    today = str(date.today())
    testing_data = context.user_data['morning_testing']['data']
    
    save_morning_testing(
        chat_id=chat_id,
        date=today,
        sleep_hours=testing_data['sleep_hours'],
        wake_up_count=testing_data['wake_up_count'],
        health_condition=testing_data['health_condition'],
        muscle_fatigue=testing_data['muscle_fatigue'],
        health_complaints=health_complaints
    )
    
    # Очищаем данные тестирования
    context.user_data.pop('morning_testing', None)
    
    keyboard = [[InlineKeyboardButton(text='сохранить', callback_data='start_morning_routine')]]
    markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(reply_markup=markup)
    return STATES['morning_routine']
