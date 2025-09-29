"""
Обработчики для стартовых команд и навигации
"""
from telegram import Update
from telegram.ext import ContextTypes
from keyboards import get_main_menu_keyboard, get_dict_menu_keyboard, get_home_button
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


async def instructions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    markup = get_home_button()
    text = '''
Это Telegram‑бот для изучения английских слов с интервальным повторением: добавляйте свои слова, тренируйтесь в 3 режимах сложности, изучайте Oxford 3000, а ИИ поможет с примерами и проверкой\\.

Как начать
1\\. Нажмите \`/start\`\\.
2\\. В главном меню выберите «Словарь» или «Инструкция»\\.
3\\. Следуйте подсказкам на экране — бот всегда показывает, что делать дальше\\.

Главное меню
\\- **Словарь**: попасть в учебный раздел\\.
\\- **Инструкция**: краткая справка и навигация \\(кнопка «Домой» — вернет в меню\\)\\.

Словарь: что доступно
\\- **добавить слово**: введите слово на английском → часть речи → перевод\\.
\\- **топ нужных слов \\(Oxford 3000\\)**: бот предложит 5 случайных слов из списка; можно посмотреть примеры и добавить слово в ваш словарь\\.
\\- **Повтор по дате**: введите дату в формате \`YYYY\\-MM\\-DD\`, чтобы повторить слова, добавленные в конкретный день \\(эти повторы не засчитываются в статистику\\)\\.
\\- **Начать повторение**: выберите режим тренировки — «Легкий», «Средний» или «Продвинутый»\\.

Режимы повторения
\\- **Легкий**: переведите слово\\. После ответа бот покажет правильные варианты и предложит продолжить\\.
\\- **Средний**: переведите слово; бот сгенерирует пример предложения на английском с этим словом и даст интерактивные шаги \\(проверка перевода, сборка/смысл\\)\\.
\\- **Продвинутый**: придумайте и отправьте свое предложение с целевым словом \\(на русском и/или английском\\)\\. ИИ оценит совпадение смысла и подскажет ошибки\\.

Во всех режимах есть:
\\- **Пропуск слова** — если хотите перейти к следующему\\.
\\- **Подсказка** \\(в продвинутом\\) — ИИ поможет с идеей и формулировкой\\.
\\- **В меню словаря** — вернуться без потери прогресса текущей сессии\\.

Oxford 3000
\\- Получите 5 случайных частоупотребимых слов\\.
\\- Выберите слово → посмотрите примеры → добавьте в словарь одной кнопкой\\.

Повтор по дате
\\- Введите дату \`YYYY\\-MM\\-DD\`\\.
\\- Бот покажет список слов за день и позволит начать повтор\\.

Команды
\\- \`/start\` — запустить бота и перейти к главному меню\\.

Советы
\\- Добавляйте часть речи при добавлении слова — это повышает точность примеров от ИИ\\.
\\- Для результата важна регулярность: проходите короткие сессии повторения каждый день\\.
\\- В продвинутом режиме старайтесь придумывать контекстные предложения — так лучше закрепляется лексика\\.

Частые вопросы
\\- **Что хранится?** Ваши слова, переводы, часть речи, дата добавления и ответы в сессиях — чтобы правильно подбирать повторение\\.
\\- **Можно вернуться назад?** Да, используйте кнопку «В меню словаря» или снова откройте «Словарь» из главного\\.
\\- **Что делает ИИ?** Генерирует примеры, помогает со смыслами, подсказывает ошибки и дает мягкую обратную связь\\.

Готовы? Жмите \`/start\`, затем «Словарь» — и выбирайте: добавлять новые слова, повторять по дате или тренироваться в одном из режимов\\.
'''

    await query.edit_message_text(text, reply_markup=markup, parse_mode="MarkdownV2")
    return STATES['instructions']


async def go_home(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    markup = get_main_menu_keyboard()
    text = MESSAGES['start']
    
    await query.edit_message_text(text, reply_markup=markup)
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
        words_for_r = format_words_for_review(words)
        text = MESSAGES['there_is_review'] + words_for_r
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

