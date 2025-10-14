"""
Обработчики для расписания
"""
from telegram import Update
from telegram.ext import ContextTypes
from keyboards.sd_k import (
    schedule_home_kb, schedule_view_kb, schedule_events_list_kb, 
    schedule_event_management_kb, schedule_manage_events_kb
)
from config import SD_MESSAGES, SD_CD, CALLBACK_DATA
from states import STATES
from models import (
    add_schedule_event, get_schedule_events_by_date, get_schedule_events_by_date_range,
    get_schedule_event_by_id, update_schedule_event, delete_schedule_event,
    get_upcoming_events, mark_schedule_event_completed, get_schedule_statistics
)
from datetime import datetime, date, timedelta


async def schedule_home(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Главное меню расписания"""
    query = update.callback_query
    await query.answer()
    
    text = SD_MESSAGES['schedule_home']
    markup = schedule_home_kb()
    
    await query.edit_message_text(text=text, reply_markup=markup)
    return STATES['schedule_home']


async def schedule_view_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Меню просмотра расписания"""
    query = update.callback_query
    await query.answer()
    
    text = SD_MESSAGES['schedule_view']
    markup = schedule_view_kb()
    
    await query.edit_message_text(text=text, reply_markup=markup)
    return STATES['schedule_view']


async def schedule_view_today(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Просмотр событий на сегодня"""
    query = update.callback_query
    await query.answer()
    
    chat_id = query.message.chat.id
    today = date.today().strftime('%Y-%m-%d')
    
    events = get_schedule_events_by_date(chat_id, today)
    
    if events:
        text = f"📅 События на сегодня ({today}):\n\n"
        for event in events:
            status = "✅" if event.is_completed else "⭕"
            text += f"{status} {event.time} - {event.title}\n"
            if event.description:
                text += f"   📝 {event.description}\n"
    else:
        text = SD_MESSAGES['no_events_today']
    
    markup = schedule_view_kb()
    await query.edit_message_text(text=text, reply_markup=markup)
    return STATES['schedule_view']


async def schedule_view_tomorrow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Просмотр событий на завтра"""
    query = update.callback_query
    await query.answer()
    
    chat_id = query.message.chat.id
    tomorrow = (date.today() + timedelta(days=1)).strftime('%Y-%m-%d')
    
    events = get_schedule_events_by_date(chat_id, tomorrow)
    
    if events:
        text = f"📅 События на завтра ({tomorrow}):\n\n"
        for event in events:
            status = "✅" if event.is_completed else "⭕"
            text += f"{status} {event.time} - {event.title}\n"
            if event.description:
                text += f"   📝 {event.description}\n"
    else:
        text = f"На завтра ({tomorrow}) событий нет."
    
    markup = schedule_view_kb()
    await query.edit_message_text(text=text, reply_markup=markup)
    return STATES['schedule_view']


async def schedule_view_week(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Просмотр событий на неделю"""
    query = update.callback_query
    await query.answer()
    
    chat_id = query.message.chat.id
    today = date.today()
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=6)
    
    events = get_schedule_events_by_date_range(chat_id, week_start.strftime('%Y-%m-%d'), week_end.strftime('%Y-%m-%d'))
    
    if events:
        text = f"📅 События на неделю ({week_start.strftime('%Y-%m-%d')} - {week_end.strftime('%Y-%m-%d')}):\n\n"
        current_date = None
        for event in events:
            if event.date != current_date:
                text += f"\n📅 {event.date}:\n"
                current_date = event.date
            status = "✅" if event.is_completed else "⭕"
            text += f"  {status} {event.time} - {event.title}\n"
    else:
        text = "На эту неделю событий нет."
    
    markup = schedule_view_kb()
    await query.edit_message_text(text=text, reply_markup=markup)
    return STATES['schedule_view']


async def schedule_view_month(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Просмотр событий на месяц"""
    query = update.callback_query
    await query.answer()
    
    chat_id = query.message.chat.id
    today = date.today()
    month_start = today.replace(day=1)
    if today.month == 12:
        month_end = today.replace(year=today.year + 1, month=1, day=1) - timedelta(days=1)
    else:
        month_end = today.replace(month=today.month + 1, day=1) - timedelta(days=1)
    
    events = get_schedule_events_by_date_range(chat_id, month_start.strftime('%Y-%m-%d'), month_end.strftime('%Y-%m-%d'))
    
    if events:
        text = f"📅 События на {today.strftime('%B %Y')}:\n\n"
        current_date = None
        for event in events:
            if event.date != current_date:
                text += f"\n📅 {event.date}:\n"
                current_date = event.date
            status = "✅" if event.is_completed else "⭕"
            text += f"  {status} {event.time} - {event.title}\n"
    else:
        text = f"На {today.strftime('%B %Y')} событий нет."
    
    markup = schedule_view_kb()
    await query.edit_message_text(text=text, reply_markup=markup)
    return STATES['schedule_view']


async def schedule_view_upcoming(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Просмотр предстоящих событий"""
    query = update.callback_query
    await query.answer()
    
    chat_id = query.message.chat.id
    events = get_upcoming_events(chat_id, limit=10)
    
    if events:
        text = "📅 Предстоящие события:\n\n"
        for event in events:
            status = "✅" if event.is_completed else "⭕"
            text += f"{status} {event.date} {event.time} - {event.title}\n"
            if event.description:
                text += f"   📝 {event.description}\n"
    else:
        text = "Предстоящих событий нет."
    
    markup = schedule_view_kb()
    await query.edit_message_text(text=text, reply_markup=markup)
    return STATES['schedule_view']


async def schedule_add_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Начало добавления события"""
    query = update.callback_query
    await query.answer()
    
    text = SD_MESSAGES['wait_schedule_title']
    await query.edit_message_text(text=text)
    return STATES['wait_schedule_title']


async def schedule_wait_title(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ожидание названия события"""
    title = update.message.text
    context.user_data['schedule_title'] = title
    
    text = SD_MESSAGES['wait_schedule_description']
    await update.message.reply_text(text)
    return STATES['wait_schedule_description']


async def schedule_wait_description(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ожидание описания события"""
    description = update.message.text
    if description.lower() in ['нет', 'no', '']:
        description = None
    context.user_data['schedule_description'] = description
    
    text = SD_MESSAGES['wait_schedule_date']
    await update.message.reply_text(text)
    return STATES['wait_schedule_date']


async def schedule_wait_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ожидание даты события"""
    try:
        event_date = update.message.text
        # Проверяем формат даты
        datetime.strptime(event_date, '%Y-%m-%d')
        context.user_data['schedule_date'] = event_date
        
        text = SD_MESSAGES['wait_schedule_time']
        await update.message.reply_text(text)
        return STATES['wait_schedule_time']
    except ValueError:
        text = "Неверный формат даты. Используйте формат YYYY-MM-DD (например: 2024-01-15)"
        await update.message.reply_text(text)
        return STATES['wait_schedule_date']


async def schedule_wait_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ожидание времени события"""
    try:
        event_time = update.message.text
        # Проверяем формат времени
        datetime.strptime(event_time, '%H:%M')
        
        chat_id = update.effective_chat.id
        title = context.user_data.pop('schedule_title')
        description = context.user_data.pop('schedule_description')
        date = context.user_data.pop('schedule_date')
        
        # Добавляем событие в базу данных
        event_id = add_schedule_event(chat_id, title, description, date, event_time)
        
        text = f"{SD_MESSAGES['schedule_event_created']}\n\n"
        text += f"📝 Название: {title}\n"
        if description:
            text += f"📄 Описание: {description}\n"
        text += f"📅 Дата: {date}\n"
        text += f"🕐 Время: {event_time}"
        
        markup = schedule_home_kb()
        await update.message.reply_text(text, reply_markup=markup)
        return STATES['schedule_home']
        
    except ValueError:
        text = "Неверный формат времени. Используйте формат HH:MM (например: 14:30)"
        await update.message.reply_text(text)
        return STATES['wait_schedule_time']


async def schedule_manage_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Начало управления событиями"""
    query = update.callback_query
    await query.answer()
    
    chat_id = query.message.chat.id
    
    # Получаем все события пользователя
    from models import Schedule
    from sqlalchemy.orm import Session
    from sqlalchemy import create_engine
    
    engine = create_engine('sqlite:///test.db')
    with Session(engine) as session:
        events = session.query(Schedule).filter(
            Schedule.chat_id == chat_id
        ).order_by(Schedule.date.desc(), Schedule.time.desc()).limit(20).all()
    
    if events:
        text = SD_MESSAGES['schedule_manage']
        markup = schedule_manage_events_kb(events)
    else:
        text = "У вас пока нет событий в расписании."
        markup = schedule_home_kb()
    
    await query.edit_message_text(text=text, reply_markup=markup)
    return STATES['schedule_manage']


async def schedule_event_detail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Детали события"""
    query = update.callback_query
    await query.answer()
    
    # Извлекаем ID события из callback_data
    event_id = int(query.data.split('_')[-1])
    chat_id = query.message.chat.id
    
    event = get_schedule_event_by_id(event_id, chat_id)
    
    if event:
        status = "✅ Выполнено" if event.is_completed else "⭕ Не выполнено"
        text = f"📅 Событие #{event.id}\n\n"
        text += f"📝 Название: {event.title}\n"
        if event.description:
            text += f"📄 Описание: {event.description}\n"
        text += f"📅 Дата: {event.date}\n"
        text += f"🕐 Время: {event.time}\n"
        text += f"📊 Статус: {status}\n"
        text += f"🕐 Создано: {event.created_at.strftime('%Y-%m-%d %H:%M')}\n"
        
        markup = schedule_event_management_kb(event_id)
    else:
        text = "Событие не найдено."
        markup = schedule_home_kb()
    
    await query.edit_message_text(text=text, reply_markup=markup)
    return STATES['schedule_manage']


async def schedule_mark_completed(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отметить событие как выполненное"""
    query = update.callback_query
    await query.answer()
    
    event_id = int(query.data.split('_')[-1])
    chat_id = query.message.chat.id
    
    success = mark_schedule_event_completed(event_id, chat_id)
    
    if success:
        text = SD_MESSAGES['schedule_event_completed']
    else:
        text = "Ошибка при обновлении события."
    
    markup = schedule_home_kb()
    await query.edit_message_text(text=text, reply_markup=markup)
    return STATES['schedule_home']


async def schedule_delete_event(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Удалить событие"""
    query = update.callback_query
    await query.answer()
    
    event_id = int(query.data.split('_')[-1])
    chat_id = query.message.chat.id
    
    event = get_schedule_event_by_id(event_id, chat_id)
    
    if event:
        success = delete_schedule_event(event_id, chat_id)
        if success:
            text = f"{SD_MESSAGES['schedule_event_deleted']}\n\nСобытие: {event.title}"
        else:
            text = "Ошибка при удалении события."
    else:
        text = "Событие не найдено."
    
    markup = schedule_home_kb()
    await query.edit_message_text(text=text, reply_markup=markup)
    return STATES['schedule_home']


async def schedule_edit_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Начало редактирования события"""
    query = update.callback_query
    await query.answer()
    
    event_id = int(query.data.split('_')[-1])
    chat_id = query.message.chat.id
    
    event = get_schedule_event_by_id(event_id, chat_id)
    
    if event:
        context.user_data['editing_event_id'] = event_id
        text = f"Редактирование события: {event.title}\n\nВведите новое название (или текущее для сохранения):"
        await query.edit_message_text(text=text)
        return STATES['schedule_edit']
    else:
        text = "Событие не найдено."
        markup = schedule_home_kb()
        await query.edit_message_text(text=text, reply_markup=markup)
        return STATES['schedule_home']


async def schedule_edit_title(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Редактирование названия события"""
    new_title = update.message.text
    event_id = context.user_data.get('editing_event_id')
    chat_id = update.effective_chat.id
    
    if event_id:
        success = update_schedule_event(event_id, chat_id, title=new_title)
        if success:
            text = f"{SD_MESSAGES['schedule_event_updated']}\n\nНовое название: {new_title}"
        else:
            text = "Ошибка при обновлении события."
    else:
        text = "Ошибка: ID события не найден."
    
    markup = schedule_home_kb()
    await update.message.reply_text(text, reply_markup=markup)
    return STATES['schedule_home']
