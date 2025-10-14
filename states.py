"""
Состояния для ConversationHandler
"""

# Определяем все состояния бота
start_route, dict_maiin, get_en_word, wait_p_s, wait_translation = range(0, 5)
wait_date, start_forced_r, first_ai_answer, wait_right_sent = range(5, 9)
wait_ru_sentance, learn_ox_word, wait_ox_ps, wait_interm_translation = range(9, 13)
wait_interm_sentence, wait_interm_user_translation, interm_ai_review = range(13, 16)
wait_interm_right_sentence, wait_starter_translation, end_starter_state, instructions = range(16, 20)
sd_home, tasks_w, add_task, wait_date_for_task, approve_task, day_view, month_view, year_view, edit_task_text = range(20, 29)
# Состояния для питания
nutrition_home, add_meal, add_dish, wait_dish_name, wait_dish_calories, wait_dish_protein, wait_dish_grams, find_dishes, wait_dish_number, complete_meal, nutrition_chart, nutrition_menu, nutrition_goals, set_calories_goal, set_protein_goal, nutrition_rules, add_rule, wait_rule_text, wait_reminder_time, wait_exceptions, nutrition_notes, add_note, wait_note_text, view_nutrition_date, wait_nutrition_date = range(29, 54)

# Состояния для рутин
routines_home, morning_routine, evening_routine, setup_morning_routine, setup_evening_routine, create_morning_routine, create_evening_routine, wait_morning_actions, wait_evening_actions, select_morning_routine, select_evening_routine, executing_morning_routine, executing_evening_routine, morning_testing = range(54, 68)

# Состояния для правил
rules_home, add_rule_text, add_rule_reminder, edit_rule, edit_rule_text, edit_rule_reminder, delete_rule_confirm, view_rules = range(68, 76)

# Состояния для спорта
sport_home, workout_plan, workout_journal, add_workout_plan, add_workout_journal, select_workout_type = range(76, 82)
wait_workout_date, wait_workout_type_plan, wait_exercise_name, wait_sets, wait_weight, wait_reps = range(82, 88)
wait_cardio_duration, wait_cardio_distance, wait_cardio_intensity, wait_journal_workout_type = range(88, 92)
wait_journal_date, wait_journal_duration, wait_journal_feeling, wait_journal_activity = range(92, 96)
wait_journal_distance, wait_journal_heart_rate, select_exercise, wait_set_weight = range(96, 100)
wait_set_reps, sport_goal, wait_sport_goal = range(100, 103)

# Состояния для теста правил
rules_test_home, rules_test_result, rules_test_violations, rules_test_reason, rules_test_exception = range(103, 108)

# Состояния для анализа
analysis_home, analysis_create, analysis_title, analysis_situation, analysis_reason, analysis_prevention, analysis_collection, analysis_review = range(108, 116)

# Состояния для дневника
diary_home, wait_diary_date, diary_view = range(116, 119)

# Состояния для расписания
schedule_home, schedule_view, schedule_add, schedule_edit, schedule_delete, schedule_manage = range(119, 125)
wait_schedule_date, wait_schedule_time, wait_schedule_title, wait_schedule_description = range(125, 129)


# Словарь состояний для удобства использования
STATES = {
    'start_route': start_route,
    'instructions': instructions,
    'dict_maiin': dict_maiin,
    'get_en_word': get_en_word,
    'wait_p_s': wait_p_s,
    'wait_translation': wait_translation,
    'wait_date': wait_date,
    'start_forced_r': start_forced_r,
    'first_ai_answer': first_ai_answer,
    'wait_right_sent': wait_right_sent,
    'wait_ru_sentance': wait_ru_sentance,
    'learn_ox_word': learn_ox_word,
    'wait_ox_ps': wait_ox_ps,
    'wait_interm_translation': wait_interm_translation,
    'wait_interm_sentence': wait_interm_sentence,
    'wait_interm_user_translation': wait_interm_user_translation,
    'interm_ai_review': interm_ai_review,
    'wait_interm_right_sentence': wait_interm_right_sentence,
    'wait_starter_translation': wait_starter_translation,
    'end_starter_state': end_starter_state,
    'sd_home': sd_home,
    'tasks_w': tasks_w,
    'add_task': add_task,
    'wait_date_for_task': wait_date_for_task,
    'approve_task': approve_task,
    'day_view': day_view,
    'month_view': month_view,
    'year_view': year_view,
    'edit_task_text': edit_task_text,
    # Состояния для питания
    'nutrition_home': nutrition_home,
    'add_meal': add_meal,
    'add_dish': add_dish,
    'wait_dish_name': wait_dish_name,
    'wait_dish_calories': wait_dish_calories,
    'wait_dish_protein': wait_dish_protein,
    'wait_dish_grams': wait_dish_grams,
    'find_dishes': find_dishes,
    'wait_dish_number': wait_dish_number,
    'complete_meal': complete_meal,
    'nutrition_chart': nutrition_chart,
    'nutrition_menu': nutrition_menu,
    'nutrition_goals': nutrition_goals,
    'set_calories_goal': set_calories_goal,
    'set_protein_goal': set_protein_goal,
    'set_calories': set_calories_goal,
    'set_protein': set_protein_goal,
    'set_goals': nutrition_goals,
    'nutrition_rules': nutrition_rules,
    'add_rule': add_rule,
    'wait_rule_text': wait_rule_text,
    'wait_reminder_time': wait_reminder_time,
    'wait_exceptions': wait_exceptions,
    'nutrition_notes': nutrition_notes,
    'add_note': add_note,
    'wait_note_text': wait_note_text,
    'view_nutrition_date': view_nutrition_date,
    'wait_nutrition_date': wait_nutrition_date,
    # Состояния для рутин
    'routines_home': routines_home,
    'morning_routine': morning_routine,
    'evening_routine': evening_routine,
    'setup_morning_routine': setup_morning_routine,
    'setup_evening_routine': setup_evening_routine,
    'create_morning_routine': create_morning_routine,
    'create_evening_routine': create_evening_routine,
    'wait_morning_actions': wait_morning_actions,
    'wait_evening_actions': wait_evening_actions,
    'select_morning_routine': select_morning_routine,
    'select_evening_routine': select_evening_routine,
    'executing_morning_routine': executing_morning_routine,
    'executing_evening_routine': executing_evening_routine,
    'morning_testing': morning_testing,
    # Состояния для правил
    'rules_home': rules_home,
    'add_rule_text': add_rule_text,
    'add_rule_reminder': add_rule_reminder,
    'edit_rule': edit_rule,
    'edit_rule_text': edit_rule_text,
    'edit_rule_reminder': edit_rule_reminder,
    'delete_rule_confirm': delete_rule_confirm,
    'view_rules': view_rules,
    # Состояния для спорта
    'sport_home': sport_home,
    'workout_plan': workout_plan,
    'workout_journal': workout_journal,
    'add_workout_plan': add_workout_plan,
    'add_workout_journal': add_workout_journal,
    'select_workout_type': select_workout_type,
    'wait_workout_date': wait_workout_date,
    'wait_workout_type_plan': wait_workout_type_plan,
    'wait_exercise_name': wait_exercise_name,
    'wait_sets': wait_sets,
    'wait_weight': wait_weight,
    'wait_reps': wait_reps,
    'wait_cardio_duration': wait_cardio_duration,
    'wait_cardio_distance': wait_cardio_distance,
    'wait_cardio_intensity': wait_cardio_intensity,
    'wait_journal_workout_type': wait_journal_workout_type,
    'wait_journal_date': wait_journal_date,
    'wait_journal_duration': wait_journal_duration,
    'wait_journal_feeling': wait_journal_feeling,
    'wait_journal_activity': wait_journal_activity,
    'wait_journal_distance': wait_journal_distance,
    'wait_journal_heart_rate': wait_journal_heart_rate,
    'select_exercise': select_exercise,
    'wait_set_weight': wait_set_weight,
    'wait_set_reps': wait_set_reps,
    'sport_goal': sport_goal,
    'wait_sport_goal': wait_sport_goal,
    # Состояния для теста правил
    'rules_test_home': rules_test_home,
    'rules_test_result': rules_test_result,
    'rules_test_violations': rules_test_violations,
    'rules_test_reason': rules_test_reason,
    'rules_test_exception': rules_test_exception,
    # Состояния для анализа
    'analysis_home': analysis_home,
    'analysis_create': analysis_create,
    'analysis_title': analysis_title,
    'analysis_situation': analysis_situation,
    'analysis_reason': analysis_reason,
    'analysis_prevention': analysis_prevention,
    'analysis_collection': analysis_collection,
    'analysis_review': analysis_review,
    # Состояния для дневника
    'diary_home': diary_home,
    'wait_diary_date': wait_diary_date,
    'diary_view': diary_view,
    # Состояния для расписания
    'schedule_home': schedule_home,
    'schedule_view': schedule_view,
    'schedule_add': schedule_add,
    'schedule_edit': schedule_edit,
    'schedule_delete': schedule_delete,
    'schedule_manage': schedule_manage,
    'wait_schedule_date': wait_schedule_date,
    'wait_schedule_time': wait_schedule_time,
    'wait_schedule_title': wait_schedule_title,
    'wait_schedule_description': wait_schedule_description
}

