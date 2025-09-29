"""
Вспомогательные функции для бота
"""
import json
import random
from datetime import datetime
from config import DATA_FILES


def load_dictionary():
    """Загружает словарь из JSON файла"""
    with open(DATA_FILES['dictionary'], 'r', encoding='UTF-8') as f:
        return json.load(f)


def load_oxford_words():
    """Загружает список слов Oxford 3000"""
    with open(DATA_FILES['words_list'], 'r') as f:
        return json.load(f)


def get_random_oxford_words(count=5):
    """Получает случайные слова из Oxford 3000"""
    oxford_words = load_oxford_words()
    words_list = []
    while len(words_list) < count:
        random_int = random.randint(0, 2800)
        word = oxford_words[random_int]
        if word not in words_list:
            words_list.append(word)
    return words_list


def shuffle_sentence_words(words_list):
    """Перемешивает слова в предложении"""
    words_text = ''
    number = len(words_list)
    words_copy = words_list.copy()
    
    while number != 0:
        r_int = random.randint(0, number - 1)
        w = words_copy.pop(r_int)
        words_text += w + ' | '
        number -= 1
    
    return words_text


def format_words_for_review(words):
    """Форматирует список слов для отображения"""
    if not words:
        return ""
    
    words_text = ""
    for word_data in words:
        words_text += f"\n{word_data['word']}"
    return words_text


def get_today_date():
    """Возвращает сегодняшнюю дату в строковом формате"""
    return str(datetime.today().date())


def format_word_info(word, part_of_speech, translation):
    """Форматирует информацию о слове"""
    return f"Слово для повторения: {word} ({part_of_speech}).\n\nНапишите перевод этого слова (необязательно все, можно только то что помните)"


def format_correct_translation(word, translations):
    """Форматирует сообщение о правильном переводе"""
    return f"Круто! Вы правильно перевели слово {word}. Вот все переводы этого слова: {translations}.\n\nХотите продолжить повторение слов?"


def format_incorrect_translation(word, translations):
    """Форматирует сообщение о неправильном переводе"""
    return f"Вы хорошо справляетесь. {word} может переводится как {translations}.\n\n Хотите продолжить повторение слов?"


def format_sentence_task(words_text):
    """Форматирует задание с предложением"""
    return f"Теперь двигаемся дальше. Ниже приведены слова которые нужно расположить в правильном порядке и получится предложение\n\nВот слова: [{words_text}]\nНапишите получившееся предложение"


def format_oxford_word_info(word, transcription, part_of_speech_text):
    """Форматирует информацию о слове из Oxford"""
    return f"Слово {word} читается как - {transcription}. Внизу на кнопках написаны части речи в которых это слово может быть использовано.\n\nНажмите на кнопку, чтобы понять как это слово используется"

