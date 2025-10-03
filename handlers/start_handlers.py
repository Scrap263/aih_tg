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
from datetime import time
from zoneinfo import ZoneInfo


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    reply_markup = get_main_menu_keyboard()
    text = MESSAGES['start']
    context.user_data.clear()
    
    await update.message.reply_text(text, reply_markup=reply_markup)
    return STATES['start_route']

async def start_and_set_reminder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    # 1. Устанавливаем ежедневное напоминание (если еще не установлено)
    # Вызываем set_daily_reminder, но не возвращаем его результат
    await set_daily_reminder(update, context) 
    
    # 2. Вызываем основную логику старта, которая возвращает состояние
    return await start(update, context) # <-- start должен вернуть STATES['start_route']

async def send_d_r(context: ContextTypes.DEFAULT_TYPE):
    print(context.job.data)
    chat_id = context.job.data['chat_id']


    if chat_id:

        today = get_today_date()
        words = find_words_for_r(chat_id, today)

        if words:
            number = len(words) + 1
            text = f'У вас есть слова для повторения. Сегодня их: {number}. Повторите их'
        else:
            text = 'У вас сегодня нет слов для повторения. Время изучить новые слова!'

        await context.bot.sendMessage(chat_id=chat_id, text=text)



async def set_daily_reminder(update: Update, context: ContextTypes.DEFAULT_TYPE):

    chat_id = update.effective_chat.id

    job_queue = context.job_queue or context.application.job_queue

    if not job_queue:
        # Эта ошибка должна исчезнуть после правильной инициализации в main.py
        await update.message.reply_text("Ошибка: Планировщик задач недоступен\\.")
        return

    # 2. УБИРАЕМ 'await' перед вызовами JobQueue
    # get_jobs_by_name - это синхронный метод JobQueue
    current_jobs = job_queue.get_jobs_by_name(str(chat_id))
    
    # current_jobs - это список. Проверяем, есть ли что-то в списке.
    if current_jobs:
        await update.message.reply_text("Ежедневное напоминание уже установлено\\.")
        return

    target_time = time(hour=16, minute=00, tzinfo=ZoneInfo('Europe/Moscow'))

    job_queue.run_daily(
        send_d_r,
        target_time,
        data = {'chat_id': chat_id}
    )


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

