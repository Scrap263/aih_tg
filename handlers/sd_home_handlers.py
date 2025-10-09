from telegram import Update
from telegram.ext import ContextTypes
from keyboards import sd_home_kb
from config import SD_MESSAGES
from states import STATES

async def sd_home(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    markup = sd_home_kb()
    text = SD_MESSAGES['sd_home']

    await query.edit_message_text(text=text, reply_markup=markup)
    return STATES['sd_home']