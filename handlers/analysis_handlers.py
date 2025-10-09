"""
Обработчики для анализа ситуаций
"""
from telegram import Update
from telegram.ext import ContextTypes
from models import (
    create_analysis, get_analyses, get_analysis_by_id,
    add_analysis_review, get_analysis_reviews
)
from keyboards.keyboards import (
    get_analysis_menu_keyboard, get_analyses_list_keyboard,
    get_analysis_detail_keyboard, get_analysis_review_keyboard,
    get_analysis_back_keyboard
)
from config import SD_MESSAGES
from states import STATES


async def analysis_home(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Главное меню анализа"""
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_text(
        text=SD_MESSAGES['analysis_home'],
        reply_markup=get_analysis_menu_keyboard()
    )
    return STATES['analysis_home']


async def analysis_create_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Начало создания анализа"""
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_text(
        text=SD_MESSAGES['analysis_create'],
        reply_markup=get_analysis_back_keyboard()
    )
    return STATES['analysis_title']


async def analysis_title_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Получено название анализа"""
    title = update.message.text
    context.user_data['analysis_title'] = title
    
    await update.message.reply_text(
        text=SD_MESSAGES['analysis_situation'],
        reply_markup=get_analysis_back_keyboard()
    )
    return STATES['analysis_situation']


async def analysis_situation_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Получено описание ситуации"""
    situation = update.message.text
    context.user_data['analysis_situation'] = situation
    
    await update.message.reply_text(
        text=SD_MESSAGES['analysis_reason'],
        reply_markup=get_analysis_back_keyboard()
    )
    return STATES['analysis_reason']


async def analysis_reason_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Получено описание причин"""
    reason = update.message.text
    context.user_data['analysis_reason'] = reason
    
    await update.message.reply_text(
        text=SD_MESSAGES['analysis_prevention'],
        reply_markup=get_analysis_back_keyboard()
    )
    return STATES['analysis_prevention']


async def analysis_prevention_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Получено описание способов предотвращения"""
    prevention = update.message.text
    
    # Создаем анализ
    chat_id = update.effective_user.id
    title = context.user_data.get('analysis_title')
    situation = context.user_data.get('analysis_situation')
    reason = context.user_data.get('analysis_reason')
    
    if title and situation and reason:
        analysis_id = create_analysis(chat_id, title, situation, reason, prevention)
        
        # Очищаем временные данные
        context.user_data.pop('analysis_title', None)
        context.user_data.pop('analysis_situation', None)
        context.user_data.pop('analysis_reason', None)
        
        await update.message.reply_text(
            text=SD_MESSAGES['analysis_created'],
            reply_markup=get_analysis_back_keyboard()
        )
    else:
        await update.message.reply_text(
            text="Ошибка при создании анализа. Попробуйте еще раз.",
            reply_markup=get_analysis_back_keyboard()
        )
    
    return STATES['analysis_home']


async def analysis_collection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Сборник анализов"""
    query = update.callback_query
    await query.answer()
    
    chat_id = query.from_user.id
    analyses = get_analyses(chat_id, limit=20)
    
    if not analyses:
        await query.edit_message_text(
            text="У вас пока нет анализов. Создайте первый анализ!",
            reply_markup=get_analysis_back_keyboard()
        )
        return STATES['analysis_home']
    
    message = f"{SD_MESSAGES['analysis_collection']}\n\n"
    for i, analysis in enumerate(analyses, 1):
        message += f"{i}. {analysis.title}\n"
    
    await query.edit_message_text(
        text=message,
        reply_markup=get_analyses_list_keyboard(analyses)
    )
    return STATES['analysis_collection']


async def analysis_view(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Просмотр конкретного анализа"""
    query = update.callback_query
    await query.answer()
    
    analysis_id = int(query.data.split('_')[-1])
    analysis = get_analysis_by_id(analysis_id)
    
    if not analysis:
        await query.edit_message_text(
            text="Анализ не найден.",
            reply_markup=get_analysis_back_keyboard()
        )
        return STATES['analysis_home']
    
    message = f"📄 {analysis.title}\n\n"
    message += f"📝 Что произошло:\n{analysis.situation}\n\n"
    message += f"🤔 Почему это произошло:\n{analysis.reason}\n\n"
    message += f"💡 Как не допустить в будущем:\n{analysis.prevention}\n\n"
    message += f"📅 Создан: {analysis.created_at.strftime('%d.%m.%Y %H:%M')}"
    
    await query.edit_message_text(
        text=message,
        reply_markup=get_analysis_detail_keyboard(analysis_id)
    )
    return STATES['analysis_review']


async def analysis_review_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Начало оценки анализа"""
    query = update.callback_query
    await query.answer()
    
    analysis_id = int(query.data.split('_')[-1])
    context.user_data['current_analysis_id'] = analysis_id
    
    await query.edit_message_text(
        text=SD_MESSAGES['analysis_review'],
        reply_markup=get_analysis_review_keyboard(analysis_id)
    )
    return STATES['analysis_review']


async def analysis_helpful(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Анализ помог"""
    query = update.callback_query
    await query.answer()
    
    analysis_id = context.user_data.get('current_analysis_id')
    chat_id = query.from_user.id
    
    if analysis_id:
        add_analysis_review(analysis_id, chat_id, True)
        context.user_data.pop('current_analysis_id', None)
        
        await query.edit_message_text(
            text=SD_MESSAGES['analysis_helpful'],
            reply_markup=get_analysis_back_keyboard()
        )
    else:
        await query.edit_message_text(
            text="Ошибка при сохранении оценки.",
            reply_markup=get_analysis_back_keyboard()
        )
    
    return STATES['analysis_home']


async def analysis_not_helpful(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Анализ не помог"""
    query = update.callback_query
    await query.answer()
    
    analysis_id = context.user_data.get('current_analysis_id')
    context.user_data['waiting_for_alternative'] = True
    
    await query.edit_message_text(
        text=SD_MESSAGES['analysis_not_helpful'] + "\n\n" + SD_MESSAGES['analysis_alternative'],
        reply_markup=get_analysis_back_keyboard()
    )
    return STATES['analysis_review']


async def analysis_alternative_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Получено альтернативное решение"""
    alternative_solution = update.message.text
    analysis_id = context.user_data.get('current_analysis_id')
    chat_id = update.effective_user.id
    
    if analysis_id:
        add_analysis_review(analysis_id, chat_id, False, alternative_solution)
        
        # Очищаем временные данные
        context.user_data.pop('current_analysis_id', None)
        context.user_data.pop('waiting_for_alternative', None)
        
        await update.message.reply_text(
            text=SD_MESSAGES['analysis_review_saved'],
            reply_markup=get_analysis_back_keyboard()
        )
    else:
        await update.message.reply_text(
            text="Ошибка при сохранении оценки.",
            reply_markup=get_analysis_back_keyboard()
        )
    
    return STATES['analysis_home']


async def analysis_back(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Возврат в главное меню анализа"""
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_text(
        text=SD_MESSAGES['analysis_home'],
        reply_markup=get_analysis_menu_keyboard()
    )
    return STATES['analysis_home']
