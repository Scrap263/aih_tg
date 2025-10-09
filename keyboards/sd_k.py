from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from config import SD_CD

def sd_home_kb():
    keyboard = [[InlineKeyboardButton(text='Задачи', callback_data=SD_CD['tasks'])]]

    return InlineKeyboardMarkup(keyboard)

    