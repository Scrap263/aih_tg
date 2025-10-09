"""
Обработчики для теста правил
"""
from telegram import Update
from telegram.ext import ContextTypes
from datetime import datetime, date
from models import (
    get_rules, create_rule_test, add_rule_violation, 
    get_rule_test_by_date, get_rule_violations_by_test,
    get_rule_violation_history
)
from keyboards.keyboards import (
    get_rules_test_keyboard, get_rules_violations_keyboard,
    get_rules_test_back_keyboard
)
from config import SD_MESSAGES
from states import STATES


async def rules_test_home(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Главное меню теста правил"""
    query = update.callback_query
    await query.answer()
    
    chat_id = query.from_user.id
    today = date.today().strftime('%Y-%m-%d')
    
    # Проверяем, есть ли уже тест на сегодня
    existing_test = get_rule_test_by_date(chat_id, today)
    if existing_test:
        if existing_test.all_rules_followed:
            message = SD_MESSAGES['rules_test_success']
        else:
            violations = get_rule_violations_by_test(existing_test.id)
            message = f"{SD_MESSAGES['rules_test_violations']}\n\n"
            for violation in violations:
                message += f"• {violation.rule.rule_text}\n"
        await query.edit_message_text(
            text=message,
            reply_markup=get_rules_test_back_keyboard()
        )
        return STATES['rules_test_home']
    
    # Получаем активные правила пользователя
    rules = get_rules(chat_id, active_only=True)
    if not rules:
        await query.edit_message_text(
            text="У вас пока нет активных правил. Сначала добавьте правила в разделе 'Правила'.",
            reply_markup=get_rules_test_back_keyboard()
        )
        return STATES['rules_test_home']
    
    await query.edit_message_text(
        text=f"{SD_MESSAGES['rules_test_home']}\n\n{SD_MESSAGES['rules_test_question']}",
        reply_markup=get_rules_test_keyboard()
    )
    return STATES['rules_test_result']


async def rules_test_all_followed(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Все правила соблюдены"""
    query = update.callback_query
    await query.answer()
    
    chat_id = query.from_user.id
    today = date.today().strftime('%Y-%m-%d')
    
    # Создаем запись о том, что все правила соблюдены
    create_rule_test(chat_id, today, True)
    
    await query.edit_message_text(
        text=SD_MESSAGES['rules_test_success'],
        reply_markup=get_rules_test_back_keyboard()
    )
    return STATES['rules_test_home']


async def rules_test_some_violated(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Некоторые правила нарушены"""
    query = update.callback_query
    await query.answer()
    
    chat_id = query.from_user.id
    today = date.today().strftime('%Y-%m-%d')
    
    # Создаем запись о том, что не все правила соблюдены
    rule_test_id = create_rule_test(chat_id, today, False)
    context.user_data['current_rule_test_id'] = rule_test_id
    
    # Получаем активные правила для выбора нарушенных
    rules = get_rules(chat_id, active_only=True)
    
    await query.edit_message_text(
        text=SD_MESSAGES['rules_test_violations'],
        reply_markup=get_rules_violations_keyboard(rules)
    )
    return STATES['rules_test_violations']


async def rules_test_violation_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Выбрано нарушенное правило"""
    query = update.callback_query
    await query.answer()
    
    rule_id = int(query.data.split('_')[-1])
    context.user_data['current_violation_rule_id'] = rule_id
    
    await query.edit_message_text(
        text=SD_MESSAGES['rules_test_reason'],
        reply_markup=get_rules_test_back_keyboard()
    )
    return STATES['rules_test_reason']


async def rules_test_reason_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Получена причина нарушения"""
    reason = update.message.text
    context.user_data['current_violation_reason'] = reason
    
    await update.message.reply_text(
        text=SD_MESSAGES['rules_test_exception'],
        reply_markup=get_rules_test_back_keyboard()
    )
    return STATES['rules_test_exception']


async def rules_test_exception_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Получено исключение из правила"""
    exception = update.message.text
    if exception.lower() in ['нет', 'no', 'не было', 'не было исключений']:
        exception = None
    
    # Сохраняем нарушение
    rule_test_id = context.user_data.get('current_rule_test_id')
    rule_id = context.user_data.get('current_violation_rule_id')
    reason = context.user_data.get('current_violation_reason')
    
    if rule_test_id and rule_id and reason:
        add_rule_violation(rule_test_id, rule_id, reason, exception)
        
        # Очищаем временные данные
        context.user_data.pop('current_violation_rule_id', None)
        context.user_data.pop('current_violation_reason', None)
    
    await update.message.reply_text(
        text=SD_MESSAGES['rules_test_saved'],
        reply_markup=get_rules_test_back_keyboard()
    )
    return STATES['rules_test_home']


async def rules_test_back(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Возврат в главное меню теста правил"""
    query = update.callback_query
    await query.answer()
    
    chat_id = query.from_user.id
    today = date.today().strftime('%Y-%m-%d')
    
    # Проверяем, есть ли уже тест на сегодня
    existing_test = get_rule_test_by_date(chat_id, today)
    if existing_test:
        if existing_test.all_rules_followed:
            message = SD_MESSAGES['rules_test_success']
        else:
            violations = get_rule_violations_by_test(existing_test.id)
            message = f"{SD_MESSAGES['rules_test_violations']}\n\n"
            for violation in violations:
                message += f"• {violation.rule.rule_text}\n"
        await query.edit_message_text(
            text=message,
            reply_markup=get_rules_test_back_keyboard()
        )
        return STATES['rules_test_home']
    
    # Получаем активные правила пользователя
    rules = get_rules(chat_id, active_only=True)
    if not rules:
        await query.edit_message_text(
            text="У вас пока нет активных правил. Сначала добавьте правила в разделе 'Правила'.",
            reply_markup=get_rules_test_back_keyboard()
        )
        return STATES['rules_test_home']
    
    await query.edit_message_text(
        text=f"{SD_MESSAGES['rules_test_home']}\n\n{SD_MESSAGES['rules_test_question']}",
        reply_markup=get_rules_test_keyboard()
    )
    return STATES['rules_test_result']
