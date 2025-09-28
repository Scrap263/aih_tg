"""
Обработчики для работы с Oxford 3000 словами
"""
from telegram import Update
from telegram.ext import ContextTypes
from keyboards import get_oxford_words_keyboard, get_word_example_keyboard, get_dict_menu_keyboard
from states import STATES
from models import add_word
from utils import load_dictionary, get_random_oxford_words, format_oxford_word_info
from config import MESSAGES


async def get_random_words(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Получение случайных слов из Oxford 3000"""
    query = update.callback_query
    await query.answer()

    words_list = get_random_oxford_words(5)
    context.user_data['words_l'] = words_list
    
    reply_markup = get_oxford_words_keyboard(words_list)
    await query.edit_message_text(MESSAGES['oxford_words'], reply_markup=reply_markup)
    
    return STATES['learn_ox_word']


async def choose_p_s(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Выбор части речи для слова из Oxford"""
    query = update.callback_query
    await query.answer()

    button_pressed = query.data
    words_l = context.user_data.pop('words_l')
    
    word_index_map = {
        'ox_1': 0, 'ox_2': 1, 'ox_3': 2, 'ox_4': 3, 'ox_5': 4
    }
    
    word = words_l[word_index_map[button_pressed]]
    context.user_data['word_choosed'] = word

    dictionary = load_dictionary()
    defin_l = list(dictionary[word].keys())
    defin = defin_l[0]
    context.user_data['defin'] = defin

    p_ss = list(dictionary[word][defin].keys())
    
    from telegram import InlineKeyboardButton, InlineKeyboardMarkup
    from config import CALLBACK_DATA
    
    keyboard = [[InlineKeyboardButton('В меню словаря', callback_data=CALLBACK_DATA['redirect_to_dict_menu'])]]
    
    for part_of_speech in p_ss:
        elem = [InlineKeyboardButton(part_of_speech, callback_data=part_of_speech)]
        keyboard.append(elem)
    
    transcription = dictionary[word]['транскрипция']
    text = format_oxford_word_info(word, transcription, '\n'.join(p_ss))
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup)
    return STATES['wait_ox_ps']


async def show_ox_examples(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показ примеров использования слова"""
    query = update.callback_query
    await query.answer()

    p_s = query.data
    context.user_data['p_s'] = p_s
    word = context.user_data['word_choosed']
    defin = context.user_data['defin']

    dictionary = load_dictionary()
    
    if dictionary[word][defin][p_s]:
        show_example = ''
        for example in dictionary[word][defin][p_s]:
            example = example.strip()
            show_example = show_example + '\n' + example

        context.user_data['transl'] = defin
        text = f'Слово - {word} ({p_s}) - {defin}\n{show_example}\n\nЕсли вы хотите попрактиковаться с этим словом, то добавьте его в словарь а затем выйдите в меню словаря, нажмите "повтор по дате" и введите сегодняшнюю дату'
        
        reply_markup = get_word_example_keyboard()
        await query.edit_message_text(text, reply_markup=reply_markup)
        return STATES['learn_ox_word']
    else:
        await query.edit_message_text('Неверно введена часть речи. Попробуйте еще раз')
        return STATES['wait_ox_ps']


async def add_ox_word(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Добавление слова из Oxford в словарь"""
    query = update.callback_query
    await query.answer()

    word = context.user_data.pop('word_choosed')
    p_s = context.user_data.pop('p_s')
    transl = context.user_data.pop('transl')
    chat_id = query.message.chat.id
    
    add_word(chat_id, word, p_s, transl)
    
    reply_markup = get_dict_menu_keyboard()
    await query.edit_message_text('вы в меню словаря', reply_markup=reply_markup)
    return STATES['dict_maiin']
