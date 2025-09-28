"""
Обработчики для работы с ИИ
"""
from telegram import Update
from telegram.ext import ContextTypes
from keyboards import get_cancel_keyboard
from states import STATES
from models import update_reviewed_word, add_sentance
from config import MESSAGES


async def save_review(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Сохранение результата продвинутого режима"""
    sentence = context.user_data.pop('sentence')
    word = context.user_data.pop('current_word')

    query = update.callback_query
    await query.answer()

    chat_id = query.message.chat.id

    update_reviewed_word(chat_id=chat_id, word=word)
    add_sentance(chat_id, sentence)

    from telegram import InlineKeyboardButton, InlineKeyboardMarkup
    keyboard = [
        [InlineKeyboardButton('Да', callback_data='start_forced_r')],
        [InlineKeyboardButton('Выход', callback_data='redirect_to_dict_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(MESSAGES['sentence_saved'], reply_markup=reply_markup)
    return STATES['start_forced_r']


async def option_2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка второго варианта ответа ИИ"""
    query = update.callback_query
    await query.answer()
    
    text = 'ИИ показала вам где ваши ошибки, теперь введите предложение правильно'
    reply_markup = get_cancel_keyboard()
    await query.message.chat.send_message(text, reply_markup=reply_markup)
    return STATES['wait_right_sent']


async def save_sent(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Сохранение исправленного предложения"""
    sentence = update.message.text
    word = context.user_data.pop('current_word')
    chat_id = update.message.chat.id

    update_reviewed_word(chat_id=chat_id, word=word)
    add_sentance(chat_id, sentence)
    
    from telegram import InlineKeyboardButton, InlineKeyboardMarkup
    keyboard = [
        [InlineKeyboardButton('Да', callback_data='start_forced_r')],
        [InlineKeyboardButton('Выход', callback_data='redirect_to_dict_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(MESSAGES['sentence_saved'], reply_markup=reply_markup)
    return STATES['start_forced_r']


async def option_3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка третьего варианта ответа ИИ"""
    query = update.callback_query
    await query.answer()

    text = 'Напишите по русски что вы хотели сказать в вашем предложении, ИИ поможет вам составить его на английском'
    reply_markup = get_cancel_keyboard()
    
    await query.edit_message_text(text, reply_markup=reply_markup)
    return STATES['wait_ru_sentance']


async def show_ai_sentence(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показ предложения, созданного ИИ"""
    ru_sentence = update.message.text
    
    from deepseek import DeepSeekAPI
    ai = DeepSeekAPI()
    response = ai.en_help_to_write(ai, ru_sentence)
    
    text = f'Вот как ваше предложение выглядит на английском: {response}. А теперь перепишите его чтобы вы запомнили его'
    reply_markup = get_cancel_keyboard()
    
    await update.message.reply_text(text, reply_markup=reply_markup)
    return STATES['wait_right_sent']


async def interm_option_2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка второго варианта в среднем режиме"""
    query = update.callback_query
    await query.answer()

    reply_markup = get_cancel_keyboard()
    text = f'Напишите английское предложение правильно'
    await query.message.chat.send_message(text, reply_markup=reply_markup)
    return STATES['wait_interm_right_sentence']


async def save_interm_option_2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Сохранение исправленного предложения в среднем режиме"""
    chat_id = update.message.chat.id
    word = context.user_data.pop('current_word')
    sentence = update.message.text
    
    update_reviewed_word(chat_id=chat_id, word=word)
    add_sentance(chat_id, sentence)

    from telegram import InlineKeyboardButton, InlineKeyboardMarkup
    keyboard = [
        [InlineKeyboardButton('Да', callback_data='interm')],
        [InlineKeyboardButton('Выход', callback_data='redirect_to_dict_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(MESSAGES['sentence_saved'], reply_markup=reply_markup)
    return STATES['start_forced_r']
