"""
Клавиатуры для Telegram бота
"""
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from config import CALLBACK_DATA


def get_main_menu_keyboard():
    """Главное меню"""
    keyboard = [[
        InlineKeyboardButton(text='Словарь', callback_data=CALLBACK_DATA['dict_main']),
        InlineKeyboardButton(text='Инструкция', callback_data=CALLBACK_DATA['instructions']),
        InlineKeyboardButton(text='Дисциплина', callback_data=CALLBACK_DATA['sd_home'])
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

def get_home_button():
    keyboard = [[InlineKeyboardButton('Домой', callback_data=CALLBACK_DATA['main_m'])]]
    return InlineKeyboardMarkup(keyboard)

# Клавиатуры для рутин
def get_routines_menu_keyboard():
    """Меню рутин"""
    keyboard = [
        [InlineKeyboardButton('🌅 Утренняя рутина', callback_data='morning_routine')],
        [InlineKeyboardButton('🌙 Вечерняя рутина', callback_data='evening_routine')],
        [InlineKeyboardButton('📊 График', callback_data='routines_chart')],
        [InlineKeyboardButton('Назад', callback_data=CALLBACK_DATA['sd_home'])]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_morning_routine_keyboard():
    """Клавиатура утренней рутины"""
    keyboard = [
        [InlineKeyboardButton('🚀 Начать утреннюю рутину', callback_data='start_morning_routine')],
        [InlineKeyboardButton('⚙️ Настроить рутину', callback_data='setup_morning_routine')],
        [InlineKeyboardButton('📋 Мои рутины', callback_data='my_morning_routines')],
        [InlineKeyboardButton('Назад', callback_data='routines_menu')]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_evening_routine_keyboard():
    """Клавиатура вечерней рутины"""
    keyboard = [
        [InlineKeyboardButton('🌙 Начать вечернюю рутину', callback_data='start_evening_routine')],
        [InlineKeyboardButton('⚙️ Настроить рутину', callback_data='setup_evening_routine')],
        [InlineKeyboardButton('📋 Мои рутины', callback_data='my_evening_routines')],
        [InlineKeyboardButton('Назад', callback_data='routines_menu')]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_routine_setup_keyboard(routine_type):
    """Клавиатура настройки рутины"""
    keyboard = [
        [InlineKeyboardButton('➕ Создать новую рутину', callback_data=f'create_{routine_type}_routine')],
        [InlineKeyboardButton('✏️ Редактировать рутину', callback_data=f'edit_{routine_type}_routine')],
        [InlineKeyboardButton('🗑️ Удалить рутину', callback_data=f'delete_{routine_type}_routine')],
        [InlineKeyboardButton('Назад', callback_data=f'{routine_type}_routine')]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_routine_actions_keyboard(actions, current_index=0):
    """Клавиатура для выполнения действий рутины"""
    keyboard = []
    if current_index < len(actions):
        keyboard.append([InlineKeyboardButton('✅ Выполнил', callback_data='action_completed')])
        keyboard.append([InlineKeyboardButton('⏭️ Пропустить', callback_data='skip_action')])
    else:
        keyboard.append([InlineKeyboardButton('🎉 Завершить рутину', callback_data='complete_routine')])
    
    keyboard.append([InlineKeyboardButton('❌ Отменить', callback_data='cancel_routine')])
    return InlineKeyboardMarkup(keyboard)

def get_morning_testing_keyboard():
    """Клавиатура для утреннего тестирования"""
    keyboard = [
        [InlineKeyboardButton('1', callback_data='health_1'), InlineKeyboardButton('2', callback_data='health_2'), 
         InlineKeyboardButton('3', callback_data='health_3'), InlineKeyboardButton('4', callback_data='health_4'), 
         InlineKeyboardButton('5', callback_data='health_5')],
        [InlineKeyboardButton('6', callback_data='health_6'), InlineKeyboardButton('7', callback_data='health_7'), 
         InlineKeyboardButton('8', callback_data='health_8'), InlineKeyboardButton('9', callback_data='health_9'), 
         InlineKeyboardButton('10', callback_data='health_10')]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_muscle_fatigue_keyboard():
    """Клавиатура для оценки мышечной усталости"""
    keyboard = [
        [InlineKeyboardButton('1', callback_data='fatigue_1'), InlineKeyboardButton('2', callback_data='fatigue_2'), 
         InlineKeyboardButton('3', callback_data='fatigue_3'), InlineKeyboardButton('4', callback_data='fatigue_4'), 
         InlineKeyboardButton('5', callback_data='fatigue_5')],
        [InlineKeyboardButton('6', callback_data='fatigue_6'), InlineKeyboardButton('7', callback_data='fatigue_7'), 
         InlineKeyboardButton('8', callback_data='fatigue_8'), InlineKeyboardButton('9', callback_data='fatigue_9'), 
         InlineKeyboardButton('10', callback_data='fatigue_10')]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_routines_list_keyboard(routines, routine_type):
    """Клавиатура со списком рутин"""
    keyboard = []
    for routine in routines:
        keyboard.append([InlineKeyboardButton(
            f"📋 {routine.name}", 
            callback_data=f'select_{routine_type}_routine_{routine.id}'
        )])
    keyboard.append([InlineKeyboardButton('Назад', callback_data=f'{routine_type}_routine')])
    return InlineKeyboardMarkup(keyboard)

# Клавиатуры для правил
def get_rules_menu_keyboard():
    """Меню правил"""
    keyboard = [
        [InlineKeyboardButton('📋 Мои правила', callback_data='view_rules')],
        [InlineKeyboardButton('➕ Добавить правило', callback_data='add_rule')],
        [InlineKeyboardButton('Назад', callback_data=CALLBACK_DATA['sd_home'])]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_rules_list_keyboard(rules):
    """Клавиатура со списком правил"""
    keyboard = []
    for rule in rules:
        status = "✅" if rule.is_active else "❌"
        keyboard.append([InlineKeyboardButton(
            f"{status} {rule.rule_text[:30]}{'...' if len(rule.rule_text) > 30 else ''}", 
            callback_data=f'rule_detail_{rule.id}'
        )])
    keyboard.append([InlineKeyboardButton('➕ Добавить правило', callback_data='add_rule')])
    keyboard.append([InlineKeyboardButton('Назад', callback_data='rules_home')])
    return InlineKeyboardMarkup(keyboard)

def get_rule_detail_keyboard(rule_id):
    """Клавиатура для детального просмотра правила"""
    keyboard = [
        [InlineKeyboardButton('✏️ Редактировать', callback_data=f'edit_rule_{rule_id}')],
        [InlineKeyboardButton('🗑️ Удалить', callback_data=f'delete_rule_{rule_id}')],
        [InlineKeyboardButton('⏰ Настроить напоминание', callback_data=f'set_reminder_{rule_id}')],
        [InlineKeyboardButton('Назад к списку', callback_data='view_rules')]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_edit_rule_keyboard(rule_id):
    """Клавиатура для редактирования правила"""
    keyboard = [
        [InlineKeyboardButton('📝 Изменить текст', callback_data=f'edit_text_{rule_id}')],
        [InlineKeyboardButton('⏰ Изменить напоминание', callback_data=f'edit_reminder_{rule_id}')],
        [InlineKeyboardButton('🔄 Включить/Выключить', callback_data=f'toggle_rule_{rule_id}')],
        [InlineKeyboardButton('Назад', callback_data=f'rule_detail_{rule_id}')]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_reminder_keyboard():
    """Клавиатура для настройки напоминания"""
    keyboard = [
        [InlineKeyboardButton('⏰ Утром (08:00)', callback_data='reminder_morning')],
        [InlineKeyboardButton('🌅 Днем (12:00)', callback_data='reminder_afternoon')],
        [InlineKeyboardButton('🌆 Вечером (18:00)', callback_data='reminder_evening')],
        [InlineKeyboardButton('🌙 Ночью (22:00)', callback_data='reminder_night')],
        [InlineKeyboardButton('❌ Без напоминания', callback_data='no_reminder')],
        [InlineKeyboardButton('Назад', callback_data='add_rule')]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_confirm_delete_keyboard(rule_id):
    """Клавиатура подтверждения удаления"""
    keyboard = [
        [InlineKeyboardButton('✅ Да, удалить', callback_data=f'confirm_delete_{rule_id}')],
        [InlineKeyboardButton('❌ Отмена', callback_data=f'rule_detail_{rule_id}')]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_skip_reminder_keyboard():
    """Клавиатура для пропуска настройки напоминания"""
    keyboard = [
        [InlineKeyboardButton('⏭️ Пропустить', callback_data='skip_reminder')],
        [InlineKeyboardButton('Назад', callback_data='add_rule')]
    ]
    return InlineKeyboardMarkup(keyboard)

# Клавиатуры для спорта
def get_sport_menu_keyboard():
    """Меню спорта"""
    keyboard = [
        [InlineKeyboardButton('📋 План тренировок', callback_data='workout_plan')],
        [InlineKeyboardButton('📝 Дневник тренировок', callback_data='workout_journal')],
        [InlineKeyboardButton('🎯 Спортивная цель', callback_data='sport_goal')],
        [InlineKeyboardButton('Назад', callback_data=CALLBACK_DATA['sd_home'])]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_workout_plan_keyboard():
    """Клавиатура плана тренировок"""
    keyboard = [
        [InlineKeyboardButton('➕ Добавить план', callback_data='add_workout_plan')],
        [InlineKeyboardButton('📋 Мои планы', callback_data='view_workout_plans')],
        [InlineKeyboardButton('Назад', callback_data='sport_home')]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_workout_journal_keyboard():
    """Клавиатура дневника тренировок"""
    keyboard = [
        [InlineKeyboardButton('➕ Добавить тренировку', callback_data='add_workout_journal')],
        [InlineKeyboardButton('📊 Статистика', callback_data='sport_statistics')],
        [InlineKeyboardButton('Назад', callback_data='sport_home')]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_workout_type_keyboard():
    """Клавиатура выбора типа тренировки"""
    keyboard = [
        [InlineKeyboardButton('💪 Силовая тренировка', callback_data='strength_workout')],
        [InlineKeyboardButton('🏃‍♂️ Кардио тренировка', callback_data='cardio_workout')],
        [InlineKeyboardButton('Назад', callback_data='sport_home')]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_exercises_keyboard(exercises):
    """Клавиатура со списком упражнений"""
    keyboard = []
    for exercise in exercises:
        keyboard.append([InlineKeyboardButton(
            f"💪 {exercise.name}", 
            callback_data=f'select_exercise_{exercise.id}'
        )])
    keyboard.append([InlineKeyboardButton('➕ Добавить новое упражнение', callback_data='add_new_exercise')])
    keyboard.append([InlineKeyboardButton('Назад', callback_data='sport_home')])
    return InlineKeyboardMarkup(keyboard)

def get_feeling_keyboard():
    """Клавиатура для оценки самочувствия"""
    keyboard = [
        [InlineKeyboardButton('1', callback_data='feeling_1'), InlineKeyboardButton('2', callback_data='feeling_2'), 
         InlineKeyboardButton('3', callback_data='feeling_3'), InlineKeyboardButton('4', callback_data='feeling_4'), 
         InlineKeyboardButton('5', callback_data='feeling_5')],
        [InlineKeyboardButton('6', callback_data='feeling_6'), InlineKeyboardButton('7', callback_data='feeling_7'), 
         InlineKeyboardButton('8', callback_data='feeling_8'), InlineKeyboardButton('9', callback_data='feeling_9'), 
         InlineKeyboardButton('10', callback_data='feeling_10')]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_add_more_sets_keyboard():
    """Клавиатура для добавления еще подходов"""
    keyboard = [
        [InlineKeyboardButton('➕ Добавить еще подход', callback_data='add_more_sets')],
        [InlineKeyboardButton('✅ Завершить упражнение', callback_data='finish_exercise')],
        [InlineKeyboardButton('🏁 Завершить тренировку', callback_data='finish_workout')]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_finish_workout_keyboard():
    """Клавиатура для завершения тренировки"""
    keyboard = [
        [InlineKeyboardButton('🏁 Завершить тренировку', callback_data='finish_workout')],
        [InlineKeyboardButton('➕ Добавить еще упражнение', callback_data='add_another_exercise')]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_sport_goal_keyboard():
    """Клавиатура спортивной цели"""
    keyboard = [
        [InlineKeyboardButton('✏️ Изменить цель', callback_data='edit_sport_goal')],
        [InlineKeyboardButton('Назад', callback_data='sport_home')]
    ]
    return InlineKeyboardMarkup(keyboard)

# Клавиатуры для теста правил
def get_rules_test_keyboard():
    """Клавиатура теста правил"""
    keyboard = [
        [InlineKeyboardButton('✅ Да, все правила соблюдены', callback_data='rules_all_followed')],
        [InlineKeyboardButton('❌ Нет, некоторые правила нарушены', callback_data='rules_some_violated')],
        [InlineKeyboardButton('Назад', callback_data=CALLBACK_DATA['sd_home'])]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_rules_violations_keyboard(violated_rules):
    """Клавиатура с нарушенными правилами"""
    keyboard = []
    for rule in violated_rules:
        keyboard.append([InlineKeyboardButton(
            f"❌ {rule.rule_text[:40]}{'...' if len(rule.rule_text) > 40 else ''}", 
            callback_data=f'violation_rule_{rule.id}'
        )])
    keyboard.append([InlineKeyboardButton('Назад', callback_data='rules_test_home')])
    return InlineKeyboardMarkup(keyboard)

def get_rules_test_back_keyboard():
    """Клавиатура возврата в тест правил"""
    keyboard = [
        [InlineKeyboardButton('Назад к тесту правил', callback_data='rules_test_home')]
    ]
    return InlineKeyboardMarkup(keyboard)

# Клавиатуры для анализа
def get_analysis_menu_keyboard():
    """Меню анализа"""
    keyboard = [
        [InlineKeyboardButton('➕ Создать анализ', callback_data='create_analysis')],
        [InlineKeyboardButton('📚 Сборник анализов', callback_data='analysis_collection')],
        [InlineKeyboardButton('Назад', callback_data=CALLBACK_DATA['sd_home'])]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_analyses_list_keyboard(analyses):
    """Клавиатура со списком анализов"""
    keyboard = []
    for analysis in analyses:
        keyboard.append([InlineKeyboardButton(
            f"📄 {analysis.title}", 
            callback_data=f'view_analysis_{analysis.id}'
        )])
    keyboard.append([InlineKeyboardButton('Назад', callback_data='analysis_home')])
    return InlineKeyboardMarkup(keyboard)

def get_analysis_detail_keyboard(analysis_id):
    """Клавиатура для детального просмотра анализа"""
    keyboard = [
        [InlineKeyboardButton('📊 Оценить анализ', callback_data=f'review_analysis_{analysis_id}')],
        [InlineKeyboardButton('Назад к списку', callback_data='analysis_collection')]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_analysis_review_keyboard(analysis_id):
    """Клавиатура для оценки анализа"""
    keyboard = [
        [InlineKeyboardButton('✅ Да, помог', callback_data=f'analysis_helpful_{analysis_id}')],
        [InlineKeyboardButton('❌ Нет, не помог', callback_data=f'analysis_not_helpful_{analysis_id}')],
        [InlineKeyboardButton('Назад', callback_data=f'view_analysis_{analysis_id}')]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_analysis_back_keyboard():
    """Клавиатура возврата в анализ"""
    keyboard = [
        [InlineKeyboardButton('Назад к анализу', callback_data='analysis_home')]
    ]
    return InlineKeyboardMarkup(keyboard)

# Клавиатуры для дневника
def get_diary_menu_keyboard():
    """Меню дневника"""
    keyboard = [
        [InlineKeyboardButton('📅 Просмотр по дате', callback_data='diary_date_selection')],
        [InlineKeyboardButton('Назад', callback_data=CALLBACK_DATA['sd_home'])]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_diary_date_keyboard():
    """Клавиатура для просмотра дневника по дате"""
    keyboard = [
        [InlineKeyboardButton('📅 Выбрать другую дату', callback_data='diary_date_selection')],
        [InlineKeyboardButton('Назад в меню дневника', callback_data='diary_home')]
    ]
    return InlineKeyboardMarkup(keyboard)

