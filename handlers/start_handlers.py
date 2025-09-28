"""
Обработчики для стартовых команд и навигации
"""
from telegram import Update
from telegram.ext import ContextTypes
from keyboards import get_main_menu_keyboard, get_dict_menu_keyboard
from config import MESSAGES, CALLBACK_DATA
from states import STATES
from models import find_words_for_r
from utils import format_words_for_review, get_today_date


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    reply_markup = get_main_menu_keyboard()
    text = MESSAGES['start']
    context.user_data.clear()
    
    await update.message.reply_text(text, reply_markup=reply_markup)
    return STATES['start_route']


async def return_to_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Возврат к главному меню"""
    query = update.callback_query
    await query.answer()

    reply_markup = get_main_menu_keyboard()
    text = MESSAGES['start']
    context.user_data.clear()
    
    await query.edit_message_text(text, reply_markup=reply_markup)
    return STATES['start_route']


async def dict_home(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Главная страница словаря"""
    query = update.callback_query
    await query.answer()

    # Логика повторения слов
    chat_id = str(query.message.chat.id)
    today = get_today_date()
    words = find_words_for_r(chat_id, today)
    
    context.user_data.clear()
    words_for_review = []
    
    for word_data in words:
        words_for_review.append(word_data)
    
    if words:
        text = format_words_for_review(words)
        context.user_data['words_for_review'] = words_for_review
    else:
        text = MESSAGES['no_words_today']

    reply_markup = get_dict_menu_keyboard()
    await query.edit_message_text(text, reply_markup=reply_markup)
    return STATES['dict_maiin']


async def exit_review(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Выход из режима повторения"""
    query = update.callback_query
    await query.answer()

    reply_markup = get_dict_menu_keyboard()
    context.user_data.clear()
    await query.edit_message_text(MESSAGES['dict_menu'], reply_markup=reply_markup)
    return STATES['dict_maiin']
