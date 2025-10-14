"""
Обработчики для работы с правилами
"""
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from models import add_rule, get_rules, get_rule_by_id, update_rule, delete_rule, toggle_rule_status
from datetime import time
from zoneinfo import ZoneInfo
from keyboards.keyboards import (
    get_rules_menu_keyboard, get_rules_list_keyboard, get_rule_detail_keyboard,
    get_edit_rule_keyboard, get_reminder_keyboard, get_confirm_delete_keyboard,
    get_skip_reminder_keyboard
)
from states import STATES


async def send_rule_reminder(context: ContextTypes.DEFAULT_TYPE):
    """Отправка напоминания о правиле"""
    chat_id = context.job.data['chat_id']
    rule_id = context.job.data['rule_id']
    
    rule = get_rule_by_id(rule_id)
    if rule and rule.is_active:
        text = f"⏰ <b>Напоминание о правиле</b>\n\n"
        text += f"📝 <b>Правило:</b> {rule.rule_text}\n"
        text += f"⏰ <b>Время:</b> {rule.reminder_time}\n\n"
        text += "Не забудьте следовать этому правилу!"
        
        await context.bot.send_message(
            chat_id=chat_id,
            text=text,
            parse_mode=ParseMode.HTML
        )


async def schedule_rule_reminder(chat_id, rule_id, reminder_time, job_queue):
    """Планирование напоминания для правила"""
    if not reminder_time:
        return
    
    try:
        # Парсим время (формат: "08:00")
        hour, minute = map(int, reminder_time.split(':'))
        target_time = time(hour=hour, minute=minute, tzinfo=ZoneInfo('Europe/Moscow'))
        
        # Создаем уникальное имя для задачи
        job_name = f"rule_reminder_{rule_id}_{chat_id}"
        
        # Удаляем существующую задачу, если есть
        existing_jobs = job_queue.get_jobs_by_name(job_name)
        for job in existing_jobs:
            job.schedule_removal()
        
        # Создаем новую задачу
        job_queue.run_daily(
            send_rule_reminder,
            target_time,
            data={'chat_id': chat_id, 'rule_id': rule_id},
            name=job_name
        )
    except Exception as e:
        print(f"Ошибка при планировании напоминания: {e}")


async def rules_home(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Главное меню правил"""
    query = update.callback_query
    await query.answer()
    
    text = "📋 <b>Управление правилами</b>\n\n"
    text += "Здесь вы можете создавать и управлять своими правилами.\n"
    text += "Правила помогают вам следовать определенным принципам и привычкам."
    
    await query.edit_message_text(
        text=text,
        parse_mode=ParseMode.HTML,
        reply_markup=get_rules_menu_keyboard()
    )
    return STATES['rules_home']


async def view_rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Просмотр списка правил"""
    query = update.callback_query
    await query.answer()
    
    chat_id = update.effective_user.id
    rules = get_rules(chat_id, active_only=False)
    
    if not rules:
        text = "📋 <b>Мои правила</b>\n\n"
        text += "У вас пока нет правил.\n"
        text += "Добавьте первое правило, чтобы начать!"
        
        keyboard = get_rules_menu_keyboard()
    else:
        text = "📋 <b>Мои правила</b>\n\n"
        text += f"Всего правил: {len(rules)}\n"
        text += f"Активных: {len([r for r in rules if r.is_active])}\n\n"
        text += "Выберите правило для просмотра:"
        
        keyboard = get_rules_list_keyboard(rules)
    
    await query.edit_message_text(
        text=text,
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard
    )
    return STATES['view_rules']


async def add_rule_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Начало добавления правила"""
    query = update.callback_query
    await query.answer()
    
    text = "➕ <b>Добавление нового правила</b>\n\n"
    text += "Напишите текст вашего правила.\n"
    text += "Например: \"Пить 2 литра воды в день\" или \"Делать зарядку каждое утро\""
    
    await query.edit_message_text(
        text=text,
        parse_mode=ParseMode.HTML,
        reply_markup=get_skip_reminder_keyboard()
    )
    return STATES['add_rule_text']


async def add_rule_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка текста правила"""
    rule_text = update.message.text.strip()
    
    if len(rule_text) < 3:
        await update.message.reply_text(
            "❌ Текст правила слишком короткий. Минимум 3 символа."
        )
        return STATES['add_rule_text']
    
    if len(rule_text) > 500:
        await update.message.reply_text(
            "❌ Текст правила слишком длинный. Максимум 500 символов."
        )
        return STATES['add_rule_text']
    
    # Сохраняем текст правила в контексте
    context.user_data['new_rule_text'] = rule_text
    
    text = "⏰ <b>Настройка напоминания</b>\n\n"
    text += f"Правило: <i>{rule_text}</i>\n\n"
    text += "Хотите настроить напоминание для этого правила?"
    
    await update.message.reply_text(
        text=text,
        parse_mode=ParseMode.HTML,
        reply_markup=get_reminder_keyboard()
    )
    return STATES['add_rule_reminder']


async def add_rule_reminder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка настройки напоминания"""
    query = update.callback_query
    await query.answer()
    
    chat_id = update.effective_user.id
    rule_text = context.user_data.get('new_rule_text')
    
    if not rule_text:
        await query.edit_message_text(
            "❌ Ошибка: текст правила не найден. Попробуйте снова.",
            reply_markup=get_rules_menu_keyboard()
        )
        return STATES['rules_home']
    
    # Определяем время напоминания
    reminder_time = None
    if query.data == 'reminder_morning':
        reminder_time = "08:00"
    elif query.data == 'reminder_afternoon':
        reminder_time = "12:00"
    elif query.data == 'reminder_evening':
        reminder_time = "18:00"
    elif query.data == 'reminder_night':
        reminder_time = "22:00"
    elif query.data == 'no_reminder':
        reminder_time = None
    elif query.data == 'skip_reminder':
        reminder_time = None
    
    # Создаем правило
    rule_id = add_rule(chat_id, rule_text, reminder_time)
    
    # Планируем напоминание, если указано время
    if reminder_time:
        job_queue = context.job_queue or context.application.job_queue
        if job_queue:
            await schedule_rule_reminder(chat_id, rule_id, reminder_time, job_queue)
    
    # Очищаем контекст
    context.user_data.pop('new_rule_text', None)
    
    text = "✅ <b>Правило добавлено!</b>\n\n"
    text += f"📝 <b>Текст:</b> {rule_text}\n"
    if reminder_time:
        text += f"⏰ <b>Напоминание:</b> {reminder_time}\n"
    else:
        text += "⏰ <b>Напоминание:</b> Не настроено\n"
    
    await query.edit_message_text(
        text=text,
        parse_mode=ParseMode.HTML,
        reply_markup=get_rules_menu_keyboard()
    )
    return STATES['rules_home']


async def rule_detail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Детальный просмотр правила"""
    query = update.callback_query
    await query.answer()
    
    # Извлекаем ID правила из callback_data
    rule_id = int(query.data.split('_')[-1])
    rule = get_rule_by_id(rule_id)
    
    if not rule:
        await query.edit_message_text(
            "❌ Правило не найдено.",
            reply_markup=get_rules_menu_keyboard()
        )
        return STATES['rules_home']
    
    status = "✅ Активно" if rule.is_active else "❌ Неактивно"
    
    text = f"📋 <b>Правило #{rule.id}</b>\n\n"
    text += f"📝 <b>Текст:</b> {rule.rule_text}\n"
    text += f"📊 <b>Статус:</b> {status}\n"
    if rule.reminder_time:
        text += f"⏰ <b>Напоминание:</b> {rule.reminder_time}\n"
    else:
        text += "⏰ <b>Напоминание:</b> Не настроено\n"
    text += f"📅 <b>Создано:</b> {rule.created_at.strftime('%d.%m.%Y %H:%M')}\n"
    if rule.updated_at != rule.created_at:
        text += f"🔄 <b>Обновлено:</b> {rule.updated_at.strftime('%d.%m.%Y %H:%M')}"
    
    await query.edit_message_text(
        text=text,
        parse_mode=ParseMode.HTML,
        reply_markup=get_rule_detail_keyboard(rule_id)
    )
    return STATES['edit_rule']


async def edit_rule_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Начало редактирования правила"""
    query = update.callback_query
    await query.answer()
    
    # Извлекаем ID правила из callback_data
    rule_id = int(query.data.split('_')[-1])
    rule = get_rule_by_id(rule_id)
    
    if not rule:
        await query.edit_message_text(
            "❌ Правило не найдено.",
            reply_markup=get_rules_menu_keyboard()
        )
        return STATES['rules_home']
    
    text = f"✏️ <b>Редактирование правила #{rule.id}</b>\n\n"
    text += f"📝 <b>Текущий текст:</b> {rule.rule_text}\n\n"
    text += "Выберите, что хотите изменить:"
    
    await query.edit_message_text(
        text=text,
        parse_mode=ParseMode.HTML,
        reply_markup=get_edit_rule_keyboard(rule_id)
    )
    return STATES['edit_rule']


async def edit_rule_text_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Начало редактирования текста правила"""
    query = update.callback_query
    await query.answer()
    
    # Извлекаем ID правила из callback_data
    rule_id = int(query.data.split('_')[-1])
    rule = get_rule_by_id(rule_id)
    
    if not rule:
        await query.edit_message_text(
            "❌ Правило не найдено.",
            reply_markup=get_rules_menu_keyboard()
        )
        return STATES['rules_home']
    
    # Сохраняем ID правила в контексте
    context.user_data['editing_rule_id'] = rule_id
    
    text = "📝 <b>Изменение текста правила</b>\n\n"
    text += f"Текущий текст: <i>{rule.rule_text}</i>\n\n"
    text += "Напишите новый текст правила:"
    
    await query.edit_message_text(
        text=text,
        parse_mode=ParseMode.HTML
    )
    return STATES['edit_rule_text']


async def edit_rule_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка изменения текста правила"""
    new_text = update.message.text.strip()
    rule_id = context.user_data.get('editing_rule_id')
    
    if not rule_id:
        await update.message.reply_text(
            "❌ Ошибка: ID правила не найден. Попробуйте снова.",
            reply_markup=get_rules_menu_keyboard()
        )
        return STATES['rules_home']
    
    if len(new_text) < 3:
        await update.message.reply_text(
            "❌ Текст правила слишком короткий. Минимум 3 символа."
        )
        return STATES['edit_rule_text']
    
    if len(new_text) > 500:
        await update.message.reply_text(
            "❌ Текст правила слишком длинный. Максимум 500 символов."
        )
        return STATES['edit_rule_text']
    
    # Обновляем правило
    success = update_rule(rule_id, rule_text=new_text)
    
    if success:
        # Очищаем контекст
        context.user_data.pop('editing_rule_id', None)
        
        text = "✅ <b>Текст правила обновлен!</b>\n\n"
        text += f"📝 <b>Новый текст:</b> {new_text}"
        
        await update.message.reply_text(
            text=text,
            parse_mode=ParseMode.HTML,
            reply_markup=get_rule_detail_keyboard(rule_id)
        )
        return STATES['edit_rule']
    else:
        await update.message.reply_text(
            "❌ Ошибка при обновлении правила.",
            reply_markup=get_rules_menu_keyboard()
        )
        return STATES['rules_home']


async def edit_rule_reminder_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Начало редактирования напоминания"""
    query = update.callback_query
    await query.answer()
    
    # Извлекаем ID правила из callback_data
    rule_id = int(query.data.split('_')[-1])
    rule = get_rule_by_id(rule_id)
    
    if not rule:
        await query.edit_message_text(
            "❌ Правило не найдено.",
            reply_markup=get_rules_menu_keyboard()
        )
        return STATES['rules_home']
    
    # Сохраняем ID правила в контексте
    context.user_data['editing_rule_id'] = rule_id
    
    text = "⏰ <b>Изменение напоминания</b>\n\n"
    text += f"Правило: <i>{rule.rule_text}</i>\n"
    if rule.reminder_time:
        text += f"Текущее напоминание: <b>{rule.reminder_time}</b>\n\n"
    else:
        text += "Текущее напоминание: <b>Не настроено</b>\n\n"
    text += "Выберите новое время напоминания:"
    
    await query.edit_message_text(
        text=text,
        parse_mode=ParseMode.HTML,
        reply_markup=get_reminder_keyboard()
    )
    return STATES['edit_rule_reminder']


async def edit_rule_reminder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка изменения напоминания"""
    query = update.callback_query
    await query.answer()
    
    rule_id = context.user_data.get('editing_rule_id')
    
    if not rule_id:
        await query.edit_message_text(
            "❌ Ошибка: ID правила не найден. Попробуйте снова.",
            reply_markup=get_rules_menu_keyboard()
        )
        return STATES['rules_home']
    
    # Определяем время напоминания
    reminder_time = None
    if query.data == 'reminder_morning':
        reminder_time = "08:00"
    elif query.data == 'reminder_afternoon':
        reminder_time = "12:00"
    elif query.data == 'reminder_evening':
        reminder_time = "18:00"
    elif query.data == 'reminder_night':
        reminder_time = "22:00"
    elif query.data == 'no_reminder':
        reminder_time = None
    
    # Обновляем правило
    success = update_rule(rule_id, reminder_time=reminder_time)
    
    if success:
        # Планируем новое напоминание
        job_queue = context.job_queue or context.application.job_queue
        if job_queue:
            chat_id = update.effective_user.id
            await schedule_rule_reminder(chat_id, rule_id, reminder_time, job_queue)
        
        # Очищаем контекст
        context.user_data.pop('editing_rule_id', None)
        
        text = "✅ <b>Напоминание обновлено!</b>\n\n"
        if reminder_time:
            text += f"⏰ <b>Новое напоминание:</b> {reminder_time}"
        else:
            text += "⏰ <b>Напоминание:</b> Отключено"
        
        await query.edit_message_text(
            text=text,
            parse_mode=ParseMode.HTML,
            reply_markup=get_rule_detail_keyboard(rule_id)
        )
        return STATES['edit_rule']
    else:
        await query.edit_message_text(
            "❌ Ошибка при обновлении напоминания.",
            reply_markup=get_rules_menu_keyboard()
        )
        return STATES['rules_home']


async def toggle_rule(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Переключение статуса правила"""
    query = update.callback_query
    await query.answer()
    
    # Извлекаем ID правила из callback_data
    rule_id = int(query.data.split('_')[-1])
    
    new_status = toggle_rule_status(rule_id)
    
    if new_status is not None:
        # Управляем напоминаниями в зависимости от статуса
        job_queue = context.job_queue or context.application.job_queue
        if job_queue:
            chat_id = update.effective_user.id
            if not new_status:
                # Если правило деактивировано, отменяем напоминание
                job_name = f"rule_reminder_{rule_id}_{chat_id}"
                existing_jobs = job_queue.get_jobs_by_name(job_name)
                for job in existing_jobs:
                    job.schedule_removal()
            else:
                # Если правило активировано, восстанавливаем напоминание
                rule = get_rule_by_id(rule_id)
                if rule and rule.reminder_time:
                    await schedule_rule_reminder(chat_id, rule_id, rule.reminder_time, job_queue)
        
        status_text = "активно" if new_status else "неактивно"
        text = f"✅ <b>Правило теперь {status_text}!</b>"
        
        await query.edit_message_text(
            text=text,
            parse_mode=ParseMode.HTML,
            reply_markup=get_rule_detail_keyboard(rule_id)
        )
        return STATES['edit_rule']
    else:
        await query.edit_message_text(
            "❌ Ошибка при изменении статуса правила.",
            reply_markup=get_rules_menu_keyboard()
        )
        return STATES['rules_home']


async def delete_rule_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Начало удаления правила"""
    query = update.callback_query
    await query.answer()
    
    # Извлекаем ID правила из callback_data
    rule_id = int(query.data.split('_')[-1])
    rule = get_rule_by_id(rule_id)
    
    if not rule:
        await query.edit_message_text(
            "❌ Правило не найдено.",
            reply_markup=get_rules_menu_keyboard()
        )
        return STATES['rules_home']
    
    text = "🗑️ <b>Удаление правила</b>\n\n"
    text += f"Вы уверены, что хотите удалить это правило?\n\n"
    text += f"📝 <b>Текст:</b> {rule.rule_text}\n"
    text += f"📅 <b>Создано:</b> {rule.created_at.strftime('%d.%m.%Y %H:%M')}\n\n"
    text += "⚠️ <b>Это действие нельзя отменить!</b>"
    
    await query.edit_message_text(
        text=text,
        parse_mode=ParseMode.HTML,
        reply_markup=get_confirm_delete_keyboard(rule_id)
    )
    return STATES['delete_rule_confirm']


async def delete_rule_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Подтверждение удаления правила"""
    query = update.callback_query
    await query.answer()
    
    # Извлекаем ID правила из callback_data
    rule_id = int(query.data.split('_')[-1])
    
    success = delete_rule(rule_id)
    
    if success:
        # Отменяем напоминание для удаленного правила
        job_queue = context.job_queue or context.application.job_queue
        if job_queue:
            chat_id = update.effective_user.id
            job_name = f"rule_reminder_{rule_id}_{chat_id}"
            existing_jobs = job_queue.get_jobs_by_name(job_name)
            for job in existing_jobs:
                job.schedule_removal()
        
        text = "✅ <b>Правило удалено!</b>\n\n"
        text += "Правило было успешно удалено из вашего списка."
        
        await query.edit_message_text(
            text=text,
            parse_mode=ParseMode.HTML,
            reply_markup=get_rules_menu_keyboard()
        )
        return STATES['rules_home']
    else:
        await query.edit_message_text(
            "❌ Ошибка при удалении правила.",
            reply_markup=get_rules_menu_keyboard()
        )
        return STATES['rules_home']


async def skip_reminder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Пропуск настройки напоминания"""
    query = update.callback_query
    await query.answer()
    
    chat_id = update.effective_user.id
    rule_text = context.user_data.get('new_rule_text')
    
    if not rule_text:
        await query.edit_message_text(
            "❌ Ошибка: текст правила не найден. Попробуйте снова.",
            reply_markup=get_rules_menu_keyboard()
        )
        return STATES['rules_home']
    
    # Создаем правило без напоминания
    rule_id = add_rule(chat_id, rule_text, None)
    
    # Очищаем контекст
    context.user_data.pop('new_rule_text', None)
    
    text = "✅ <b>Правило добавлено!</b>\n\n"
    text += f"📝 <b>Текст:</b> {rule_text}\n"
    text += "⏰ <b>Напоминание:</b> Не настроено"
    
    await query.edit_message_text(
        text=text,
        parse_mode=ParseMode.HTML,
        reply_markup=get_rules_menu_keyboard()
    )
    return STATES['rules_home']
