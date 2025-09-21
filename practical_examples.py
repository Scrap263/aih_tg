"""
Практические примеры декораторов для вашего проекта aih_tg

Этот файл содержит примеры, адаптированные под структуру вашего проекта.
"""

import asyncio
from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from states import bot  # Импортируем ваш бот из states.py

# =============================================================================
# ПРИМЕРЫ ДЕКОРАТОРОВ ДЛЯ ВАШЕГО ПРОЕКТА
# =============================================================================

# 1. Обработка команд для работы со словарем
@bot.message_handler(commands=['add_word'])
async def add_word_command(message: Message):
    """Обработчик команды /add_word для добавления слов в словарь"""
    await bot.reply_to(message, "Введите слово для добавления в словарь:")

@bot.message_handler(commands=['search'])
async def search_word_command(message: Message):
    """Обработчик команды /search для поиска слов в словаре"""
    await bot.reply_to(message, "Введите слово для поиска:")

@bot.message_handler(commands=['list'])
async def list_words_command(message: Message):
    """Обработчик команды /list для показа всех слов"""
    await bot.reply_to(message, "Список всех слов в словаре:")

# 2. Обработка текстовых сообщений с разными фильтрами
@bot.message_handler(content_types=['text'])
async def text_message_handler(message: Message):
    """Обработчик всех текстовых сообщений"""
    text = message.text.lower()
    
    if text.startswith('добавить'):
        await handle_add_word(message)
    elif text.startswith('найти'):
        await handle_search_word(message)
    elif text.startswith('показать'):
        await handle_show_words(message)
    else:
        await bot.reply_to(message, "Не понимаю команду. Используйте /help для справки.")

# 3. Обработка документов (CSV файлы)
@bot.message_handler(content_types=['document'])
async def document_handler(message: Message):
    """Обработчик документов (CSV файлы для импорта слов)"""
    if message.document.file_name.endswith('.csv'):
        await bot.reply_to(message, "Получен CSV файл. Обрабатываю...")
        # Здесь можно добавить логику обработки CSV
    else:
        await bot.reply_to(message, "Пожалуйста, отправьте CSV файл.")

# 4. Обработка с регулярными выражениями
@bot.message_handler(regexp=r'^[а-яё\s]+$', content_types=['text'])
async def russian_text_handler(message: Message):
    """Обработчик текста на русском языке"""
    await bot.reply_to(message, f"Получен русский текст: {message.text}")

# 5. Обработка callback запросов для интерактивных кнопок
@bot.callback_query_handler(func=lambda call: call.data.startswith('word_'))
async def word_callback_handler(call: CallbackQuery):
    """Обработчик callback запросов для работы со словами"""
    word_id = call.data.split('_')[1]
    
    if call.data.endswith('_delete'):
        await handle_delete_word(call, word_id)
    elif call.data.endswith('_edit'):
        await handle_edit_word(call, word_id)
    elif call.data.endswith('_show'):
        await handle_show_word(call, word_id)

# 6. Обработка только для приватных чатов
@bot.message_handler(chat_types=['private'])
async def private_message_handler(message: Message):
    """Обработчик сообщений только в приватных чатах"""
    await bot.reply_to(message, "Это приватный чат. Здесь можно работать со словарем.")

# 7. Обработка с пользовательскими функциями
def is_admin_user(message: Message) -> bool:
    """Проверяет, является ли пользователь администратором"""
    admin_ids = [123456789]  # Замените на реальные ID администраторов
    return message.from_user.id in admin_ids

@bot.message_handler(func=is_admin_user)
async def admin_message_handler(message: Message):
    """Обработчик сообщений от администраторов"""
    await bot.reply_to(message, "Привет, администратор! Доступны дополнительные команды.")

# 8. Обработка длинных сообщений
def is_long_message(message: Message) -> bool:
    """Проверяет, является ли сообщение длинным"""
    return len(message.text) > 100 if message.text else False

@bot.message_handler(func=is_long_message)
async def long_message_handler(message: Message):
    """Обработчик длинных сообщений"""
    await bot.reply_to(message, "Сообщение слишком длинное. Попробуйте разбить его на части.")

# =============================================================================
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# =============================================================================

async def handle_add_word(message: Message):
    """Обработка добавления слова"""
    word = message.text.replace('добавить', '').strip()
    if word:
        # Здесь можно добавить логику сохранения в базу данных
        await bot.reply_to(message, f"Слово '{word}' добавлено в словарь!")
    else:
        await bot.reply_to(message, "Пожалуйста, укажите слово для добавления.")

async def handle_search_word(message: Message):
    """Обработка поиска слова"""
    word = message.text.replace('найти', '').strip()
    if word:
        # Здесь можно добавить логику поиска в базе данных
        await bot.reply_to(message, f"Поиск слова '{word}'...")
    else:
        await bot.reply_to(message, "Пожалуйста, укажите слово для поиска.")

async def handle_show_words(message: Message):
    """Обработка показа всех слов"""
    # Здесь можно добавить логику получения всех слов из базы данных
    await bot.reply_to(message, "Список всех слов в словаре:")

async def handle_delete_word(call: CallbackQuery, word_id: str):
    """Обработка удаления слова"""
    await bot.answer_callback_query(call.id, "Слово удалено!")
    await bot.edit_message_text(
        "Слово удалено из словаря.",
        call.message.chat.id,
        call.message.message_id
    )

async def handle_edit_word(call: CallbackQuery, word_id: str):
    """Обработка редактирования слова"""
    await bot.answer_callback_query(call.id, "Редактирование слова...")
    await bot.send_message(call.message.chat.id, "Введите новое значение слова:")

async def handle_show_word(call: CallbackQuery, word_id: str):
    """Обработка показа слова"""
    await bot.answer_callback_query(call.id, "Показываю слово...")
    # Здесь можно добавить логику получения слова из базы данных
    await bot.send_message(call.message.chat.id, f"Информация о слове с ID: {word_id}")

# =============================================================================
# ПРИМЕР ИСПОЛЬЗОВАНИЯ ИНЛАЙН КНОПОК
# =============================================================================

@bot.message_handler(commands=['menu'])
async def show_menu(message: Message):
    """Показывает главное меню с кнопками"""
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("Добавить слово", callback_data="add_word"))
    keyboard.add(InlineKeyboardButton("Поиск слова", callback_data="search_word"))
    keyboard.add(InlineKeyboardButton("Список слов", callback_data="list_words"))
    keyboard.add(InlineKeyboardButton("Импорт CSV", callback_data="import_csv"))
    
    await bot.reply_to(message, "Выберите действие:", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data in ['add_word', 'search_word', 'list_words', 'import_csv'])
async def menu_callback_handler(call: CallbackQuery):
    """Обработчик callback запросов главного меню"""
    await bot.answer_callback_query(call.id)
    
    if call.data == 'add_word':
        await bot.send_message(call.message.chat.id, "Введите слово для добавления:")
    elif call.data == 'search_word':
        await bot.send_message(call.message.chat.id, "Введите слово для поиска:")
    elif call.data == 'list_words':
        await bot.send_message(call.message.chat.id, "Список всех слов в словаре:")
    elif call.data == 'import_csv':
        await bot.send_message(call.message.chat.id, "Отправьте CSV файл для импорта слов:")

# =============================================================================
# ПРИМЕР ОБРАБОТКИ ОШИБОК
# =============================================================================

@bot.message_handler(func=lambda message: True)
async def error_handler(message: Message):
    """Глобальный обработчик ошибок"""
    try:
        # Основная логика обработки
        pass
    except Exception as e:
        print(f"Ошибка при обработке сообщения: {e}")
        await bot.reply_to(message, "Произошла ошибка при обработке вашего сообщения. Попробуйте позже.")

# =============================================================================
# ЗАПУСК БОТА (если запускаете этот файл отдельно)
# =============================================================================

async def main():
    """Основная функция для запуска бота"""
    print("Бот запущен!")
    await bot.infinity_polling()

if __name__ == '__main__':
    asyncio.run(main())
