from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from config import SD_CD, CALLBACK_DATA

def sd_home_kb():
    keyboard = [[
        InlineKeyboardButton(text='Задачи', callback_data=SD_CD['tasks']),
        InlineKeyboardButton(text='Питание', callback_data=SD_CD['nutrition']),
        InlineKeyboardButton(text='🌅🌙 Рутины', callback_data=SD_CD['routines'])],
        [InlineKeyboardButton(text='📋 Правила', callback_data=SD_CD['rules']),
        InlineKeyboardButton(text='🏃‍♂️ Спорт', callback_data=SD_CD['sport']),
        InlineKeyboardButton(text='📖 Дневник', callback_data=SD_CD['diary'])],
        [InlineKeyboardButton(text='📅 Расписание', callback_data=SD_CD['schedule']),
        InlineKeyboardButton(text='📋 Тест правил', callback_data=SD_CD['rules_test']),
        InlineKeyboardButton(text='🔍 Анализ', callback_data=SD_CD['analysis'])],
        [InlineKeyboardButton(text='📊 График', callback_data=SD_CD['routines_chart']),
        InlineKeyboardButton(text='Назад', callback_data=CALLBACK_DATA['main_m'])]
    ]

    return InlineKeyboardMarkup(keyboard)

def tasks_w_kb():
    keyboard = [
        [InlineKeyboardButton(text='Добавить задачу', callback_data=SD_CD['add_task'])],
        [InlineKeyboardButton(text='Управление задачами', callback_data='manage_tasks')],
        [InlineKeyboardButton(text='День', callback_data=SD_CD['day'])],
        [InlineKeyboardButton(text='Месяц', callback_data=SD_CD['month'])],
        [InlineKeyboardButton(text='Год', callback_data=SD_CD['year'])],
        [InlineKeyboardButton(text='Назад', callback_data=CALLBACK_DATA['sd_home'])]
    ]

    return InlineKeyboardMarkup(keyboard)    

def edit_unsaved_task_kb():
    keyboard = [[InlineKeyboardButton(text='Сохранить задачу'),
                 InlineKeyboardButton(text='Редактировать задачу')],
                 [InlineKeyboardButton(text='В меню дисциплины', callback_data=CALLBACK_DATA['sd_home'])]]
    return InlineKeyboardMarkup(keyboard)

def task_management_kb(task_id):
    keyboard = [[
        InlineKeyboardButton(text='✅ Отметить выполненной', callback_data=f'mark_completed_{task_id}'),
        InlineKeyboardButton(text='✏️ Редактировать', callback_data=f'edit_task_{task_id}'),
        InlineKeyboardButton(text='🗑️ Удалить', callback_data=f'delete_task_{task_id}')],
        [InlineKeyboardButton(text='Назад к задачам', callback_data=CALLBACK_DATA['tasks'])]
    ]
    return InlineKeyboardMarkup(keyboard)

def tasks_list_kb(tasks):
    """Клавиатура со списком задач для выбора"""
    keyboard = []
    for task in tasks:
        status = "✅" if task.completed else "⭕"
        keyboard.append([InlineKeyboardButton(
            text=f"{status} {task.text[:30]}{'...' if len(task.text) > 30 else ''}", 
            callback_data=f'task_detail_{task.id}'
        )])
    keyboard.append([InlineKeyboardButton(text='Назад', callback_data=CALLBACK_DATA['tasks'])])
    return InlineKeyboardMarkup(keyboard)

# Клавиатуры для питания
def nutrition_home_kb():
    keyboard = [
        [InlineKeyboardButton(text='🍽️ Добавить приём пищи', callback_data=SD_CD['add_meal'])],
        [InlineKeyboardButton(text='📊 График', callback_data=SD_CD['nutrition_chart'])],
        [InlineKeyboardButton(text='📅 Просмотр по дате', callback_data='view_nutrition_date')],
        [InlineKeyboardButton(text='Назад', callback_data=CALLBACK_DATA['sd_home'])]
    ]
    return InlineKeyboardMarkup(keyboard)

def add_meal_kb():
    keyboard = [
        [InlineKeyboardButton(text='➕ Добавить блюдо', callback_data=SD_CD['add_dish'])],
        [InlineKeyboardButton(text='🔍 Найти блюда', callback_data=SD_CD['find_dishes'])],
        [InlineKeyboardButton(text='✅ Завершить приём пищи', callback_data=SD_CD['complete_meal'])],
        [InlineKeyboardButton(text='Назад', callback_data=SD_CD['nutrition'])]
    ]
    return InlineKeyboardMarkup(keyboard)

def add_another_dish_kb():
    keyboard = [
        [InlineKeyboardButton(text='Да, добавить ещё', callback_data=SD_CD['add_dish'])],
        [InlineKeyboardButton(text='Нет, достаточно', callback_data=SD_CD['complete_meal'])],
        [InlineKeyboardButton(text='Назад к приёму пищи', callback_data=SD_CD['add_meal'])]
    ]
    return InlineKeyboardMarkup(keyboard)

def nutrition_chart_kb():
    keyboard = [
        [InlineKeyboardButton(text='📋 Питание', callback_data=SD_CD['nutrition_menu'])],
        [InlineKeyboardButton(text='Назад', callback_data=SD_CD['nutrition'])]
    ]
    return InlineKeyboardMarkup(keyboard)

def nutrition_menu_kb():
    keyboard = [
        [InlineKeyboardButton(text='➕ Добавить правило', callback_data=SD_CD['add_rule'])],
        [InlineKeyboardButton(text='🎯 Добавить цель по питанию', callback_data=SD_CD['set_goals'])],
        [InlineKeyboardButton(text='📝 Добавить заметку по питанию', callback_data=SD_CD['add_note'])],
        [InlineKeyboardButton(text='Назад', callback_data=SD_CD['nutrition_chart'])]
    ]
    return InlineKeyboardMarkup(keyboard)

def set_goals_kb():
    keyboard = [
        [InlineKeyboardButton(text='🔥 Калории', callback_data=SD_CD['set_calories'])],
        [InlineKeyboardButton(text='🥩 Белок', callback_data=SD_CD['set_protein'])],
        [InlineKeyboardButton(text='Назад', callback_data=SD_CD['nutrition_menu'])]
    ]
    return InlineKeyboardMarkup(keyboard)

def dishes_list_kb(dishes):
    """Клавиатура со списком блюд"""
    keyboard = []
    for dish in dishes:
        keyboard.append([InlineKeyboardButton(
            text=f"{dish.id}. {dish.name} ({dish.calories_per_100g} ккал/100г)", 
            callback_data=f'select_dish_{dish.id}'
        )])
    keyboard.append([InlineKeyboardButton(text='Назад', callback_data=SD_CD['add_meal'])])
    return InlineKeyboardMarkup(keyboard)

def meal_summary_kb():
    keyboard = [
        [InlineKeyboardButton(text='✅ Завершить приём пищи', callback_data=SD_CD['complete_meal'])],
        [InlineKeyboardButton(text='➕ Добавить ещё блюдо', callback_data=SD_CD['add_dish'])],
        [InlineKeyboardButton(text='Назад к приёму пищи', callback_data=SD_CD['add_meal'])]
    ]
    return InlineKeyboardMarkup(keyboard)

# Клавиатуры для расписания
def schedule_home_kb():
    keyboard = [
        [InlineKeyboardButton(text='📅 Просмотр расписания', callback_data=SD_CD['schedule_view'])],
        [InlineKeyboardButton(text='➕ Добавить событие', callback_data=SD_CD['schedule_add'])],
        [InlineKeyboardButton(text='⚙️ Управление событиями', callback_data=SD_CD['schedule_manage'])],
        [InlineKeyboardButton(text='Назад', callback_data=CALLBACK_DATA['sd_home'])]
    ]
    return InlineKeyboardMarkup(keyboard)

def schedule_view_kb():
    keyboard = [
        [InlineKeyboardButton(text='📅 Сегодня', callback_data='schedule_today')],
        [InlineKeyboardButton(text='📅 Завтра', callback_data='schedule_tomorrow')],
        [InlineKeyboardButton(text='📅 Эта неделя', callback_data='schedule_week')],
        [InlineKeyboardButton(text='📅 Этот месяц', callback_data='schedule_month')],
        [InlineKeyboardButton(text='📅 Предстоящие', callback_data='schedule_upcoming')],
        [InlineKeyboardButton(text='Назад', callback_data=SD_CD['schedule'])]
    ]
    return InlineKeyboardMarkup(keyboard)

def schedule_events_list_kb(events):
    """Клавиатура со списком событий"""
    keyboard = []
    for event in events:
        status = "✅" if event.is_completed else "⭕"
        keyboard.append([InlineKeyboardButton(
            text=f"{status} {event.time} - {event.title[:25]}{'...' if len(event.title) > 25 else ''}", 
            callback_data=f'schedule_event_{event.id}'
        )])
    keyboard.append([InlineKeyboardButton(text='Назад', callback_data=SD_CD['schedule_view'])])
    return InlineKeyboardMarkup(keyboard)

def schedule_event_management_kb(event_id):
    """Клавиатура управления событием"""
    keyboard = [
        [InlineKeyboardButton(text='✅ Отметить выполненным', callback_data=f'schedule_complete_{event_id}'),
         InlineKeyboardButton(text='✏️ Редактировать', callback_data=f'schedule_edit_{event_id}')],
        [InlineKeyboardButton(text='🗑️ Удалить', callback_data=f'schedule_delete_{event_id}')],
        [InlineKeyboardButton(text='Назад к расписанию', callback_data=SD_CD['schedule_view'])]
    ]
    return InlineKeyboardMarkup(keyboard)

def schedule_manage_events_kb(events):
    """Клавиатура управления всеми событиями"""
    keyboard = []
    for event in events:
        status = "✅" if event.is_completed else "⭕"
        keyboard.append([InlineKeyboardButton(
            text=f"{status} {event.date} {event.time} - {event.title[:20]}{'...' if len(event.title) > 20 else ''}", 
            callback_data=f'schedule_manage_{event.id}'
        )])
    keyboard.append([InlineKeyboardButton(text='Назад', callback_data=SD_CD['schedule'])])
    return InlineKeyboardMarkup(keyboard)