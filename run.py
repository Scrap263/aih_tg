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
import os
from dotenv import load_dotenv
from models import find_words_for_r, update_structure, add_word, forced_review
from datetime import datetime

load_dotenv()

api=os.getenv('TG_API')

#callback_datas
dict_main='main_dict'

start_route, dict_maiin, get_en_word, wait_p_s, wait_translation = range(0, 5)
wait_date, start_forced_r = range(5, 7)

words_for_review = []

async def start(update: Update ,context: ContextTypes.DEFAULT_TYPE):
    update_structure()
    keyboard = [[
        InlineKeyboardButton(text='Словарь', callback_data=dict_main),
        InlineKeyboardButton('кнопка 2', callback_data='second')
    ]]

    reply_markup = InlineKeyboardMarkup(keyboard)
    text = 'Start message'
    
    await update.message.reply_text(text, reply_markup=reply_markup)
    return start_route

async def dict_home(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    keyboard = [[
        InlineKeyboardButton('добавить слово', callback_data='add_word'),
        InlineKeyboardButton('топ нужных слов', callback_data='oxford3000'),
        InlineKeyboardButton('Повтор по дате', callback_data='review_words')
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    #Review words logic
    chat_id = str(query.message.chat.id)
    w_list = ''
    today = str(datetime.today().date())
    words = find_words_for_r(chat_id, today)
    for i in words:
        w_list = w_list + '\n' + i['word']
    if w_list:
        text = w_list
    else:
        text = 'на сегодня нет слов для повторения'

    print(text)

    await query.edit_message_text(text, reply_markup=reply_markup)
    return dict_maiin


async def ask_en_word(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    await query.edit_message_text('Введите слово на английском, которое хотите добавить в словарь:')
    return get_en_word


async def get_word(update: Update, context: ContextTypes.DEFAULT_TYPE):

    word = update.message.text
    context.user_data['en'] = word

    await update.message.reply_text('А теперь введите часть речи вашего слова: (Verb - глагол, noun - существительное, adjective - прилагательное, adverb - наречие, phrase - фраза)')
    return wait_p_s


async def get_p_s(update: Update, context: ContextTypes.DEFAULT_TYPE):

    p_s = update.message.text
    context.user_data['ps'] = p_s

    await update.message.reply_text('А теперь введите перевод этого слова на русский')
    return wait_translation


async def get_translation(update: Update, context: ContextTypes.DEFAULT_TYPE):

    translation = update.message.text
    chat_id = str(update.message.chat.id)
    word = context.user_data.pop('en')
    p_s = context.user_data.pop('ps')
    add_word(chat_id, word, p_s, translation)
    await update.message.reply_text('Слово добавлено!')
    word_to_add = []
    keyboard = [[
        InlineKeyboardButton('добавить слово', callback_data='add_word'),
        InlineKeyboardButton('топ нужных слов', callback_data='oxford3000'),
        InlineKeyboardButton('Повтор по дате', callback_data='review_words')
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Вы в меню словаря', reply_markup=reply_markup)
    return dict_maiin

async def date_for_r(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    await query.edit_message_text('Введите дату слова за которую вы хотите повторить (эти повторения не будут зачтены). Формат даты: YYYY-MM-DD', )
    return wait_date

async def get_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    date = datetime.strptime(update.message.text, '%Y-%m-%d')
    d = date.date()
    chat_id = update.message.chat.id
    words = forced_review(chat_id, d)
    w_list = ''
    for i in words:
        words_for_review.append(i)
        w_list = w_list + '\n' + i['word']
    if w_list:
        text = w_list
        keyboard = [[
        InlineKeyboardButton('Начать повторение', callback_data='start_forced_r')
        ]]
        markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(text, reply_markup=markup)
        return start_forced_r
    else:
        text = 'в этот день слов добавлено не было'
        keyboard = [[
        InlineKeyboardButton('добавить слово', callback_data='add_word'),
        InlineKeyboardButton('топ нужных слов', callback_data='oxford3000'),
        InlineKeyboardButton('Повтор по дате', callback_data='review_words')
        ]]
        markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(text, reply_markup=markup)
        return dict_maiin

async def send_next_word_f(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if words_for_review:
        query = update.callback_query
        await query.answer()

        messagee = words_for_review.pop(0)
        word = messagee['word']
        p_s = messagee['s_part']
        transl = messagee['translation']
        context.user_data['translation'] = transl
        text = f'Слово: {word} ({p_s})\nВведите предложение с этим словом. Его проверит нейросеть'
        context.user_data['text'] = text
        keyboard = [[
            InlineKeyboardButton('Подсказка', callback_data='hint')
        ]]
        markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, reply_markup=markup)

async def show_hint(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    part_1 = context.user_data.pop('text')
    transl = context.user_data.pop('translation')

    text = f'{part_1} \nПеревод: {transl}'
    await query.edit_message_text(text)


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
                CallbackQueryHandler(date_for_r, pattern='^' + 'review_words' + '$')
            ],
            get_en_word : [
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_word)
            ],
            wait_p_s : [
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_p_s)
            ],
            wait_translation: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_translation)
            ],
            wait_date : [
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_date)
            ],
            start_forced_r : [
                #Тут нужно заменить func name на функцию которая будет вызываться для повторения
                CallbackQueryHandler(send_next_word_f, pattern='^' + 'start_forced_r' + '$'),
                CallbackQueryHandler(show_hint, pattern='^' + 'hint' + '$')
            ]
        },
        fallbacks= [CommandHandler('start', start)]
    )

    bot.add_handler(conv_handler)

    bot.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()