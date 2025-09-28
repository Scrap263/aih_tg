"""
Обработчики для режимов повторения слов
"""
from telegram import Update
from telegram.ext import ContextTypes
from keyboards import (
    get_review_type_keyboard, get_starter_word_keyboard, get_intermediate_word_keyboard,
    get_advanced_word_keyboard, get_continue_keyboard, get_ai_review_keyboard,
    get_advanced_ai_keyboard, get_cancel_keyboard
)
from states import STATES
from models import update_reviewed_word, add_sentance
from utils import format_word_info, format_correct_translation, format_incorrect_translation
from utils import format_sentence_task, shuffle_sentence_words
from config import MESSAGES
import random


async def ask_review_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Запрос типа повторения"""
    query = update.callback_query
    await query.answer()

    text = MESSAGES['review_types']
    reply_markup = get_review_type_keyboard()
    await query.edit_message_text(text, reply_markup=reply_markup)
    return STATES['start_forced_r']


async def send_word_starter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отправка слова для простого режима повторения"""
    query = update.callback_query
    await query.answer()

    words_for_review = context.user_data['words_for_review']
    if words_for_review:
        word_data = words_for_review.pop(0)
        
        word = word_data['word']
        p_s = word_data['s_part']
        transl = word_data['translation']

        context.user_data['current_word'] = word
        context.user_data['current_p_s'] = p_s
        context.user_data['current_transl'] = transl
        
        reply_markup = get_starter_word_keyboard()
        text = format_word_info(word, p_s, transl)
        await query.edit_message_text(text, reply_markup=reply_markup)
        return STATES['wait_starter_translation']
    else:
        query = update.callback_query
        await query.answer()
        
        from keyboards import get_dict_menu_keyboard
        reply_markup = get_dict_menu_keyboard()
        await query.edit_message_text(MESSAGES['no_words_review'], reply_markup=reply_markup)
        return STATES['dict_maiin']


async def end_starter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Завершение простого режима повторения"""
    user_translation = update.message.text
    right_transl = context.user_data.pop('current_transl')
    word = context.user_data.pop('current_word')
    chat_id = update.message.chat.id

    if user_translation in right_transl:
        text = format_correct_translation(word, right_transl)
    else:
        text = format_incorrect_translation(word, right_transl)
    
    update_reviewed_word(chat_id, word)
    
    reply_markup = get_continue_keyboard()
    await update.message.reply_text(text, reply_markup=reply_markup)
    return STATES['end_starter_state']


async def send_word_interm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отправка слова для среднего режима повторения"""
    query = update.callback_query
    await query.answer()

    words_for_review = context.user_data['words_for_review']
    if words_for_review:
        word_data = words_for_review.pop(0)
        
        word = word_data['word']
        p_s = word_data['s_part']
        transl = word_data['translation']

        context.user_data['current_word'] = word
        context.user_data['current_p_s'] = p_s
        context.user_data['current_transl'] = transl
        
        reply_markup = get_intermediate_word_keyboard()
        text = format_word_info(word, p_s, transl)
        await query.edit_message_text(text, reply_markup=reply_markup)
        
        # Отправляем запрос к ИИ для создания предложения
        from deepseek import DeepSeekAPI
        ai = DeepSeekAPI()
        word_with_ps = f'{word} ({p_s})'
        sentence = ai.come_up_with_sentence(word_with_ps)
        context.user_data['ai_sentence'] = sentence
        sentence_words = sentence.split(sep=' ')
        context.user_data['sentence_words_list'] = sentence_words
        
        return STATES['wait_interm_translation']
    else:
        query = update.callback_query
        await query.answer()
        
        from keyboards import get_dict_menu_keyboard
        reply_markup = get_dict_menu_keyboard()
        await query.edit_message_text(MESSAGES['no_words_review'], reply_markup=reply_markup)
        return STATES['dict_maiin']


async def show_interm_translation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показ результата перевода в среднем режиме"""
    user_translation = update.message.text
    right_transl = context.user_data['current_transl']
    word = context.user_data['current_word']
    p_s = context.user_data['current_p_s']
    words_list = context.user_data['sentence_words_list']
    
    words_text = shuffle_sentence_words(words_list)
    reply_markup = get_cancel_keyboard()
    
    if user_translation in right_transl:
        text = f"Круто! Вы вспомнили и правильно написали перевод слова {word} ({p_s}). " + format_sentence_task(words_text)
    else:
        text = f"Вот как это слово переводится: {right_transl}. " + format_sentence_task(words_text)
    
    await update.message.reply_text(text, reply_markup=reply_markup)
    return STATES['wait_interm_sentence']


async def wait_interm_sent_translation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ожидание перевода предложения в среднем режиме"""
    sentence = update.message.text
    context.user_data['sentence'] = sentence
    
    from telegram import InlineKeyboardButton, InlineKeyboardMarkup
    from config import CALLBACK_DATA
    
    keyboard = [
        [InlineKeyboardButton('Исправить английское предложение', callback_data='back_to_en_sentence')],
        [InlineKeyboardButton('В меню словаря', callback_data=CALLBACK_DATA['redirect_to_dict_menu'])]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text('А теперь переведите это предложение на русский', reply_markup=reply_markup)
    return STATES['wait_interm_user_translation']


async def check_user_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Проверка пользовательского ввода ИИ"""
    translation = update.message.text
    en_sentence = context.user_data['sentence']
    user_input = f'{en_sentence} - {translation}'
    ai_sent = context.user_data.pop('ai_sentence')
    
    await update.message.reply_text('Ваше предложение отправлено на проверку')
    
    from deepseek import DeepSeekAPI
    ai = DeepSeekAPI()
    ai_checked = ai.check_interm(user_input, ai_sent)

    reply_markup = get_ai_review_keyboard()
    await update.message.reply_text(ai_checked, reply_markup=reply_markup)
    return STATES['interm_ai_review']


async def save_interm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Сохранение результата среднего режима"""
    query = update.callback_query
    await query.answer()

    sentence = context.user_data.pop('sentence')
    word = context.user_data.pop('current_word')
    chat_id = query.message.chat.id

    update_reviewed_word(chat_id=chat_id, word=word)
    add_sentance(chat_id, sentence)

    from telegram import InlineKeyboardButton, InlineKeyboardMarkup
    keyboard = [
        [InlineKeyboardButton('Да', callback_data='interm')],
        [InlineKeyboardButton('Выход', callback_data='redirect_to_dict_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(MESSAGES['sentence_saved'], reply_markup=reply_markup)
    return STATES['start_forced_r']


async def send_next_word_f(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отправка следующего слова для продвинутого режима"""
    words_for_review = context.user_data['words_for_review']
    if words_for_review:
        query = update.callback_query
        await query.answer()

        word_data = words_for_review.pop(0)
        word = word_data['word']
        p_s = word_data['s_part']
        transl = word_data['translation']
        
        context.user_data['current_word'] = word
        context.user_data['translation'] = transl
        text = f'Слово: {word} ({p_s})\nВведите предложение с этим словом. Его проверит нейросеть'
        context.user_data['text'] = text
        
        reply_markup = get_advanced_word_keyboard()
        await query.edit_message_text(text, reply_markup=reply_markup)
        return STATES['start_forced_r']
    else:
        query = update.callback_query
        await query.answer()
        
        from keyboards import get_dict_menu_keyboard
        reply_markup = get_dict_menu_keyboard()
        await query.edit_message_text(MESSAGES['no_words_review'], reply_markup=reply_markup)
        return STATES['dict_maiin']


async def show_hint(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показ подсказки"""
    query = update.callback_query
    await query.answer()

    part_1 = context.user_data.pop('text')
    transl = context.user_data.pop('translation')

    text = f'{part_1} \nПеревод: {transl}'
    
    from telegram import InlineKeyboardButton, InlineKeyboardMarkup
    from config import CALLBACK_DATA
    
    keyboard = [
        [InlineKeyboardButton('Пропустить', callback_data='skip_word')],
        [InlineKeyboardButton('В меню словаря', callback_data=CALLBACK_DATA['redirect_to_dict_menu'])]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup)
    return STATES['start_forced_r']


async def get_sentence(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Получение предложения от пользователя"""
    sentence = update.message.text
    context.user_data['sentence'] = sentence

    from deepseek import DeepSeekAPI
    ai = DeepSeekAPI()
    response = ai.en_first(sentence)
    tr = response['translation']
    fs = response['faults']

    text = f'Перевод: {tr}.\nОшибки: {fs}'

    reply_markup = get_advanced_ai_keyboard()
    await update.message.reply_text(text, reply_markup=reply_markup)
    return STATES['first_ai_answer']
