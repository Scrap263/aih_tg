from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters
)
import json
import os
from dotenv import load_dotenv
from models import find_words_for_r, update_structure, add_word, forced_review, update_reviewed_word, add_sentance, find_user_words
from datetime import datetime
from deepseek import DeepSeekAPI
import random

load_dotenv()

api=os.getenv('TG_API')

#callback_datas
dict_main='main_dict'

start_route, dict_maiin, get_en_word, wait_p_s, wait_translation = range(0, 5)
wait_date, start_forced_r, first_ai_answer, wait_right_sent = range(5, 9)
wait_ru_sentance, learn_ox_word, wait_ox_ps, wait_interm_translation = range(9, 13)
wait_interm_sentence, wait_interm_user_translation, interm_ai_review = range(13, 16)
wait_interm_right_sentence, wait_starter_translation, end_starter_state = range(16, 19)

dict_menu_text = 'Вы в меню словаря'

ai = DeepSeekAPI()

with open('new_dictionary.json', 'r', encoding='UTF-8') as f:
    dictionary = json.load(f)

def show_dict_menu():
    keyboard = [
        [InlineKeyboardButton('добавить слово', callback_data='add_word'),
        InlineKeyboardButton('топ нужных слов', callback_data='oxford3000')],
        [InlineKeyboardButton('Повтор по дате', callback_data='review_words'),
        InlineKeyboardButton('Начать повторение', callback_data='ask_type_of_review')],
        [InlineKeyboardButton('Назад', callback_data='main_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup

async def start(update: Update ,context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[
        InlineKeyboardButton(text='Словарь', callback_data=dict_main),
        InlineKeyboardButton('кнопка 2', callback_data='second')
    ]]

    reply_markup = InlineKeyboardMarkup(keyboard)
    text = 'Start message'
    context.user_data.clear()
    
    await update.message.reply_text(text, reply_markup=reply_markup)
    return start_route

async def return_to_start(update: Update ,context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    keyboard = [[
        InlineKeyboardButton(text='Словарь', callback_data=dict_main),
        InlineKeyboardButton('кнопка 2', callback_data='second')
    ]]

    reply_markup = InlineKeyboardMarkup(keyboard)
    text = 'Start message'

    context.user_data.clear()
    
    await query.edit_message_text(text, reply_markup=reply_markup)
    return start_route

async def dict_home(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    #Review words logic
    chat_id = str(query.message.chat.id)
    w_list = ''
    today = str(datetime.today().date())
    words = find_words_for_r(chat_id, today)
    context.user_data.clear()
    words_for_review = []
    for i in words:
        words_for_review.append(i)
        w_list = w_list + '\n' + i['word']
    if w_list:
        text = w_list
        keyboard = [[
            InlineKeyboardButton('добавить слово', callback_data='add_word'),
            InlineKeyboardButton('топ нужных слов', callback_data='oxford3000'),
            InlineKeyboardButton('Повтор по дате', callback_data='review_words'),
            InlineKeyboardButton('Начать повторение', callback_data='ask_type_of_review')
        ]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.user_data['words_for_review'] = words_for_review
    else:
        text = 'на сегодня нет слов для повторения'

    reply_markup = show_dict_menu()

    print(text)

    await query.edit_message_text(text, reply_markup=reply_markup)
    return dict_maiin


async def ask_en_word(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    keyboard = [[InlineKeyboardButton('В меню словаря', callback_data='redirect_to_dict_menu')]]
    markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text('Введите слово на английском, которое хотите добавить в словарь:', reply_markup=markup)
    return get_en_word


async def get_word(update: Update, context: ContextTypes.DEFAULT_TYPE):

    word = update.message.text
    context.user_data['en'] = word

    keyboard = [[InlineKeyboardButton('В меню словаря', callback_data='redirect_to_dict_menu')]]
    markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text('А теперь введите часть речи вашего слова: (глагол, существительное, рилагательное, наречие, фраза и тд)', reply_markup=markup)
    return wait_p_s


async def get_p_s(update: Update, context: ContextTypes.DEFAULT_TYPE):

    p_s = update.message.text
    context.user_data['ps'] = p_s

    keyboard = [[InlineKeyboardButton('В меню словаря', callback_data='redirect_to_dict_menu')]]
    markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text('А теперь введите перевод этого слова на русский', reply_markup=markup)
    return wait_translation


async def get_translation(update: Update, context: ContextTypes.DEFAULT_TYPE):

    translation = update.message.text
    chat_id = str(update.message.chat.id)
    word = context.user_data.pop('en')
    p_s = context.user_data.pop('ps')
    add_word(chat_id, word, p_s, translation)
    await update.message.reply_text('Слово добавлено!')
    word_to_add = []
    reply_markup = show_dict_menu()
    await update.message.reply_text(dict_menu_text, reply_markup=reply_markup)
    return dict_maiin

async def date_for_r(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    keyboard = [[InlineKeyboardButton('В меню словаря', callback_data='redirect_to_dict_menu')]]
    markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text('Введите дату слова за которую вы хотите повторить (эти повторения не будут зачтены). Формат даты: YYYY-MM-DD', reply_markup=markup)
    return wait_date

async def get_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    date = datetime.strptime(update.message.text, '%Y-%m-%d')
    d = date.date()
    chat_id = update.message.chat.id
    words = forced_review(chat_id, d)
    w_list = ''
    words_for_review = []
    for i in words:
        words_for_review.append(i)
        w_list = w_list + '\n' + i['word']
    if w_list:
        text = w_list
        keyboard = [[
        InlineKeyboardButton('Начать повторение', callback_data='ask_type_of_review')
        ],
        [InlineKeyboardButton('В меню словаря', callback_data='redirect_to_dict_menu')]]
        markup = InlineKeyboardMarkup(keyboard)
        context.user_data['words_for_review'] = words_for_review
        await update.message.reply_text(text, reply_markup=markup)
        return start_forced_r
    else:
        text = 'в этот день слов добавлено не было'
        reply_markup = show_dict_menu()
        await update.message.reply_text(text, reply_markup=reply_markup)
        return dict_maiin

async def ask_review_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    text = 'Бот поддерживает 3 режима повторения, которые основаны на сложности: "Легкий", "Средний" и "Продвинутый". \n\nЛегкий - нужно будет просто перевести слово.\nСредний - нужно будет перевести слово и расставить слова в правильном порядке в предложении.\nПродвинутый - самому придумать предложение со словом. \n\nВыберите желаемый вариант повторения'
    keyboard = [
        [InlineKeyboardButton('Легкий', callback_data='starter'),
         InlineKeyboardButton('Средний', callback_data='interm'),
         InlineKeyboardButton('Продвинутый', callback_data='start_forced_r')],
        [InlineKeyboardButton('В меню словаря', callback_data='redirect_to_dict_menu')] 
        ]
    markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=markup)
    return start_forced_r

async def send_word_starter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    words_for_review = context.user_data['words_for_review']
    if words_for_review:
        messagee = words_for_review.pop(0)

        word = messagee['word']
        p_s = messagee['s_part']
        transl = messagee['translation']

        context.user_data['current_word'] = word
        context.user_data['current_p_s'] = p_s
        context.user_data['current_transl'] = transl
        keyboard = [[InlineKeyboardButton('В меню словаря', callback_data='redirect_to_dict_menu'),
                     InlineKeyboardButton('Пропустить', callback_data='starter_skip_word')]]
        markup = InlineKeyboardMarkup(keyboard)

        text = f'Слово для повотрения: {word} ({p_s}).\n\nНапишите перевод этого слова (необязательно все, можно только то что помните)'
        await query.edit_message_text(text, reply_markup=markup)
        return wait_starter_translation
    else:
        query = update.callback_query
        await query.answer()

        markup = show_dict_menu()
        await query.edit_message_text('Слов для повторения нет', reply_markup=markup)
        return dict_maiin

async def end_starter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_translation = update.message.text
    right_transl = context.user_data.pop('current_transl')
    word =  context.user_data.pop('current_word')
    chat_id = update.message.chat.id

    if user_translation in right_transl:
        text = f'Круто! Вы правильно перевели слово {word}. Вот все переводы этого слова: {right_transl}. \n\nХотите продолжить повторение слов?'
    else:
        text = f'Вы хорошо справляетесь. {word} может переводится как {right_transl}.\n\n Хотите продолжить повторение слов?'
    update_reviewed_word(chat_id, word)
    keyboard = [
        [InlineKeyboardButton('Да', callback_data='next_word'),
         InlineKeyboardButton('Нет', callback_data='redirect_to_dict_menu')]
        ]
    markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(text, reply_markup=markup)
    return end_starter_state

async def send_word_interm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    words_for_review = context.user_data['words_for_review']
    if words_for_review:
        messagee = words_for_review.pop(0)

        word = messagee['word']
        p_s = messagee['s_part']
        transl = messagee['translation']

        context.user_data['current_word'] = word
        context.user_data['current_p_s'] = p_s
        context.user_data['current_transl'] = transl
        keyboard = [[InlineKeyboardButton('Пропустить', callback_data='interm_skip_word'),
                     InlineKeyboardButton('В меню словаря', callback_data='redirect_to_dict_menu')
                     ]]
        markup = InlineKeyboardMarkup(keyboard)

        text = f'Слово для повотрения: {word} ({p_s}).\n\nНапишите перевод этого слова (необязательно все, можно только то что помните)'
        await query.edit_message_text(text, reply_markup=markup)
        #send message to deepseek
        word_with_ps = f'{word} ({p_s})'
        w = str(word_with_ps)
        print(w)
        sentence = ai.come_up_with_sentence(w)
        context.user_data['ai_sentence'] = sentence
        sentence_words = sentence.split(sep=' ')
        context.user_data['sentence_words_list'] = sentence_words
        return wait_interm_translation
    else:
        query = update.callback_query
        await query.answer()

        markup = show_dict_menu()
        await query.edit_message_text('Слов для повторения нет', reply_markup=markup)
        return dict_maiin

async def show_interm_translation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_translation = update.message.text
    right_transl = context.user_data['current_transl']
    word = context.user_data['current_word']
    p_s = context.user_data['current_p_s']
    words_list = context.user_data['sentence_words_list']
    print(words_list)

    words_text = ''
    number = int(len(words_list))
    print(number)
    while number != 0:
        r_int = random.randint(0, number-1)
        w = words_list.pop(r_int)
        words_text += w + ' | '
        number -= 1
    keyboard = [[InlineKeyboardButton('В меню словаря', callback_data='redirect_to_dict_menu')]]
    markup = InlineKeyboardMarkup(keyboard)
    if user_translation in right_transl:
        text = f'Круто! Вы вспомнили и правильно написали перевод слова {word} ({p_s}). Теперь двигаемся дальше. Ниже приведены слова которые нужно расположить в правильном порядке и получится предложение\n\nВот слова: [{words_text}]\nНапишите получившееся предложение'
    else:
        text = f'Вот как это слово переводится: {right_transl}. Теперь двигаемся дальше. Ниже приведены слова которые нужно расположить в правильном порядке и получится предложение\n\nВот слова: [{words_text}]\nНапишите получившееся предложение'
    await update.message.reply_text(text, reply_markup=markup)
    return wait_interm_sentence

async def wait_interm_sent_translation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sentence = update.message.text
    context.user_data['sentence'] = sentence
    keyboard = [
        [InlineKeyboardButton('Исправить английское предложение', callback_data='back_to_en_sentence')]
        [InlineKeyboardButton('В меню словаря', callback_data='redirect_to_dict_menu')]]
    markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('А теперь переведите это предложение на русский', reply_markup=markup)
    return wait_interm_user_translation

async def check_user_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    translation = update.message.text
    en_sentence = context.user_data['sentence']
    user_input = f'{en_sentence} - {translation}'
    ai_sent = context.user_data.pop('ai_sentence')
    await update.message.reply_text('Ваше предложение отправлено на проверку')
    ai_checked = ai.check_interm(user_input, ai_sent)

    keyboard = [
        [InlineKeyboardButton('Все правильно', callback_data='interm_option_1')],
        [InlineKeyboardButton('Есть ошибки в английском или и в английском и русском предложении', callback_data='interm_option_2')],
        [InlineKeyboardButton('Есть ошибки только в русском предложении', callback_data='interm_option_1')],
        [InlineKeyboardButton('В меню словаря', callback_data='redirect_to_dict_menu')]
    ]
    markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(ai_checked, reply_markup=markup)
    return interm_ai_review
    
async def save_interm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    sentence = context.user_data.pop('sentence')
    word = context.user_data.pop('current_word')

    chat_id = query.message.chat.id
    print(chat_id)

    update_reviewed_word(chat_id=chat_id, word=word)
    add_sentance(chat_id, sentence)

    keyboard = [
        [InlineKeyboardButton('Да', callback_data='interm')],
        [InlineKeyboardButton('Выход', callback_data='redirect_to_dict_menu')]
        ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text('Ваше предложение сохранено\nХотите продолжить?', reply_markup=reply_markup)
    return start_forced_r

async def interm_option_2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    keyboard = [[InlineKeyboardButton('В меню словаря', callback_data='redirect_to_dict_menu')]]
    markup = InlineKeyboardMarkup(keyboard)
    text = f'Напишите английское предложение правильно'
    await query.message.chat.send_message(text, reply_markup=markup)
    return wait_interm_right_sentence

async def save_interm_option_2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat.id
    word = context.user_data.pop('current_word')
    sentence = update.message.text
    update_reviewed_word(chat_id=chat_id, word=word)
    add_sentance(chat_id, sentence)

    keyboard = [
        [InlineKeyboardButton('Да', callback_data='interm')],
        [InlineKeyboardButton('Выход', callback_data='redirect_to_dict_menu')]
        ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Ваше предложение сохранено\nХотите продолжить?', reply_markup=reply_markup)
    return start_forced_r

async def send_next_word_f(update: Update, context: ContextTypes.DEFAULT_TYPE):
    words_for_review = context.user_data['words_for_review']
    if words_for_review:
        query = update.callback_query
        await query.answer()

        messagee = words_for_review.pop(0)
        word = messagee['word']
        p_s = messagee['s_part']
        transl = messagee['translation']
        context.user_data['current_word'] = word
        context.user_data['translation'] = transl
        text = f'Слово: {word} ({p_s})\nВведите предложение с этим словом. Его проверит нейросеть'
        context.user_data['text'] = text
        keyboard = [[
            InlineKeyboardButton('Подсказка', callback_data='hint'),
            InlineKeyboardButton('Пропустить', callback_data='skip_word')
        ],
        [InlineKeyboardButton('В меню словаря', callback_data='redirect_to_dict_menu')]]
        markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, reply_markup=markup)
        return start_forced_r
    else:
        query = update.callback_query
        await query.answer()

        markup = show_dict_menu()
        await query.edit_message_text('Слов для повторения нет', reply_markup=markup)
        return dict_maiin

async def show_hint(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    part_1 = context.user_data.pop('text')
    transl = context.user_data.pop('translation')

    text = f'{part_1} \nПеревод: {transl}'
    keyboard = [[InlineKeyboardButton('Пропустить', callback_data='skip_word')],
                [InlineKeyboardButton('В меню словаря', callback_data='redirect_to_dict_menu')]]
    markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=markup)
    return start_forced_r

async def get_sentence(update: Update, context: ContextTypes.DEFAULT_TYPE):

    sentence = update.message.text
    context.user_data['sentence'] = sentence

    response = ai.en_first(sentence)
    tr = response['translation']
    fs = response['faults']

    text = f'Перевод: {tr}.\nОшибки: {fs}'

    keyboard = [
        [InlineKeyboardButton('Смысл совпал, ошибок нет', callback_data='option_1')],
        [InlineKeyboardButton('смысл совпал, но есть ошибки', callback_data='option_2')],
        [InlineKeyboardButton('Смысл не совпал', callback_data='option_3')],
        [InlineKeyboardButton('В меню словаря', callback_data='redirect_to_dict_menu')]
    ]
    markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(text, reply_markup=markup)
    return first_ai_answer

async def save_review(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sentence = context.user_data.pop('sentence')
    word = context.user_data.pop('current_word')

    query = update.callback_query
    await query.answer()

    chat_id = query.message.chat.id
    print(chat_id)

    update_reviewed_word(chat_id=chat_id, word=word)
    add_sentance(chat_id, sentence)

    keyboard = [
        [InlineKeyboardButton('Да', callback_data='start_forced_r')],
        [InlineKeyboardButton('Выход', callback_data='redirect_to_dict_menu')]
        ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text('Ваше предложение сохранено\nХотите продолжить?', reply_markup=reply_markup)
    return start_forced_r

async def option_2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    text = 'ИИ показала вам где ваши ошибки, теперь введите предложение правильно'
    keyboard = [[InlineKeyboardButton('В меню словаря', callback_data='redirect_to_dict_menu')]]
    markup = InlineKeyboardMarkup(keyboard)
    await query.message.chat.send_message(text, reply_markup=markup)
    return wait_right_sent

async def save_sent(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sentence = update.message.text
    word = context.user_data.pop('current_word')
    chat_id = update.message.chat.id

    update_reviewed_word(chat_id=chat_id, word=word)
    add_sentance(chat_id, sentence)    
    
    keyboard = [
        [InlineKeyboardButton('Да', callback_data='start_forced_r')],
        [InlineKeyboardButton('Выход', callback_data='redirect_to_dict_menu')]
        ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Ваше предложение сохранено\nХотите продолжить?', reply_markup=reply_markup)
    return start_forced_r

async def option_3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    text = 'Напишите по русски что вы хотели сказать в вашем предложении, ИИ поможет вам составить его на английском'
    keyboard = [[InlineKeyboardButton('В меню словаря', callback_data='redirect_to_dict_menu')]]
    markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=markup)
    return wait_ru_sentance

async def show_ai_sentence(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ru_sentence = update.message.text
    response = ai.en_help_to_write(ai, ru_sentence)
    text = f'Вот как ваше предложение выглядит на английском: {response}. А теперь перепишите его чтобы вы запомнили его'
    keyboard = [[InlineKeyboardButton('В меню словаря', callback_data='redirect_to_dict_menu')]]
    markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(text, reply_markup=markup)
    return wait_right_sent

async def exit_review(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    reply_markup = show_dict_menu()
    context.user_data.clear()
    await query.edit_message_text(dict_menu_text, reply_markup=reply_markup)
    return dict_maiin

async def get_random_words(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    with open('words_list.json', 'r') as wl:
        oxford_3000_words = json.load(wl)
    i = 0
    words_l = []
    while i < 5:
        random_int = random.randint(0, 2999)
        w = oxford_3000_words[random_int]
        words_l.append(w)
        i += 1
    context.user_data['words_l'] = words_l
    keyboard = [
        [InlineKeyboardButton(words_l[0], callback_data='ox_1'),
         InlineKeyboardButton(words_l[1], callback_data='ox_2')],
        [InlineKeyboardButton(words_l[2], callback_data='ox_3'),
         InlineKeyboardButton(words_l[3], callback_data='ox_4')],
        [InlineKeyboardButton(words_l[4], callback_data='ox_5')],
        [InlineKeyboardButton('В меню словаря', callback_data='redirect_to_dict_menu')]
        ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text('Вот вам 5 рандомных слов их 3000 самых используемых английских слов. Нажмите на слово чтобы изучить его', reply_markup=reply_markup)    
    words_l = []
    return learn_ox_word

async def choose_p_s(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    button_pressed = query.data
    words_l = context.user_data.pop('words_l')

    if button_pressed == 'ox_1':
        word = words_l[0]
    elif button_pressed == 'ox_2':
        word = words_l[1]
    elif button_pressed == 'ox_3':
        word = words_l[2]
    elif button_pressed == 'ox_4':
        word = words_l[3]
    elif button_pressed == 'ox_5':
        word = words_l[4]
    context.user_data['word_choosed'] = word

    defin_l = list(dictionary[word].keys())
    defin = defin_l[0]

    context.user_data['defin'] = defin

    p_ss = list(dictionary[word][defin].keys())
    p_ss_text = ''
    keyboard = [[InlineKeyboardButton('В меню словаря', callback_data='redirect_to_dict_menu')]]
    for i in p_ss:
        elem = [InlineKeyboardButton(i, callback_data=i)]
        keyboard.append(elem)
        p_ss_text = p_ss_text + '\n' + i
    transcription = dictionary[word]['транскрипция']
    text = f'Слово {word} читается как - {transcription}. Внизу на кнопках написаны части речи в которых это слово может быть использовано.\n\nНажмите на кнопку, чтобы понять как это слово используется'
    markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=markup)
    return wait_ox_ps

async def show_ox_examples(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    p_s = query.data
    print(p_s)
    context.user_data['p_s'] = p_s
    word = context.user_data['word_choosed']
    defin = context.user_data['defin']

    if dictionary[word][defin][p_s]:
        show_example = ''
        for example in dictionary[word][defin][p_s]:
            example.strip()
            show_example = show_example + '\n' + example

        context.user_data['transl'] = defin
        text = f'Слово - {word} ({p_s}) - {defin}\n{show_example}\n\nЕсли вы хотите попрактиковаться с этим словом, то добавьте его в словарь а затем выйдите в меню словаря, нажмите "повтор по дате" и введите сегодняшнюю дату'
        keyboard = [[InlineKeyboardButton('Добавить слово в словарь', callback_data='add_ox_word')],
                    [InlineKeyboardButton('В меню словаря', callback_data='redirect_to_dict_menu')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, reply_markup=reply_markup)
        return learn_ox_word
    else:
        await query.edit_message_text('Неверно введена часть речи. Попробуйте еще раз')
        return wait_ox_ps
        
async def add_ox_word(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    word = context.user_data.pop('word_choosed')
    p_s = context.user_data.pop('p_s')
    transl = context.user_data.pop('transl')
    chat_id = query.message.chat.id
    add_word(chat_id, word, p_s, transl)
    markup = show_dict_menu()
    await query.edit_message_text('вы в меню словаря', reply_markup=markup)
    return dict_maiin

#Закончить
async def search_word_in_dictionary(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    

def main():

    bot = Application.builder().token(api).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states= {
            start_route: [
                CallbackQueryHandler(dict_home, pattern='^' + dict_main + '$')
            ],
            dict_maiin : [
                CallbackQueryHandler(ask_en_word, pattern='^' + 'add_word' + '$'),
                CallbackQueryHandler(date_for_r, pattern='^' + 'review_words' + '$'),
                CallbackQueryHandler(ask_review_type , pattern='^' + 'ask_type_of_review' + '$'),
                CallbackQueryHandler(send_next_word_f, pattern='^' + 'start_forced_r' + '$'),
                CallbackQueryHandler(get_random_words, pattern='^' + 'oxford3000' + '$'),
                CallbackQueryHandler(return_to_start, pattern='^' + 'main_menu' + '$')
            ],
            get_en_word : [
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_word),
                CallbackQueryHandler(dict_home, pattern='^' + 'redirect_to_dict_menu' + '$')
            ],
            wait_p_s : [
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_p_s),
                CallbackQueryHandler(dict_home, pattern='^' + 'redirect_to_dict_menu' + '$')
            ],
            wait_translation: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_translation),
                CallbackQueryHandler(dict_home, pattern='^' + 'redirect_to_dict_menu' + '$')
            ],
            wait_date : [
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_date),
                CallbackQueryHandler(dict_home, pattern='^' + 'redirect_to_dict_menu' + '$')
            ],
            start_forced_r : [
                CallbackQueryHandler(send_next_word_f, pattern='^' + 'start_forced_r' + '$'),
                CallbackQueryHandler(show_hint, pattern='^' + 'hint' + '$'),
                CallbackQueryHandler(dict_home, pattern='^' + 'redirect_to_dict_menu' + '$'),
                CallbackQueryHandler(ask_review_type , pattern='^' + 'ask_type_of_review' + '$'),
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_sentence),
                CallbackQueryHandler(send_next_word_f, pattern='^' + 'skip_word' + '$'),
                CallbackQueryHandler(send_word_interm , pattern='^' + 'interm' + '$'),
                CallbackQueryHandler(send_word_starter, pattern='^' + 'starter' + '$')
            ],
            first_ai_answer : [
               CallbackQueryHandler(save_review, pattern='^' + 'option_1' + '$'),
               CallbackQueryHandler(option_2, pattern='^' + 'option_2' + '$'),
               CallbackQueryHandler(option_3, pattern='^' + 'option_3' + '$'),
               CallbackQueryHandler(dict_home, pattern='^' + 'redirect_to_dict_menu' + '$')
            ],
            wait_right_sent: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, save_sent),
                CallbackQueryHandler(dict_home, pattern='^' + 'redirect_to_dict_menu' + '$')
            ],
            wait_ru_sentance: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, show_ai_sentence),
                CallbackQueryHandler(dict_home, pattern='^' + 'redirect_to_dict_menu' + '$')
            ],
            learn_ox_word : [
                CallbackQueryHandler(choose_p_s, pattern='^' + 'ox_1' + '$'),
                CallbackQueryHandler(choose_p_s, pattern='^' + 'ox_2' + '$'),
                CallbackQueryHandler(choose_p_s, pattern='^' + 'ox_3' + '$'),
                CallbackQueryHandler(choose_p_s, pattern='^' + 'ox_4' + '$'),
                CallbackQueryHandler(choose_p_s, pattern='^' + 'ox_5' + '$'),
                CallbackQueryHandler(add_ox_word, pattern='^' + 'add_ox_word' + '$'),
                CallbackQueryHandler(dict_home, pattern='^' + 'redirect_to_dict_menu' + '$')
            ],
            wait_ox_ps : [
                CallbackQueryHandler(show_ox_examples),
                MessageHandler(filters.TEXT & ~filters.COMMAND, show_ox_examples),
                CallbackQueryHandler(dict_home, pattern='^' + 'redirect_to_dict_menu' + '$')
            ],
            wait_interm_translation : [
                MessageHandler(filters.TEXT & ~filters.COMMAND, show_interm_translation),
                CallbackQueryHandler(dict_home, pattern='^' + 'redirect_to_dict_menu' + '$'),
                CallbackQueryHandler(send_word_interm, pattern='^' + 'interm_skip_word' + '$')
            ],
            wait_interm_sentence : [
                MessageHandler(filters.TEXT & ~filters.COMMAND, wait_interm_sent_translation),
                CallbackQueryHandler(dict_home, pattern='^' + 'redirect_to_dict_menu' + '$')
            ],
            wait_interm_user_translation : [
                MessageHandler(filters.TEXT & ~filters.COMMAND, check_user_input),
                CallbackQueryHandler(show_interm_translation, pattern='^' + 'back_to_en_sentence' + '$'),
                CallbackQueryHandler(dict_home, pattern='^' + 'redirect_to_dict_menu' + '$')
            ],
            interm_ai_review : [
                CallbackQueryHandler(save_interm, pattern='^' + 'interm_option_1' + '$'),
                CallbackQueryHandler(interm_option_2, pattern='^' + 'interm_option_2' + '$'),
                CallbackQueryHandler(dict_home, pattern='^' + 'redirect_to_dict_menu' + '$')
            ],
            wait_interm_right_sentence : [
                MessageHandler(filters.TEXT & ~filters.COMMAND, save_interm_option_2),
                CallbackQueryHandler(dict_home, pattern='^' + 'redirect_to_dict_menu' + '$')
            ],
            wait_starter_translation : [
                MessageHandler(filters.TEXT & ~filters.COMMAND, end_starter),
                CallbackQueryHandler(dict_home, pattern='^' + 'redirect_to_dict_menu' + '$'),
                CallbackQueryHandler(send_word_starter, pattern='^' + 'starter_skip_word' + '$')
            ],
            end_starter_state : [
                CallbackQueryHandler(dict_home, pattern='^' + 'redirect_to_dict_menu' + '$'),
                CallbackQueryHandler(send_word_starter, pattern='^' + 'next_word' + '$')
            ]
        },
        fallbacks= [CommandHandler('start', start)]
    )

    bot.add_handler(conv_handler)

    bot.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()