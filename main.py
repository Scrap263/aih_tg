"""
Основной файл запуска Telegram бота
"""
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    filters
)

from config import TG_API, CALLBACK_DATA
from states import STATES
from models import update_structure
import handlers


def create_conversation_handler():
    """Создает ConversationHandler с всеми состояниями и обработчиками"""
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', handlers.start)],
        states={
            STATES['start_route']: [
                CallbackQueryHandler(handlers.dict_home, pattern='^' + CALLBACK_DATA['dict_main'] + '$'),
                CallbackQueryHandler(handlers.instructions, pattern='^' + CALLBACK_DATA['instructions'] + '$')
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
            ]
        },
        fallbacks=[CommandHandler('start', handlers.start)]
    )
    
    return conv_handler


def main():
    """Основная функция запуска бота"""
    # Инициализируем базу данных
    update_structure()
    
    # Создаем приложение бота
    bot = Application.builder().token(TG_API).build()
    
    # Добавляем обработчик разговоров
    conv_handler = create_conversation_handler()
    bot.add_handler(conv_handler)
    
    # Запускаем бота
    print("Бот запущен...")
    bot.run_polling(allowed_updates=['message', 'callback_query'])


if __name__ == '__main__':
    main()

