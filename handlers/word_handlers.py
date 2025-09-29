"""
Обработчики для работы со словами
"""
from telegram import Update
from telegram.ext import ContextTypes
from keyboards import get_cancel_keyboard, get_dict_menu_keyboard
from config import MESSAGES
from states import STATES
from models import add_word
from utils import get_today_date


async def ask_en_word(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Запрос английского слова"""
    query = update.callback_query
    await query.answer()

    reply_markup = get_cancel_keyboard()
    await query.edit_message_text(MESSAGES['enter_en_word'], reply_markup=reply_markup)
    return STATES['get_en_word']


async def get_word(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Получение английского слова"""
    word = update.message.text
    context.user_data['en'] = word

    reply_markup = get_cancel_keyboard()
    await update.message.reply_text(MESSAGES['enter_part_of_speech'], reply_markup=reply_markup)
    return STATES['wait_p_s']


async def get_p_s(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Получение части речи"""
    p_s = update.message.text
    context.user_data['ps'] = p_s

    reply_markup = get_cancel_keyboard()
    await update.message.reply_text(MESSAGES['enter_translation'], reply_markup=reply_markup)
    return STATES['wait_translation']


async def get_translation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Получение перевода и добавление слова"""
    translation = update.message.text
    chat_id = str(update.message.chat.id)
    word = context.user_data.pop('en')
    p_s = context.user_data.pop('ps')
    
    add_word(chat_id, word, p_s, translation)
    await update.message.reply_text(MESSAGES['word_added'])
    
    reply_markup = get_dict_menu_keyboard()
    await update.message.reply_text(MESSAGES['dict_menu'], reply_markup=reply_markup)
    return STATES['dict_maiin']


async def date_for_r(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Запрос даты для повторения"""
    query = update.callback_query
    await query.answer()

    reply_markup = get_cancel_keyboard()
    await query.edit_message_text(MESSAGES['enter_date'], reply_markup=reply_markup)
    return STATES['wait_date']


async def get_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Получение даты и поиск слов для повторения"""
    from datetime import datetime
    from keyboards import get_forced_review_keyboard
    from models import forced_review
    from utils import format_words_for_review
    
    date = datetime.strptime(update.message.text, '%Y-%m-%d')
    d = date.date()
    chat_id = update.message.chat.id
    words = forced_review(chat_id, d)
    
    words_for_review = []
    for word_data in words:
        words_for_review.append(word_data)
    
    if words:
        text = format_words_for_review(words)
        reply_markup = get_forced_review_keyboard()
        context.user_data['words_for_review'] = words_for_review
        await update.message.reply_text(text, reply_markup=reply_markup)
        return STATES['start_forced_r']
    else:
        text = MESSAGES['no_words_date']
        reply_markup = get_dict_menu_keyboard()
        await update.message.reply_text(text, reply_markup=reply_markup)
        return STATES['dict_maiin']

