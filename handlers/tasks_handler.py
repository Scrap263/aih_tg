"""
Обработчики для стартовых команд и навигации
"""
from telegram import Update
from telegram.ext import ContextTypes
from keyboards import tasks_w_kb
from config import SD_MESSAGES, SD_CD, CALLBACK_DATA
from states import STATES
from models import Tasks
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from datetime import datetime, date
from keyboards.sd_k import edit_unsaved_task_kb, task_management_kb, tasks_list_kb


async def tasks_w(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    text = SD_MESSAGES['tasks_w']
    markup = tasks_w_kb()

    await query.edit_message_text(text=text, reply_markup=markup)
    return STATES['tasks_w']

async def add_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    text = 'Напишите задачу которую хотите добавить'
    await query.edit_message_text(text)
    return STATES['add_task']

async def wait_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    task_text = update.message.text
    context.user_data['task_text'] = task_text

    text = 'Введите дату задачи'

    await update.message.reply_text(text)
    return STATES['wait_date_for_task']

async def approve_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Сохранение задачи в базу данных"""
    task_date = update.message.text
    task_text = context.user_data.pop('task_text')

    try:
        # Создаем сессию для работы с базой данных
        engine = create_engine('sqlite:///test.db')
        with Session(engine) as session:
            # Создаем новую задачу
            new_task = Tasks(
                date=task_date,
                chat_id=update.effective_chat.id,
                text=task_text
            )
            session.add(new_task)
            session.commit()
            
        text = f"Задача успешно сохранена!\n\nТекст: {task_text}\nДата: {task_date}"
        markup = tasks_w_kb()
        await update.message.reply_text(text, reply_markup=markup)
        return STATES['tasks_w']
        
    except Exception as e:
        text = f"Ошибка при сохранении задачи: {str(e)}"
        markup = tasks_w_kb()
        await update.message.reply_text(text, reply_markup=markup)
        return STATES['tasks_w']


async def day_view(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Просмотр задач за день"""
    query = update.callback_query
    await query.answer()
    
    today = date.today().strftime('%Y-%m-%d')
    chat_id = query.message.chat.id
    
    try:
        engine = create_engine('sqlite:///test.db')
        with Session(engine) as session:
            tasks = session.query(Tasks).filter(
                Tasks.chat_id == chat_id,
                Tasks.date == today
            ).all()
            
        if tasks:
            text = f"Задачи на сегодня ({today}):\n\n"
            for i, task in enumerate(tasks, 1):
                status = "✅" if task.completed else "⭕"
                text += f"{i}. {status} {task.text}\n"
        else:
            text = f"На сегодня ({today}) задач нет."
            
        markup = tasks_w_kb()
        await query.edit_message_text(text, reply_markup=markup)
        return STATES['tasks_w']
        
    except Exception as e:
        text = f"Ошибка при получении задач: {str(e)}"
        markup = tasks_w_kb()
        await query.edit_message_text(text, reply_markup=markup)
        return STATES['tasks_w']


async def month_view(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Просмотр задач за месяц"""
    query = update.callback_query
    await query.answer()
    
    current_month = date.today().strftime('%Y-%m')
    chat_id = query.message.chat.id
    
    try:
        engine = create_engine('sqlite:///test.db')
        with Session(engine) as session:
            tasks = session.query(Tasks).filter(
                Tasks.chat_id == chat_id,
                Tasks.date.like(f'{current_month}%')
            ).order_by(Tasks.date).all()
            
        if tasks:
            text = f"Задачи за {current_month}:\n\n"
            current_date = None
            for task in tasks:
                task_date = task.date
                if task_date != current_date:
                    text += f"\n📅 {task_date}:\n"
                    current_date = task_date
                status = "✅" if task.completed else "⭕"
                text += f"• {status} {task.text}\n"
        else:
            text = f"За {current_month} задач нет."
            
        markup = tasks_w_kb()
        await query.edit_message_text(text, reply_markup=markup)
        return STATES['tasks_w']
        
    except Exception as e:
        text = f"Ошибка при получении задач: {str(e)}"
        markup = tasks_w_kb()
        await query.edit_message_text(text, reply_markup=markup)
        return STATES['tasks_w']


async def year_view(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Просмотр задач за год"""
    query = update.callback_query
    await query.answer()
    
    current_year = date.today().strftime('%Y')
    chat_id = query.message.chat.id
    
    try:
        engine = create_engine('sqlite:///test.db')
        with Session(engine) as session:
            tasks = session.query(Tasks).filter(
                Tasks.chat_id == chat_id,
                Tasks.date.like(f'{current_year}%')
            ).order_by(Tasks.date).all()
            
        if tasks:
            # Группируем задачи по месяцам
            months = {}
            for task in tasks:
                month = task.date[:7]  # YYYY-MM
                if month not in months:
                    months[month] = []
                months[month].append(task)
            
            text = f"Статистика за {current_year} год:\n\n"
            text += f"Всего задач: {len(tasks)}\n"
            text += f"Месяцев с задачами: {len(months)}\n\n"
            
            text += "Задачи по месяцам:\n"
            for month, month_tasks in months.items():
                text += f"\n📅 {month} ({len(month_tasks)} задач):\n"
                for task in month_tasks[:3]:  # Показываем только первые 3 задачи
                    status = "✅" if task.completed else "⭕"
                    text += f"• {status} {task.text}\n"
                if len(month_tasks) > 3:
                    text += f"... и еще {len(month_tasks) - 3} задач\n"
        else:
            text = f"За {current_year} год задач нет."
            
        markup = tasks_w_kb()
        await query.edit_message_text(text, reply_markup=markup)
        return STATES['tasks_w']
        
    except Exception as e:
        text = f"Ошибка при получении задач: {str(e)}"
        markup = tasks_w_kb()
        await query.edit_message_text(text, reply_markup=markup)
        return STATES['tasks_w']


async def show_tasks_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показать список всех задач для управления"""
    query = update.callback_query
    await query.answer()
    
    chat_id = query.message.chat.id
    
    try:
        engine = create_engine('sqlite:///test.db')
        with Session(engine) as session:
            tasks = session.query(Tasks).filter(
                Tasks.chat_id == chat_id
            ).order_by(Tasks.date.desc(), Tasks.created_at.desc()).limit(20).all()
            
        if tasks:
            text = "Выберите задачу для управления:\n\n"
            markup = tasks_list_kb(tasks)
        else:
            text = "У вас пока нет задач."
            markup = tasks_w_kb()
            
        await query.edit_message_text(text, reply_markup=markup)
        return STATES['tasks_w']
        
    except Exception as e:
        text = f"Ошибка при получении задач: {str(e)}"
        markup = tasks_w_kb()
        await query.edit_message_text(text, reply_markup=markup)
        return STATES['tasks_w']


async def show_task_detail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показать детали задачи и кнопки управления"""
    query = update.callback_query
    await query.answer()
    
    # Извлекаем ID задачи из callback_data
    task_id = int(query.data.split('_')[-1])
    chat_id = query.message.chat.id
    
    try:
        engine = create_engine('sqlite:///test.db')
        with Session(engine) as session:
            task = session.query(Tasks).filter(
                Tasks.id == task_id,
                Tasks.chat_id == chat_id
            ).first()
            
        if task:
            status = "✅ Выполнена" if task.completed else "⭕ Не выполнена"
            text = f"📋 Задача #{task.id}\n\n"
            text += f"📝 Текст: {task.text}\n"
            text += f"📅 Дата: {task.date}\n"
            text += f"📊 Статус: {status}\n"
            text += f"🕐 Создана: {task.created_at.strftime('%Y-%m-%d %H:%M')}\n"
            
            markup = task_management_kb(task_id)
        else:
            text = "Задача не найдена."
            markup = tasks_w_kb()
            
        await query.edit_message_text(text, reply_markup=markup)
        return STATES['tasks_w']
        
    except Exception as e:
        text = f"Ошибка при получении задачи: {str(e)}"
        markup = tasks_w_kb()
        await query.edit_message_text(text, reply_markup=markup)
        return STATES['tasks_w']


async def mark_task_completed(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отметить задачу как выполненную"""
    query = update.callback_query
    await query.answer()
    
    task_id = int(query.data.split('_')[-1])
    chat_id = query.message.chat.id
    
    try:
        engine = create_engine('sqlite:///test.db')
        with Session(engine) as session:
            task = session.query(Tasks).filter(
                Tasks.id == task_id,
                Tasks.chat_id == chat_id
            ).first()
            
            if task:
                task.completed = not task.completed  # Переключаем статус
                session.commit()
                status = "выполненной" if task.completed else "не выполненной"
                text = f"Задача отмечена как {status}!"
            else:
                text = "Задача не найдена."
                
        markup = tasks_w_kb()
        await query.edit_message_text(text, reply_markup=markup)
        return STATES['tasks_w']
        
    except Exception as e:
        text = f"Ошибка при обновлении задачи: {str(e)}"
        markup = tasks_w_kb()
        await query.edit_message_text(text, reply_markup=markup)
        return STATES['tasks_w']


async def delete_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Удалить задачу"""
    query = update.callback_query
    await query.answer()
    
    task_id = int(query.data.split('_')[-1])
    chat_id = query.message.chat.id
    
    try:
        engine = create_engine('sqlite:///test.db')
        with Session(engine) as session:
            task = session.query(Tasks).filter(
                Tasks.id == task_id,
                Tasks.chat_id == chat_id
            ).first()
            
            if task:
                task_text = task.text
                session.delete(task)
                session.commit()
                text = f"Задача '{task_text}' удалена!"
            else:
                text = "Задача не найдена."
                
        markup = tasks_w_kb()
        await query.edit_message_text(text, reply_markup=markup)
        return STATES['tasks_w']
        
    except Exception as e:
        text = f"Ошибка при удалении задачи: {str(e)}"
        markup = tasks_w_kb()
        await query.edit_message_text(text, reply_markup=markup)
        return STATES['tasks_w']