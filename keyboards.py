"""
Клавиатуры для Telegram бота
"""
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from config import CALLBACK_DATA


def get_main_menu_keyboard():
    """Главное меню"""
    keyboard = [[
        InlineKeyboardButton(text='Словарь', callback_data=CALLBACK_DATA['dict_main']),
        InlineKeyboardButton('кнопка 2', callback_data='second')
    ]]
    return InlineKeyboardMarkup(keyboard)


def get_dict_menu_keyboard():
    """Меню словаря"""
    keyboard = [
        [InlineKeyboardButton('добавить слово', callback_data=CALLBACK_DATA['add_word']),
         InlineKeyboardButton('топ нужных слов', callback_data=CALLBACK_DATA['oxford3000'])],
        [InlineKeyboardButton('Повтор по дате', callback_data=CALLBACK_DATA['review_words']),
         InlineKeyboardButton('Начать повторение', callback_data=CALLBACK_DATA['ask_type_of_review'])],
        [InlineKeyboardButton('Назад', callback_data=CALLBACK_DATA['main_menu'])]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_review_type_keyboard():
    """Клавиатура выбора типа повторения"""
    keyboard = [
        [InlineKeyboardButton('Легкий', callback_data='starter'),
         InlineKeyboardButton('Средний', callback_data='interm'),
         InlineKeyboardButton('Продвинутый', callback_data='start_forced_r')],
        [InlineKeyboardButton('В меню словаря', callback_data=CALLBACK_DATA['redirect_to_dict_menu'])]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_cancel_keyboard():
    """Клавиатура отмены/возврата"""
    keyboard = [[InlineKeyboardButton('В меню словаря', callback_data=CALLBACK_DATA['redirect_to_dict_menu'])]]
    return InlineKeyboardMarkup(keyboard)


def get_words_review_keyboard():
    """Клавиатура для повторения слов"""
    keyboard = [
        [InlineKeyboardButton('добавить слово', callback_data=CALLBACK_DATA['add_word']),
         InlineKeyboardButton('топ нужных слов', callback_data=CALLBACK_DATA['oxford3000']),
         InlineKeyboardButton('Повтор по дате', callback_data=CALLBACK_DATA['review_words']),
         InlineKeyboardButton('Начать повторение', callback_data=CALLBACK_DATA['ask_type_of_review'])]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_starter_word_keyboard():
    """Клавиатура для простого режима повторения"""
    keyboard = [
        [InlineKeyboardButton('В меню словаря', callback_data=CALLBACK_DATA['redirect_to_dict_menu']),
         InlineKeyboardButton('Пропустить', callback_data='starter_skip_word')]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_intermediate_word_keyboard():
    """Клавиатура для среднего режима повторения"""
    keyboard = [
        [InlineKeyboardButton('Пропустить', callback_data='interm_skip_word'),
         InlineKeyboardButton('В меню словаря', callback_data=CALLBACK_DATA['redirect_to_dict_menu'])]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_advanced_word_keyboard():
    """Клавиатура для продвинутого режима повторения"""
    keyboard = [
        [InlineKeyboardButton('Подсказка', callback_data='hint'),
         InlineKeyboardButton('Пропустить', callback_data='skip_word')],
        [InlineKeyboardButton('В меню словаря', callback_data=CALLBACK_DATA['redirect_to_dict_menu'])]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_continue_keyboard():
    """Клавиатура для продолжения/выхода"""
    keyboard = [
        [InlineKeyboardButton('Да', callback_data='next_word'),
         InlineKeyboardButton('Нет', callback_data=CALLBACK_DATA['redirect_to_dict_menu'])]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_ai_review_keyboard():
    """Клавиатура для ответов ИИ"""
    keyboard = [
        [InlineKeyboardButton('Все правильно', callback_data='interm_option_1')],
        [InlineKeyboardButton('Есть ошибки в английском или и в английском и русском предложении', callback_data='interm_option_2')],
        [InlineKeyboardButton('Есть ошибки только в русском предложении', callback_data='interm_option_1')],
        [InlineKeyboardButton('В меню словаря', callback_data=CALLBACK_DATA['redirect_to_dict_menu'])]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_advanced_ai_keyboard():
    """Клавиатура для продвинутого режима с ИИ"""
    keyboard = [
        [InlineKeyboardButton('Смысл совпал, ошибок нет', callback_data='option_1')],
        [InlineKeyboardButton('смысл совпал, но есть ошибки', callback_data='option_2')],
        [InlineKeyboardButton('Смысл не совпал', callback_data='option_3')],
        [InlineKeyboardButton('В меню словаря', callback_data=CALLBACK_DATA['redirect_to_dict_menu'])]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_oxford_words_keyboard(words_list):
    """Клавиатура для выбора слов из Oxford 3000"""
    keyboard = [
        [InlineKeyboardButton(words_list[0], callback_data='ox_1'),
         InlineKeyboardButton(words_list[1], callback_data='ox_2')],
        [InlineKeyboardButton(words_list[2], callback_data='ox_3'),
         InlineKeyboardButton(words_list[3], callback_data='ox_4')],
        [InlineKeyboardButton(words_list[4], callback_data='ox_5')],
        [InlineKeyboardButton('В меню словаря', callback_data=CALLBACK_DATA['redirect_to_dict_menu'])]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_word_example_keyboard():
    """Клавиатура для примеров использования слова"""
    keyboard = [
        [InlineKeyboardButton('Добавить слово в словарь', callback_data='add_ox_word')],
        [InlineKeyboardButton('В меню словаря', callback_data=CALLBACK_DATA['redirect_to_dict_menu'])]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_forced_review_keyboard():
    """Клавиатура для принудительного повторения"""
    keyboard = [
        [InlineKeyboardButton('Начать повторение', callback_data=CALLBACK_DATA['ask_type_of_review'])],
        [InlineKeyboardButton('В меню словаря', callback_data=CALLBACK_DATA['redirect_to_dict_menu'])]
    ]
    return InlineKeyboardMarkup(keyboard)
