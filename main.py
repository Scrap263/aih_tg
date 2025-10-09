"""
Основной файл запуска Telegram бота
"""
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    filters,
    JobQueue
)
import asyncio

from config import TG_API, CALLBACK_DATA, SD_CD
from states import STATES
from models import update_structure
import handlers
import handlers.rules_test_handlers as rules_test_handlers
import handlers.analysis_handlers as analysis_handlers


def create_conversation_handler():
    """Создает ConversationHandler с всеми состояниями и обработчиками"""
    
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('start', handlers.start_and_set_reminder)],
        states={
            STATES['start_route']: [
                CallbackQueryHandler(handlers.dict_home, pattern='^' + CALLBACK_DATA['dict_main'] + '$'),
                CallbackQueryHandler(handlers.instructions, pattern='^' + CALLBACK_DATA['instructions'] + '$'),
                CallbackQueryHandler(handlers.sd_home, pattern="^" + CALLBACK_DATA['sd_home'] + '$')
            ],
            STATES['dict_maiin']: [
                CallbackQueryHandler(handlers.ask_en_word, pattern='^' + CALLBACK_DATA['add_word'] + '$'),
                CallbackQueryHandler(handlers.date_for_r, pattern='^' + CALLBACK_DATA['review_words'] + '$'),
                CallbackQueryHandler(handlers.ask_review_type, pattern='^' + CALLBACK_DATA['ask_type_of_review'] + '$'),
                CallbackQueryHandler(handlers.send_next_word_f, pattern='^' + 'start_forced_r' + '$'),
                CallbackQueryHandler(handlers.get_random_words, pattern='^' + CALLBACK_DATA['oxford3000'] + '$'),
                CallbackQueryHandler(handlers.return_to_start, pattern='^' + CALLBACK_DATA['main_menu'] + '$')
            ],
            STATES['get_en_word']: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.get_word),
                CallbackQueryHandler(handlers.dict_home, pattern='^' + CALLBACK_DATA['redirect_to_dict_menu'] + '$')
            ],
            STATES['wait_p_s']: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.get_p_s),
                CallbackQueryHandler(handlers.dict_home, pattern='^' + CALLBACK_DATA['redirect_to_dict_menu'] + '$')
            ],
            STATES['wait_translation']: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.get_translation),
                CallbackQueryHandler(handlers.dict_home, pattern='^' + CALLBACK_DATA['redirect_to_dict_menu'] + '$')
            ],
            STATES['wait_date']: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.get_date),
                CallbackQueryHandler(handlers.dict_home, pattern='^' + CALLBACK_DATA['redirect_to_dict_menu'] + '$')
            ],
            STATES['start_forced_r']: [
                CallbackQueryHandler(handlers.send_next_word_f, pattern='^' + 'start_forced_r' + '$'),
                CallbackQueryHandler(handlers.show_hint, pattern='^' + 'hint' + '$'),
                CallbackQueryHandler(handlers.dict_home, pattern='^' + CALLBACK_DATA['redirect_to_dict_menu'] + '$'),
                CallbackQueryHandler(handlers.ask_review_type, pattern='^' + CALLBACK_DATA['ask_type_of_review'] + '$'),
                MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.get_sentence),
                CallbackQueryHandler(handlers.send_next_word_f, pattern='^' + 'skip_word' + '$'),
                CallbackQueryHandler(handlers.send_word_interm, pattern='^' + 'interm' + '$'),
                CallbackQueryHandler(handlers.send_word_starter, pattern='^' + 'starter' + '$')
            ],
            STATES['first_ai_answer']: [
                CallbackQueryHandler(handlers.save_review, pattern='^' + 'option_1' + '$'),
                CallbackQueryHandler(handlers.option_2, pattern='^' + 'option_2' + '$'),
                CallbackQueryHandler(handlers.option_3, pattern='^' + 'option_3' + '$'),
                CallbackQueryHandler(handlers.dict_home, pattern='^' + CALLBACK_DATA['redirect_to_dict_menu'] + '$')
            ],
            STATES['wait_right_sent']: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.save_sent),
                CallbackQueryHandler(handlers.dict_home, pattern='^' + CALLBACK_DATA['redirect_to_dict_menu'] + '$')
            ],
            STATES['wait_ru_sentance']: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.show_ai_sentence),
                CallbackQueryHandler(handlers.dict_home, pattern='^' + CALLBACK_DATA['redirect_to_dict_menu'] + '$')
            ],
            STATES['learn_ox_word']: [
                CallbackQueryHandler(handlers.choose_p_s, pattern='^' + 'ox_1' + '$'),
                CallbackQueryHandler(handlers.choose_p_s, pattern='^' + 'ox_2' + '$'),
                CallbackQueryHandler(handlers.choose_p_s, pattern='^' + 'ox_3' + '$'),
                CallbackQueryHandler(handlers.choose_p_s, pattern='^' + 'ox_4' + '$'),
                CallbackQueryHandler(handlers.choose_p_s, pattern='^' + 'ox_5' + '$'),
                CallbackQueryHandler(handlers.add_ox_word, pattern='^' + 'add_ox_word' + '$'),
                CallbackQueryHandler(handlers.dict_home, pattern='^' + CALLBACK_DATA['redirect_to_dict_menu'] + '$')
            ],
            STATES['wait_ox_ps']: [
                CallbackQueryHandler(handlers.show_ox_examples),
                MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.show_ox_examples),
                CallbackQueryHandler(handlers.dict_home, pattern='^' + CALLBACK_DATA['redirect_to_dict_menu'] + '$')
            ],
            STATES['wait_interm_translation']: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.show_interm_translation),
                CallbackQueryHandler(handlers.dict_home, pattern='^' + CALLBACK_DATA['redirect_to_dict_menu'] + '$'),
                CallbackQueryHandler(handlers.send_word_interm, pattern='^' + 'interm_skip_word' + '$')
            ],
            STATES['wait_interm_sentence']: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.wait_interm_sent_translation),
                CallbackQueryHandler(handlers.dict_home, pattern='^' + CALLBACK_DATA['redirect_to_dict_menu'] + '$')
            ],
            STATES['wait_interm_user_translation']: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.check_user_input),
                CallbackQueryHandler(handlers.show_interm_translation, pattern='^' + 'back_to_en_sentence' + '$'),
                CallbackQueryHandler(handlers.dict_home, pattern='^' + CALLBACK_DATA['redirect_to_dict_menu'] + '$')
            ],
            STATES['interm_ai_review']: [
                CallbackQueryHandler(handlers.save_interm, pattern='^' + 'interm_option_1' + '$'),
                CallbackQueryHandler(handlers.interm_option_2, pattern='^' + 'interm_option_2' + '$'),
                CallbackQueryHandler(handlers.dict_home, pattern='^' + CALLBACK_DATA['redirect_to_dict_menu'] + '$')
            ],
            STATES['wait_interm_right_sentence']: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.save_interm_option_2),
                CallbackQueryHandler(handlers.dict_home, pattern='^' + CALLBACK_DATA['redirect_to_dict_menu'] + '$')
            ],
            STATES['wait_starter_translation']: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.end_starter),
                CallbackQueryHandler(handlers.dict_home, pattern='^' + CALLBACK_DATA['redirect_to_dict_menu'] + '$'),
                CallbackQueryHandler(handlers.send_word_starter, pattern='^' + 'starter_skip_word' + '$')
            ],
            STATES['end_starter_state']: [
                CallbackQueryHandler(handlers.dict_home, pattern='^' + CALLBACK_DATA['redirect_to_dict_menu'] + '$'),
                CallbackQueryHandler(handlers.send_word_starter, pattern='^' + 'next_word' + '$')
            ],
            STATES['instructions']: [
                CallbackQueryHandler(handlers.go_home, pattern='^' + CALLBACK_DATA['main_m'] + '$')
            ],
            STATES['sd_home'] : [
                CallbackQueryHandler(handlers.tasks_w, pattern='^' + SD_CD['tasks'] + '$'),
                CallbackQueryHandler(handlers.nutrition_home, pattern='^' + SD_CD['nutrition'] + '$'),
                CallbackQueryHandler(handlers.routines_home, pattern='^' + SD_CD['routines'] + '$'),
                CallbackQueryHandler(handlers.rules_home, pattern='^' + SD_CD['rules'] + '$'),
                CallbackQueryHandler(handlers.sport_home, pattern='^' + SD_CD['sport'] + '$'),
                CallbackQueryHandler(handlers.routines_chart, pattern='^' + SD_CD['routines_chart'] + '$'),
                CallbackQueryHandler(handlers.day_view, pattern='^' + SD_CD['day'] + '$'),
                CallbackQueryHandler(handlers.month_view, pattern='^' + SD_CD['month'] + '$'),
                CallbackQueryHandler(handlers.year_view, pattern='^' + SD_CD['year'] + '$'),
                CallbackQueryHandler(handlers.go_home, pattern='^' + CALLBACK_DATA['main_m'] + '$')
            ],
            STATES['tasks_w'] : [
                CallbackQueryHandler(handlers.add_task, pattern='^' + SD_CD['add_task'] + '$'),
                CallbackQueryHandler(handlers.show_tasks_list, pattern='^manage_tasks$'),
                CallbackQueryHandler(handlers.day_view, pattern='^' + SD_CD['day'] + '$'),
                CallbackQueryHandler(handlers.month_view, pattern='^' + SD_CD['month'] + '$'),
                CallbackQueryHandler(handlers.year_view, pattern='^' + SD_CD['year'] + '$'),
                CallbackQueryHandler(handlers.sd_home, pattern='^' + CALLBACK_DATA['sd_home'] + '$'),
                CallbackQueryHandler(handlers.show_task_detail, pattern='^task_detail_'),
                CallbackQueryHandler(handlers.mark_task_completed, pattern='^mark_completed_'),
                CallbackQueryHandler(handlers.delete_task, pattern='^delete_task_'),
                CallbackQueryHandler(handlers.tasks_w, pattern='^' + SD_CD['tasks'] + '$')
            ],
            STATES['add_task']: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.wait_date)
            ],
            STATES['wait_date_for_task']: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.approve_task)
            ],
            # Состояния для питания
            STATES['nutrition_home']: [
                CallbackQueryHandler(handlers.add_meal_start, pattern='^' + SD_CD['add_meal'] + '$'),
                CallbackQueryHandler(handlers.nutrition_chart, pattern='^' + SD_CD['nutrition_chart'] + '$'),
                CallbackQueryHandler(handlers.view_nutrition_date_start, pattern='^view_nutrition_date$'),
                CallbackQueryHandler(handlers.sd_home, pattern='^' + CALLBACK_DATA['sd_home'] + '$')
            ],
            STATES['add_meal']: [
                CallbackQueryHandler(handlers.add_dish_start, pattern='^' + SD_CD['add_dish'] + '$'),
                CallbackQueryHandler(handlers.find_dishes_start, pattern='^' + SD_CD['find_dishes'] + '$'),
                CallbackQueryHandler(handlers.complete_meal_final, pattern='^' + SD_CD['complete_meal'] + '$'),
                CallbackQueryHandler(handlers.nutrition_home, pattern='^' + SD_CD['nutrition'] + '$')
            ],
            STATES['wait_dish_name']: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.wait_dish_name)
            ],
            STATES['wait_dish_calories']: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.wait_dish_calories)
            ],
            STATES['wait_dish_protein']: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.wait_dish_protein)
            ],
            STATES['wait_dish_grams']: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.wait_dish_grams)
            ],
            STATES['find_dishes']: [
                CallbackQueryHandler(handlers.select_dish, pattern='^select_dish_'),
                CallbackQueryHandler(handlers.add_meal_start, pattern='^' + SD_CD['add_meal'] + '$')
            ],
            STATES['nutrition_chart']: [
                CallbackQueryHandler(handlers.nutrition_menu, pattern='^' + SD_CD['nutrition_menu'] + '$'),
                CallbackQueryHandler(handlers.nutrition_home, pattern='^' + SD_CD['nutrition'] + '$')
            ],
            STATES['nutrition_menu']: [
                CallbackQueryHandler(handlers.add_rule_start, pattern='^' + SD_CD['add_rule'] + '$'),
                CallbackQueryHandler(handlers.set_goals_start, pattern='^' + SD_CD['set_goals'] + '$'),
                CallbackQueryHandler(handlers.add_note_start, pattern='^' + SD_CD['add_note'] + '$'),
                CallbackQueryHandler(handlers.nutrition_chart, pattern='^' + SD_CD['nutrition_chart'] + '$')
            ],
            STATES['wait_rule_text']: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.wait_rule_text)
            ],
            STATES['wait_reminder_time']: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.wait_reminder_time),
                CallbackQueryHandler(handlers.skip_reminder, pattern='^skip_reminder$')
            ],
            STATES['wait_exceptions']: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.wait_exceptions),
                CallbackQueryHandler(handlers.skip_exceptions, pattern='^skip_exceptions$')
            ],
            STATES['set_goals']: [
                CallbackQueryHandler(handlers.set_calories_start, pattern='^' + SD_CD['set_calories'] + '$'),
                CallbackQueryHandler(handlers.set_protein_start, pattern='^' + SD_CD['set_protein'] + '$'),
                CallbackQueryHandler(handlers.nutrition_menu, pattern='^' + SD_CD['nutrition_menu'] + '$')
            ],
            STATES['set_calories']: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.wait_calories_goal)
            ],
            STATES['set_protein']: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.wait_protein_goal)
            ],
            STATES['wait_note_text']: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.wait_note_text)
            ],
            STATES['wait_nutrition_date']: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.wait_nutrition_date),
                CallbackQueryHandler(handlers.nutrition_home, pattern='^' + SD_CD['nutrition'] + '$')
            ],
            STATES['view_nutrition_date']: [
                CallbackQueryHandler(handlers.view_nutrition_date_start, pattern='^view_nutrition_date$'),
                CallbackQueryHandler(handlers.nutrition_home, pattern='^' + SD_CD['nutrition'] + '$')
            ],
            # Состояния для рутин
            STATES['routines_home']: [
                CallbackQueryHandler(handlers.morning_routine_menu, pattern='^morning_routine$'),
                CallbackQueryHandler(handlers.evening_routine_menu, pattern='^evening_routine$'),
                CallbackQueryHandler(handlers.routines_chart, pattern='^routines_chart$'),
                CallbackQueryHandler(handlers.sd_home, pattern='^' + CALLBACK_DATA['sd_home'] + '$')
            ],
            STATES['morning_routine']: [
                CallbackQueryHandler(handlers.start_morning_routine, pattern='^start_morning_routine$'),
                CallbackQueryHandler(handlers.setup_morning_routine, pattern='^setup_morning_routine$'),
                CallbackQueryHandler(handlers.routines_home, pattern='^routines_menu$')
            ],
            STATES['evening_routine']: [
                CallbackQueryHandler(handlers.start_evening_routine, pattern='^start_evening_routine$'),
                CallbackQueryHandler(handlers.setup_evening_routine, pattern='^setup_evening_routine$'),
                CallbackQueryHandler(handlers.routines_home, pattern='^routines_menu$')
            ],
            STATES['setup_morning_routine']: [
                CallbackQueryHandler(handlers.create_morning_routine_start, pattern='^create_morning_routine$'),
                CallbackQueryHandler(handlers.morning_routine_menu, pattern='^morning_routine$')
            ],
            STATES['setup_evening_routine']: [
                CallbackQueryHandler(handlers.create_evening_routine_start, pattern='^create_evening_routine$'),
                CallbackQueryHandler(handlers.evening_routine_menu, pattern='^evening_routine$')
            ],
            STATES['create_morning_routine']: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.wait_routine_name)
            ],
            STATES['create_evening_routine']: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.wait_routine_name)
            ],
            STATES['wait_morning_actions']: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.wait_morning_actions)
            ],
            STATES['wait_evening_actions']: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.wait_evening_actions)
            ],
            STATES['select_morning_routine']: [
                CallbackQueryHandler(handlers.select_morning_routine, pattern='^select_morning_routine_'),
                CallbackQueryHandler(handlers.morning_routine_menu, pattern='^morning_routine$')
            ],
            STATES['select_evening_routine']: [
                CallbackQueryHandler(handlers.select_evening_routine, pattern='^select_evening_routine_'),
                CallbackQueryHandler(handlers.evening_routine_menu, pattern='^evening_routine$')
            ],
            STATES['executing_morning_routine']: [
                CallbackQueryHandler(handlers.routine_action_completed, pattern='^action_completed$'),
                CallbackQueryHandler(handlers.skip_routine_action, pattern='^skip_action$'),
                CallbackQueryHandler(handlers.cancel_routine, pattern='^cancel_routine$')
            ],
            STATES['executing_evening_routine']: [
                CallbackQueryHandler(handlers.routine_action_completed, pattern='^action_completed$'),
                CallbackQueryHandler(handlers.skip_routine_action, pattern='^skip_action$'),
                CallbackQueryHandler(handlers.cancel_routine, pattern='^cancel_routine$')
            ],
            STATES['morning_testing']: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.morning_testing_handle_text),
                CallbackQueryHandler(handlers.morning_testing_health_condition, pattern='^health_[1-9]|10$'),
                CallbackQueryHandler(handlers.morning_testing_muscle_fatigue, pattern='^fatigue_[1-9]|10$')
            ],
            # Состояния для правил
            STATES['rules_home']: [
                CallbackQueryHandler(handlers.view_rules, pattern='^view_rules$'),
                CallbackQueryHandler(handlers.add_rule_start, pattern='^add_rule$'),
                CallbackQueryHandler(handlers.sd_home, pattern='^' + CALLBACK_DATA['sd_home'] + '$')
            ],
            STATES['view_rules']: [
                CallbackQueryHandler(handlers.rule_detail, pattern='^rule_detail_'),
                CallbackQueryHandler(handlers.add_rule_start, pattern='^add_rule$'),
                CallbackQueryHandler(handlers.rules_home, pattern='^rules_home$')
            ],
            STATES['add_rule_text']: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.add_rule_text),
                CallbackQueryHandler(handlers.rules_home, pattern='^rules_home$')
            ],
            STATES['add_rule_reminder']: [
                CallbackQueryHandler(handlers.add_rule_reminder, pattern='^reminder_'),
                CallbackQueryHandler(handlers.skip_reminder, pattern='^skip_reminder$'),
                CallbackQueryHandler(handlers.add_rule_start, pattern='^add_rule$')
            ],
            STATES['edit_rule']: [
                CallbackQueryHandler(handlers.edit_rule_start, pattern='^edit_rule_'),
                CallbackQueryHandler(handlers.delete_rule_start, pattern='^delete_rule_'),
                CallbackQueryHandler(handlers.edit_rule_reminder_start, pattern='^set_reminder_'),
                CallbackQueryHandler(handlers.view_rules, pattern='^view_rules$')
            ],
            STATES['edit_rule_text']: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.edit_rule_text),
                CallbackQueryHandler(handlers.rules_home, pattern='^rules_home$')
            ],
            STATES['edit_rule_reminder']: [
                CallbackQueryHandler(handlers.edit_rule_reminder, pattern='^reminder_'),
                CallbackQueryHandler(handlers.rules_home, pattern='^rules_home$')
            ],
            STATES['delete_rule_confirm']: [
                CallbackQueryHandler(handlers.delete_rule_confirm, pattern='^confirm_delete_'),
                CallbackQueryHandler(handlers.rule_detail, pattern='^rule_detail_')
            ],
            # Состояния для спорта
            STATES['sport_home']: [
                CallbackQueryHandler(handlers.workout_plan_menu, pattern='^workout_plan$'),
                CallbackQueryHandler(handlers.workout_journal_menu, pattern='^workout_journal$'),
                CallbackQueryHandler(handlers.sport_goal_menu, pattern='^sport_goal$'),
                CallbackQueryHandler(handlers.sd_home, pattern='^' + CALLBACK_DATA['sd_home'] + '$')
            ],
            STATES['workout_plan']: [
                CallbackQueryHandler(handlers.add_workout_plan_start, pattern='^add_workout_plan$'),
                CallbackQueryHandler(handlers.sport_home, pattern='^sport_home$')
            ],
            STATES['workout_journal']: [
                CallbackQueryHandler(handlers.add_workout_journal_start, pattern='^add_workout_journal$'),
                CallbackQueryHandler(handlers.sport_home, pattern='^sport_home$')
            ],
            STATES['select_workout_type']: [
                CallbackQueryHandler(handlers.select_workout_type_plan, pattern='^strength_workout$'),
                CallbackQueryHandler(handlers.select_workout_type_plan, pattern='^cardio_workout$'),
                CallbackQueryHandler(handlers.workout_plan_menu, pattern='^workout_plan$')
            ],
            STATES['wait_workout_date']: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.wait_workout_date)
            ],
            STATES['wait_exercise_name']: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.wait_exercise_name)
            ],
            STATES['wait_sets']: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.wait_sets)
            ],
            STATES['wait_weight']: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.wait_weight)
            ],
            STATES['wait_reps']: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.wait_reps)
            ],
            STATES['wait_cardio_duration']: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.wait_cardio_duration)
            ],
            STATES['wait_cardio_distance']: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.wait_cardio_distance)
            ],
            STATES['wait_cardio_intensity']: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.wait_cardio_intensity)
            ],
            STATES['wait_journal_workout_type']: [
                CallbackQueryHandler(handlers.select_workout_type_journal, pattern='^strength_workout$'),
                CallbackQueryHandler(handlers.select_workout_type_journal, pattern='^cardio_workout$'),
                CallbackQueryHandler(handlers.workout_journal_menu, pattern='^workout_journal$')
            ],
            STATES['wait_journal_date']: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.wait_journal_date)
            ],
            STATES['wait_journal_duration']: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.wait_journal_duration)
            ],
            STATES['wait_journal_activity']: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.wait_journal_activity)
            ],
            STATES['wait_journal_distance']: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.wait_journal_distance)
            ],
            STATES['wait_journal_heart_rate']: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.wait_journal_heart_rate)
            ],
            STATES['wait_journal_feeling']: [
                CallbackQueryHandler(handlers.journal_feeling_selected, pattern='^feeling_[1-9]|10$')
            ],
            STATES['select_exercise']: [
                CallbackQueryHandler(handlers.select_exercise_for_journal, pattern='^select_exercise_'),
                CallbackQueryHandler(handlers.select_exercise_for_journal, pattern='^add_new_exercise$'),
                CallbackQueryHandler(handlers.add_more_sets, pattern='^add_more_sets$'),
                CallbackQueryHandler(handlers.add_more_sets, pattern='^finish_exercise$'),
                CallbackQueryHandler(handlers.add_more_sets, pattern='^finish_workout$'),
                CallbackQueryHandler(handlers.add_another_exercise, pattern='^add_another_exercise$')
            ],
            STATES['wait_set_weight']: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.wait_set_weight)
            ],
            STATES['wait_set_reps']: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.wait_set_reps)
            ],
            STATES['sport_goal']: [
                CallbackQueryHandler(handlers.edit_sport_goal, pattern='^edit_sport_goal$'),
                CallbackQueryHandler(handlers.sport_home, pattern='^sport_home$')
            ],
            STATES['wait_sport_goal']: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.wait_sport_goal)
            ],
            # Состояния для теста правил
            STATES['rules_test_home']: [
                CallbackQueryHandler(rules_test_handlers.rules_test_back, pattern='^rules_test_home$')
            ],
            STATES['rules_test_result']: [
                CallbackQueryHandler(rules_test_handlers.rules_test_all_followed, pattern='^rules_all_followed$'),
                CallbackQueryHandler(rules_test_handlers.rules_test_some_violated, pattern='^rules_some_violated$'),
                CallbackQueryHandler(rules_test_handlers.rules_test_back, pattern='^rules_test_home$')
            ],
            STATES['rules_test_violations']: [
                CallbackQueryHandler(rules_test_handlers.rules_test_violation_selected, pattern='^violation_rule_'),
                CallbackQueryHandler(rules_test_handlers.rules_test_back, pattern='^rules_test_home$')
            ],
            STATES['rules_test_reason']: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, rules_test_handlers.rules_test_reason_received),
                CallbackQueryHandler(rules_test_handlers.rules_test_back, pattern='^rules_test_home$')
            ],
            STATES['rules_test_exception']: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, rules_test_handlers.rules_test_exception_received),
                CallbackQueryHandler(rules_test_handlers.rules_test_back, pattern='^rules_test_home$')
            ],
            # Состояния для анализа
            STATES['analysis_home']: [
                CallbackQueryHandler(analysis_handlers.analysis_create_start, pattern='^create_analysis$'),
                CallbackQueryHandler(analysis_handlers.analysis_collection, pattern='^analysis_collection$'),
                CallbackQueryHandler(analysis_handlers.analysis_back, pattern='^analysis_home$')
            ],
            STATES['analysis_title']: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, analysis_handlers.analysis_title_received),
                CallbackQueryHandler(analysis_handlers.analysis_back, pattern='^analysis_home$')
            ],
            STATES['analysis_situation']: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, analysis_handlers.analysis_situation_received),
                CallbackQueryHandler(analysis_handlers.analysis_back, pattern='^analysis_home$')
            ],
            STATES['analysis_reason']: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, analysis_handlers.analysis_reason_received),
                CallbackQueryHandler(analysis_handlers.analysis_back, pattern='^analysis_home$')
            ],
            STATES['analysis_prevention']: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, analysis_handlers.analysis_prevention_received),
                CallbackQueryHandler(analysis_handlers.analysis_back, pattern='^analysis_home$')
            ],
            STATES['analysis_collection']: [
                CallbackQueryHandler(analysis_handlers.analysis_view, pattern='^view_analysis_'),
                CallbackQueryHandler(analysis_handlers.analysis_back, pattern='^analysis_home$')
            ],
            STATES['analysis_review']: [
                CallbackQueryHandler(analysis_handlers.analysis_review_start, pattern='^review_analysis_'),
                CallbackQueryHandler(analysis_handlers.analysis_helpful, pattern='^analysis_helpful_'),
                CallbackQueryHandler(analysis_handlers.analysis_not_helpful, pattern='^analysis_not_helpful_'),
                CallbackQueryHandler(analysis_handlers.analysis_back, pattern='^analysis_home$'),
                MessageHandler(filters.TEXT & ~filters.COMMAND, analysis_handlers.analysis_alternative_received)
            ]
        },
        fallbacks=[CommandHandler('start', handlers.start)]
    )
    
    return conv_handler



def main():
    """Основная функция запуска бота"""
    update_structure()
    
    # Создаем Application
    bot = Application.builder().token(TG_API).build()
    
    # Добавляем обработчик разговоров
    conv_handler = create_conversation_handler()
    bot.add_handler(conv_handler)
        
    print("Бот запущен...")
    bot.run_polling(allowed_updates=['message', 'callback_query', 'command'])


if __name__ == '__main__':
    main()

