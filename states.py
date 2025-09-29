"""
Состояния для ConversationHandler
"""

# Определяем все состояния бота
start_route, dict_maiin, get_en_word, wait_p_s, wait_translation = range(0, 5)
wait_date, start_forced_r, first_ai_answer, wait_right_sent = range(5, 9)
wait_ru_sentance, learn_ox_word, wait_ox_ps, wait_interm_translation = range(9, 13)
wait_interm_sentence, wait_interm_user_translation, interm_ai_review = range(13, 16)
wait_interm_right_sentence, wait_starter_translation, end_starter_state, instructions = range(16, 20)

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
    'end_starter_state': end_starter_state
}

