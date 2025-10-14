"""
Пакет обработчиков для Telegram бота
"""

from .start_handlers import start, return_to_start, dict_home, exit_review, instructions, go_home, set_daily_reminder, start_and_set_reminder
from .word_handlers import (
    ask_en_word, get_word, get_p_s, get_translation,
    date_for_r, get_date
)
from .review_handlers import (
    ask_review_type, send_word_starter, end_starter, send_word_interm,
    show_interm_translation, wait_interm_sent_translation, check_user_input,
    save_interm, send_next_word_f, show_hint, get_sentence
)
from .oxford_handlers import (
    get_random_words, choose_p_s, show_ox_examples, add_ox_word
)
from .ai_handlers import (
    save_review, option_2, save_sent, option_3, show_ai_sentence,
    interm_option_2, save_interm_option_2
)

from .sd_home_handlers import (sd_home)

from .tasks_handler import tasks_w, add_task, wait_date, approve_task, day_view, month_view, year_view, show_tasks_list, show_task_detail, mark_task_completed, delete_task, edit_task_start, edit_task_text

from .nutrition_handlers import (
    nutrition_home, add_meal_start, add_dish_start, wait_dish_name, wait_dish_calories,
    wait_dish_protein, wait_dish_grams, find_dishes_start, select_dish, complete_meal_final,
    nutrition_chart, nutrition_menu, add_rule_start, wait_rule_text, wait_reminder_time,
    wait_exceptions, skip_reminder, skip_exceptions, set_goals_start, set_calories_start,
    set_protein_start, wait_calories_goal, wait_protein_goal, add_note_start, wait_note_text,
    view_nutrition_date_start, wait_nutrition_date,
)

from .routine_handlers import (
    routines_home, morning_routine_menu, evening_routine_menu, start_morning_routine,
    start_evening_routine, setup_morning_routine, setup_evening_routine,
    create_morning_routine_start, create_evening_routine_start, wait_routine_name,
    wait_morning_actions, wait_evening_actions, select_morning_routine, select_evening_routine,
    routine_action_completed, skip_routine_action, cancel_routine, routines_chart,
    view_morning_routines, view_evening_routines
)

from .morning_testing_handlers import (
    morning_testing_handle_text, morning_testing_health_condition,
    morning_testing_muscle_fatigue, morning_testing_health_complaints
)

from .rules_handlers import (
    rules_home, view_rules, add_rule_start, add_rule_text, add_rule_reminder,
    rule_detail, edit_rule_start, edit_rule_text_start, edit_rule_text,
    edit_rule_reminder_start, edit_rule_reminder, toggle_rule,
    delete_rule_start, delete_rule_confirm, skip_reminder
)

from .sport_handlers import (
    sport_home, workout_plan_menu, workout_journal_menu, add_workout_plan_start,
    add_workout_journal_start, select_workout_type_plan, select_workout_type_journal,
    wait_workout_date, wait_journal_date, wait_exercise_name, wait_sets, wait_weight,
    wait_reps, wait_cardio_duration, wait_cardio_distance, wait_cardio_intensity,
    wait_journal_duration, wait_journal_activity, wait_journal_distance,
    wait_journal_heart_rate, journal_feeling_selected, select_exercise_for_journal,
    wait_set_weight, wait_set_reps, add_more_sets, add_another_exercise, sport_goal_menu, edit_sport_goal,
    wait_sport_goal, view_workout_plans, sport_statistics
)

from .diary_handlers import (
    diary_home, diary_date_selection, wait_diary_date, diary_back_to_menu
)

__all__ = [
    'start', 'return_to_start', 'dict_home', 'exit_review',
    'ask_en_word', 'get_word', 'get_p_s', 'get_translation',
    'date_for_r', 'get_date',
    'ask_review_type', 'send_word_starter', 'end_starter', 'send_word_interm',
    'show_interm_translation', 'wait_interm_sent_translation', 'check_user_input',
    'save_interm', 'send_next_word_f', 'show_hint', 'get_sentence',
    'get_random_words', 'choose_p_s', 'show_ox_examples', 'add_ox_word',
    'save_review', 'option_2', 'save_sent', 'option_3', 'show_ai_sentence',
    'interm_option_2', 'save_interm_option_2', 'instructions', 'go_home', 'start_and_set_reminder', 'set_daily_reminder',
    'sd_home', 'tasks_w', 'add_task', 'wait_date', 'approve_task', 'day_view', 'month_view', 'year_view', 'show_tasks_list', 'show_task_detail', 'mark_task_completed', 'delete_task', 'edit_task_start', 'edit_task_text',
    'nutrition_home', 'add_meal_start', 'add_dish_start', 'wait_dish_name', 'wait_dish_calories',
    'wait_dish_protein', 'wait_dish_grams', 'find_dishes_start', 'select_dish', 'complete_meal_final',
    'nutrition_chart', 'nutrition_menu', 'add_rule_start', 'wait_rule_text', 'wait_reminder_time',
    'wait_exceptions', 'skip_reminder', 'skip_exceptions', 'set_goals_start', 'set_calories_start',
    'set_protein_start', 'wait_calories_goal', 'wait_protein_goal', 'add_note_start', 'wait_note_text',
    'view_nutrition_date_start', 'wait_nutrition_date',
    'routines_home', 'morning_routine_menu', 'evening_routine_menu', 'start_morning_routine',
    'start_evening_routine', 'setup_morning_routine', 'setup_evening_routine',
    'create_morning_routine_start', 'create_evening_routine_start', 'wait_routine_name',
    'wait_morning_actions', 'wait_evening_actions', 'select_morning_routine', 'select_evening_routine',
    'routine_action_completed', 'skip_routine_action', 'cancel_routine', 'routines_chart',
    'view_morning_routines', 'view_evening_routines',
    'morning_testing_handle_text', 'morning_testing_health_condition',
    'morning_testing_muscle_fatigue', 'morning_testing_health_complaints',
    'rules_home', 'view_rules', 'add_rule_start', 'add_rule_text', 'add_rule_reminder',
    'rule_detail', 'edit_rule_start', 'edit_rule_text_start', 'edit_rule_text',
    'edit_rule_reminder_start', 'edit_rule_reminder', 'toggle_rule',
    'delete_rule_start', 'delete_rule_confirm', 'skip_reminder',
    'sport_home', 'workout_plan_menu', 'workout_journal_menu', 'add_workout_plan_start',
    'add_workout_journal_start', 'select_workout_type_plan', 'select_workout_type_journal',
    'wait_workout_date', 'wait_journal_date', 'wait_exercise_name', 'wait_sets', 'wait_weight',
    'wait_reps', 'wait_cardio_duration', 'wait_cardio_distance', 'wait_cardio_intensity',
    'wait_journal_duration', 'wait_journal_activity', 'wait_journal_distance',
    'wait_journal_heart_rate', 'journal_feeling_selected', 'select_exercise_for_journal',
    'wait_set_weight', 'wait_set_reps', 'add_more_sets', 'add_another_exercise', 'sport_goal_menu', 'edit_sport_goal',
    'wait_sport_goal', 'view_workout_plans', 'sport_statistics',
    'diary_home', 'diary_date_selection', 'wait_diary_date', 'diary_back_to_menu'
]

