# Шпаргалка по декораторам в async PyTelegramBotAPI

## Основные декораторы

### 1. Обработка сообщений
```python
@bot.message_handler(commands=['start', 'help'])
async def start_handler(message):
    await bot.reply_to(message, "Привет!")

@bot.message_handler(content_types=['text'])
async def text_handler(message):
    await bot.reply_to(message, message.text)

@bot.message_handler(regexp=r'^[0-9]+$')
async def number_handler(message):
    await bot.reply_to(message, "Это число!")

@bot.message_handler(func=lambda msg: len(msg.text) > 10)
async def long_text_handler(message):
    await bot.reply_to(message, "Длинное сообщение!")
```

### 2. Обработка callback запросов
```python
@bot.callback_query_handler(func=lambda call: True)
async def callback_handler(call):
    await bot.answer_callback_query(call.id)
    await bot.send_message(call.message.chat.id, "Кнопка нажата!")
```

### 3. Обработка отредактированных сообщений
```python
@bot.edited_message_handler()
async def edited_handler(message):
    await bot.reply_to(message, "Сообщение отредактировано!")
```

### 4. Обработка inline запросов
```python
@bot.inline_handler(lambda query: len(query.query) > 0)
async def inline_handler(inline_query):
    results = []
    await bot.answer_inline_query(inline_query.id, results)
```

## Фильтры для message_handler

### content_types
```python
@bot.message_handler(content_types=['photo', 'video', 'document'])
async def media_handler(message):
    pass
```

### commands
```python
@bot.message_handler(commands=['start', 'help', 'menu'])
async def commands_handler(message):
    pass
```

### regexp
```python
@bot.message_handler(regexp=r'^[а-яё\s]+$')
async def russian_text_handler(message):
    pass
```

### chat_types
```python
@bot.message_handler(chat_types=['private', 'group'])
async def chat_handler(message):
    pass
```

### func (пользовательская функция)
```python
def is_admin(message):
    return message.from_user.id in [123456789, 987654321]

@bot.message_handler(func=is_admin)
async def admin_handler(message):
    pass
```

## Специальные декораторы

### Обработка опросов
```python
@bot.poll_handler()
async def poll_handler(poll):
    pass

@bot.poll_answer_handler()
async def poll_answer_handler(poll_answer):
    pass
```

### Обработка участников чата
```python
@bot.chat_member_handler()
async def chat_member_handler(chat_member_updated):
    pass

@bot.my_chat_member_handler()
async def my_chat_member_handler(chat_member_updated):
    pass
```

### Обработка запросов на присоединение
```python
@bot.chat_join_request_handler()
async def join_request_handler(chat_join_request):
    pass
```

### Обработка постов в каналах
```python
@bot.channel_post_handler()
async def channel_post_handler(message):
    pass

@bot.edited_channel_post_handler()
async def edited_channel_post_handler(message):
    pass
```

### Обработка платежей
```python
@bot.shipping_query_handler()
async def shipping_handler(shipping_query):
    pass

@bot.pre_checkout_query_handler()
async def checkout_handler(pre_checkout_query):
    pass
```

## Комбинирование декораторов

```python
@bot.message_handler(commands=['menu'])
@bot.message_handler(func=lambda msg: 'меню' in msg.text.lower())
async def menu_handler(message):
    pass
```

## Обработка ошибок

```python
@bot.message_handler(func=lambda message: True)
async def error_handler(message):
    try:
        # Ваша логика
        pass
    except Exception as e:
        print(f"Ошибка: {e}")
        await bot.reply_to(message, "Произошла ошибка!")
```

## Полезные советы

1. **Порядок декораторов важен** - более специфичные декораторы должны быть выше общих
2. **Используйте `await`** для всех асинхронных операций
3. **Обрабатывайте ошибки** в каждом хендлере
4. **Используйте типизацию** для лучшей читаемости кода
5. **Группируйте похожие хендлеры** в отдельные файлы
6. **Используйте `func` фильтр** для сложной логики
7. **Не забывайте про `bot.answer_callback_query()`** для callback запросов
