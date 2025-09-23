"""
Руководство по декораторам в async PyTelegramBotAPI

Этот файл содержит примеры всех основных декораторов и способов их использования
в асинхронной версии PyTelegramBotAPI.
"""

import asyncio
import re
from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

# Инициализация бота
bot = AsyncTeleBot('YOUR_BOT_TOKEN')

# =============================================================================
# 1. ОСНОВНЫЕ ДЕКОРАТОРЫ ДЛЯ СООБЩЕНИЙ
# =============================================================================

# @bot.message_handler - основной декоратор для обработки сообщений
@bot.message_handler(commands=['start', 'help'])
async def start_handler(message: Message):
    """Обработчик команд /start и /help"""
    await bot.reply_to(message, "Привет! Я бот-помощник. Используйте /menu для навигации.")

# Обработка текстовых сообщений с фильтрами
@bot.message_handler(content_types=['text'])
async def text_handler(message: Message):
    """Обработчик всех текстовых сообщений"""
    await bot.reply_to(message, f"Вы написали: {message.text}")

# Обработка документов и аудио
@bot.message_handler(content_types=['document', 'audio'])
async def media_handler(message: Message):
    """Обработчик документов и аудио"""
    if message.document:
        await bot.reply_to(message, f"Получен документ: {message.document.file_name}")
    elif message.audio:
        await bot.reply_to(message, f"Получено аудио: {message.audio.title or 'Без названия'}")

# Обработка с регулярными выражениями
@bot.message_handler(regexp=r'^[0-9]+$')
async def number_handler(message: Message):
    """Обработчик сообщений, содержащих только цифры"""
    await bot.reply_to(message, f"Вы ввели число: {message.text}")

# Обработка с пользовательской функцией
def is_long_message(message: Message) -> bool:
    """Проверяет, является ли сообщение длинным (более 50 символов)"""
    return len(message.text) > 50 if message.text else False

@bot.message_handler(func=is_long_message)
async def long_message_handler(message: Message):
    """Обработчик длинных сообщений"""
    await bot.reply_to(message, "Ваше сообщение довольно длинное!")

# Обработка по типу чата
@bot.message_handler(chat_types=['private'])
async def private_chat_handler(message: Message):
    """Обработчик только для приватных чатов"""
    await bot.reply_to(message, "Это приватный чат!")

# =============================================================================
# 2. ДЕКОРАТОРЫ ДЛЯ РАЗЛИЧНЫХ ТИПОВ ОБНОВЛЕНИЙ
# =============================================================================

# Обработка отредактированных сообщений
@bot.edited_message_handler()
async def edited_message_handler(message: Message):
    """Обработчик отредактированных сообщений"""
    await bot.reply_to(message, f"Сообщение было отредактировано: {message.text}")

# Обработка callback запросов (нажатия на inline кнопки)
@bot.callback_query_handler(func=lambda call: True)
async def callback_handler(call: CallbackQuery):
    """Обработчик всех callback запросов"""
    await bot.answer_callback_query(call.id, "Кнопка нажата!")
    
    if call.data == "button1":
        await bot.send_message(call.message.chat.id, "Нажата кнопка 1")
    elif call.data == "button2":
        await bot.send_message(call.message.chat.id, "Нажата кнопка 2")

# Обработка inline запросов
@bot.inline_handler(lambda query: len(query.query) > 0)
async def inline_query_handler(inline_query):
    """Обработчик inline запросов"""
    results = []
    # Создаем результаты для inline запроса
    results.append({
        'type': 'article',
        'id': '1',
        'title': f'Результат для "{inline_query.query}"',
        'message_text': f'Вы искали: {inline_query.query}'
    })
    
    await bot.answer_inline_query(inline_query.id, results)

# =============================================================================
# 3. ДЕКОРАТОРЫ ДЛЯ СПЕЦИАЛЬНЫХ ТИПОВ ОБНОВЛЕНИЙ
# =============================================================================

# Обработка опросов
@bot.poll_handler()
async def poll_handler(poll):
    """Обработчик опросов"""
    print(f"Получен опрос: {poll.question}")

# Обработка ответов на опросы
@bot.poll_answer_handler()
async def poll_answer_handler(poll_answer):
    """Обработчик ответов на опросы"""
    print(f"Пользователь {poll_answer.user.id} ответил на опрос")

# Обработка запросов на присоединение к чату
@bot.chat_join_request_handler()
async def chat_join_request_handler(chat_join_request):
    """Обработчик запросов на присоединение к чату"""
    await bot.approve_chat_join_request(chat_join_request.chat.id, chat_join_request.from_user.id)

# Обработка изменений статуса участников чата
@bot.chat_member_handler()
async def chat_member_handler(chat_member_updated):
    """Обработчик изменений статуса участников чата"""
    print(f"Статус участника изменен в чате {chat_member_updated.chat.id}")

# Обработка изменений статуса бота в чате
@bot.my_chat_member_handler()
async def my_chat_member_handler(chat_member_updated):
    """Обработчик изменений статуса бота в чате"""
    print(f"Статус бота изменен в чате {chat_member_updated.chat.id}")

# =============================================================================
# 4. ДЕКОРАТОРЫ ДЛЯ КАНАЛОВ
# =============================================================================

# Обработка постов в каналах
@bot.channel_post_handler()
async def channel_post_handler(message: Message):
    """Обработчик постов в каналах"""
    print(f"Новый пост в канале: {message.text}")

# Обработка отредактированных постов в каналах
@bot.edited_channel_post_handler()
async def edited_channel_post_handler(message: Message):
    """Обработчик отредактированных постов в каналах"""
    print(f"Пост в канале отредактирован: {message.text}")

# =============================================================================
# 5. ДЕКОРАТОРЫ ДЛЯ ПЛАТЕЖЕЙ И ТОРГОВЛИ
# =============================================================================

# Обработка запросов на доставку
@bot.shipping_query_handler()
async def shipping_query_handler(shipping_query):
    """Обработчик запросов на доставку"""
    await bot.answer_shipping_query(shipping_query.id, ok=True)

# Обработка pre-checkout запросов
@bot.pre_checkout_query_handler()
async def pre_checkout_query_handler(pre_checkout_query):
    """Обработчик pre-checkout запросов"""
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

# =============================================================================
# 6. КОМБИНИРОВАНИЕ ДЕКОРАТОРОВ
# =============================================================================

# Можно использовать несколько декораторов для одной функции
@bot.message_handler(commands=['menu'])
@bot.message_handler(func=lambda msg: msg.text and 'меню' in msg.text.lower())
async def menu_handler(message: Message):
    """Обработчик команды /menu и сообщений со словом 'меню'"""
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("Кнопка 1", callback_data="button1"))
    keyboard.add(InlineKeyboardButton("Кнопка 2", callback_data="button2"))
    
    await bot.reply_to(message, "Выберите опцию:", reply_markup=keyboard)

# =============================================================================
# 7. ПРОДВИНУТЫЕ ПРИМЕРЫ С ФИЛЬТРАМИ
# =============================================================================

# Обработка сообщений от конкретного пользователя
def is_from_admin(message: Message) -> bool:
    """Проверяет, является ли отправитель администратором"""
    admin_ids = [123456789, 987654321]  # ID администраторов
    return message.from_user.id in admin_ids

@bot.message_handler(func=is_from_admin)
async def admin_handler(message: Message):
    """Обработчик сообщений от администраторов"""
    await bot.reply_to(message, "Привет, администратор!")

# Обработка сообщений с определенными типами контента
@bot.message_handler(content_types=['photo'])
async def photo_handler(message: Message):
    """Обработчик фотографий"""
    await bot.reply_to(message, "Красивое фото!")

@bot.message_handler(content_types=['video'])
async def video_handler(message: Message):
    """Обработчик видео"""
    await bot.reply_to(message, "Интересное видео!")

# Обработка сообщений с геолокацией
@bot.message_handler(content_types=['location'])
async def location_handler(message: Message):
    """Обработчик геолокации"""
    lat = message.location.latitude
    lon = message.location.longitude
    await bot.reply_to(message, f"Ваши координаты: {lat}, {lon}")

# =============================================================================
# 8. ОБРАБОТКА ОШИБОК И ИСКЛЮЧЕНИЙ
# =============================================================================

# Глобальный обработчик ошибок
@bot.message_handler(func=lambda message: True)
async def error_handler(message: Message):
    """Глобальный обработчик для всех сообщений"""
    try:
        # Ваша логика обработки
        pass
    except Exception as e:
        print(f"Ошибка при обработке сообщения: {e}")
        await bot.reply_to(message, "Произошла ошибка при обработке вашего сообщения.")

# =============================================================================
# 9. ЗАПУСК БОТА
# =============================================================================

async def main():
    """Основная функция для запуска бота"""
    print("Бот запущен!")
    await bot.infinity_polling()

if __name__ == '__main__':
    asyncio.run(main())
