from sqlalchemy.orm import Session
from sqlalchemy import create_engine, or_, Date, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, DeclarativeBase, relationship
from datetime import datetime, date, timedelta
from typing import Optional

engine = create_engine('sqlite:///test.db')

#Содаем базовый класс для всех моделей
class Base(DeclarativeBase):
    pass

class Word(Base):
    __tablename__ = 'user_words'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(nullable=False, index=True)
    en_word: Mapped[str] = mapped_column(nullable=False)
    p_speech: Mapped[str] = mapped_column(nullable=False)
    transl: Mapped[str] = mapped_column(nullable=False)
    date_created: Mapped[date] = mapped_column(Date, default=date.today())
    r_1: Mapped[str] = mapped_column(nullable=False)
    r_2: Mapped[str] = mapped_column(nullable=False)
    r_3: Mapped[str] = mapped_column(nullable=False)
    r_4: Mapped[str] = mapped_column(nullable=False)
    r_5: Mapped[str] = mapped_column(nullable=False)
    sentances: Mapped[list['Sentances']] = relationship(back_populates='word')


class Sentances(Base):
    __tablename__ = 'english_sentances'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    chat_id: Mapped[int] = mapped_column(ForeignKey('user_words.user_id'))
    sentance: Mapped[str] = mapped_column(nullable=False, default='Sentance wasnt saved')

    word : Mapped['Word'] = relationship(back_populates='sentances')

class Tasks(Base):
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    date : Mapped[str] = mapped_column(nullable=False)
    chat_id: Mapped[int] = mapped_column(nullable=False)
    text: Mapped[str] = mapped_column(nullable=False)
    completed: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)

# Модели для питания
class Dish(Base):
    __tablename__ = 'dishes'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    calories_per_100g: Mapped[float] = mapped_column(nullable=False)
    protein_per_100g: Mapped[float] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)

class Meal(Base):
    __tablename__ = 'meals'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    chat_id: Mapped[int] = mapped_column(nullable=False)
    date: Mapped[str] = mapped_column(nullable=False)
    total_calories: Mapped[float] = mapped_column(default=0.0)
    total_protein: Mapped[float] = mapped_column(default=0.0)
    is_completed: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    meal_items: Mapped[list['MealItem']] = relationship(back_populates='meal')

class MealItem(Base):
    __tablename__ = 'meal_items'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    meal_id: Mapped[int] = mapped_column(ForeignKey('meals.id'))
    dish_id: Mapped[int] = mapped_column(ForeignKey('dishes.id'))
    grams: Mapped[float] = mapped_column(nullable=False)
    calories: Mapped[float] = mapped_column(nullable=False)
    protein: Mapped[float] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    
    meal: Mapped['Meal'] = relationship(back_populates='meal_items')
    dish: Mapped['Dish'] = relationship()

class NutritionGoal(Base):
    __tablename__ = 'nutrition_goals'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    chat_id: Mapped[int] = mapped_column(nullable=False, unique=True)
    daily_calories: Mapped[float] = mapped_column(nullable=False)
    daily_protein: Mapped[float] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now)

class NutritionRule(Base):
    __tablename__ = 'nutrition_rules'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    chat_id: Mapped[int] = mapped_column(nullable=False)
    rule_text: Mapped[str] = mapped_column(nullable=False)
    reminder_time: Mapped[Optional[str]] = mapped_column(nullable=True)
    exceptions: Mapped[Optional[str]] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)

class NutritionNote(Base):
    __tablename__ = 'nutrition_notes'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    chat_id: Mapped[int] = mapped_column(nullable=False)
    note_text: Mapped[str] = mapped_column(nullable=False)
    date: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)


def update_structure():
    Base.metadata.create_all(engine)

def add_word(chat_id, en_word, p_speech, transl):
    today = datetime.today().date()
    r_1 = today + timedelta(1)
    r_2 = today + timedelta(3)
    r_3 = today + timedelta(7)
    r_4 = today + timedelta(14)
    r_5 = today + timedelta(28)
    with Session(engine) as session:
        word = Word(user_id=chat_id, en_word=en_word, p_speech=p_speech, transl=transl, r_1=r_1, r_2=r_2, r_3=r_3, r_4=r_4, r_5=r_5)
        session.add(word)
        session.commit()

def add_sentance(chat_id, sentance):
    with Session(engine) as session:
        sent = Sentances(chat_id=chat_id, sentance=sentance)
        session.add(sent)
        session.commit()

def find_words_for_r(chat_id, date):
    with Session(engine) as session:
        word = session.query(Word).filter( Word.user_id == chat_id, or_(
            Word.r_1 == date,
            Word.r_2 == date,
            Word.r_3 == date,
            Word.r_4 == date,
            Word.r_5 == date
        )).all()
        message = []
        for each in word:
            w = each.en_word
            p_s = each.p_speech
            trans = each.transl
            w_d = {'word': w, 's_part': p_s, 'translation': trans}
            message.append(w_d)
        return message
    
def update_reviewed_word(chat_id, word):
    today = str(datetime.today().date())
    columns = ['r_1', 'r_2', 'r_3', 'r_4', 'r_5']
    print(word)

    with Session(engine) as session:
        w_t_u = session.query(Word).filter(Word.user_id == chat_id, Word.en_word == word).first()
        for column in columns:
            if getattr(w_t_u, column) == today:
                setattr(w_t_u, column, 'reviewed')
                break
        session.commit()

def forced_review(chat_id, date):
    with Session(engine) as session:
        words = session.query(Word).filter(Word.user_id == chat_id, Word.date_created == date).all()
        print(words)
        message = []
        for each in words:
            w = each.en_word
            p_s = each.p_speech
            trans = each.transl
            w_d = {'word': w, 's_part': p_s, 'translation': trans}
            message.append(w_d)
        return message

def find_user_words(chat_id):
    with Session(engine) as session:
        words = session.query(Word).filter(Word.user_id == chat_id).all
        words_list = []
        for row in words:
            word = row.en_word
            words_list.append(word)
        return words_list

# Функции для работы с питанием
def add_dish(name, calories_per_100g, protein_per_100g):
    with Session(engine) as session:
        dish = Dish(name=name, calories_per_100g=calories_per_100g, protein_per_100g=protein_per_100g)
        session.add(dish)
        session.commit()
        return dish.id

def get_all_dishes():
    with Session(engine) as session:
        dishes = session.query(Dish).all()
        return dishes

def get_dish_by_id(dish_id):
    with Session(engine) as session:
        dish = session.query(Dish).filter(Dish.id == dish_id).first()
        return dish

def create_meal(chat_id, date):
    with Session(engine) as session:
        meal = Meal(chat_id=chat_id, date=date)
        session.add(meal)
        session.commit()
        return meal.id

def get_current_meal(chat_id, date):
    with Session(engine) as session:
        meal = session.query(Meal).filter(
            Meal.chat_id == chat_id, 
            Meal.date == date, 
            Meal.is_completed == False
        ).first()
        return meal

def add_meal_item(meal_id, dish_id, grams):
    with Session(engine) as session:
        dish = session.query(Dish).filter(Dish.id == dish_id).first()
        if dish:
            calories = (dish.calories_per_100g * grams) / 100
            protein = (dish.protein_per_100g * grams) / 100
            
            meal_item = MealItem(
                meal_id=meal_id,
                dish_id=dish_id,
                grams=grams,
                calories=calories,
                protein=protein
            )
            session.add(meal_item)
            
            # Обновляем общие калории и белок в приёме пищи
            meal = session.query(Meal).filter(Meal.id == meal_id).first()
            meal.total_calories += calories
            meal.total_protein += protein
            
            session.commit()
            return meal_item.id
        return None

def complete_meal(meal_id):
    with Session(engine) as session:
        meal = session.query(Meal).filter(Meal.id == meal_id).first()
        if meal:
            meal.is_completed = True
            session.commit()
            return True
        return False

def set_nutrition_goal(chat_id, daily_calories, daily_protein):
    with Session(engine) as session:
        goal = session.query(NutritionGoal).filter(NutritionGoal.chat_id == chat_id).first()
        if goal:
            goal.daily_calories = daily_calories
            goal.daily_protein = daily_protein
            goal.updated_at = datetime.now()
        else:
            goal = NutritionGoal(
                chat_id=chat_id,
                daily_calories=daily_calories,
                daily_protein=daily_protein
            )
            session.add(goal)
        session.commit()
        return goal.id

def get_nutrition_goal(chat_id):
    with Session(engine) as session:
        goal = session.query(NutritionGoal).filter(NutritionGoal.chat_id == chat_id).first()
        return goal

def add_nutrition_rule(chat_id, rule_text, reminder_time=None, exceptions=None):
    with Session(engine) as session:
        rule = NutritionRule(
            chat_id=chat_id,
            rule_text=rule_text,
            reminder_time=reminder_time,
            exceptions=exceptions
        )
        session.add(rule)
        session.commit()
        return rule.id

def get_nutrition_rules(chat_id):
    with Session(engine) as session:
        rules = session.query(NutritionRule).filter(NutritionRule.chat_id == chat_id).all()
        return rules

def add_nutrition_note(chat_id, note_text, date):
    with Session(engine) as session:
        note = NutritionNote(
            chat_id=chat_id,
            note_text=note_text,
            date=date
        )
        session.add(note)
        session.commit()
        return note.id

def get_nutrition_notes(chat_id, date=None):
    with Session(engine) as session:
        query = session.query(NutritionNote).filter(NutritionNote.chat_id == chat_id)
        if date:
            query = query.filter(NutritionNote.date == date)
        notes = query.all()
        return notes

def get_meals_by_date(chat_id, date):
    """Получить все приёмы пищи за конкретную дату"""
    with Session(engine) as session:
        meals = session.query(Meal).filter(
            Meal.chat_id == chat_id,
            Meal.date == date,
            Meal.is_completed == True
        ).all()
        return meals

def get_meal_items_with_dishes(meal_id):
    """Получить все блюда приёма пищи с информацией о блюдах"""
    with Session(engine) as session:
        meal_items = session.query(MealItem).filter(MealItem.meal_id == meal_id).all()
        return meal_items

def get_nutrition_summary_by_date(chat_id, date):
    """Получить сводку по питанию за конкретную дату"""
    meals = get_meals_by_date(chat_id, date)
    
    total_calories = 0
    total_protein = 0
    meals_data = []
    
    for meal in meals:
        meal_items = get_meal_items_with_dishes(meal.id)
        meal_data = {
            'meal_id': meal.id,
            'created_at': meal.created_at,
            'total_calories': meal.total_calories,
            'total_protein': meal.total_protein,
            'items': []
        }
        
        for item in meal_items:
            item_data = {
                'dish_name': item.dish.name,
                'grams': item.grams,
                'calories': item.calories,
                'protein': item.protein
            }
            meal_data['items'].append(item_data)
        
        meals_data.append(meal_data)
        total_calories += meal.total_calories
        total_protein += meal.total_protein
    
    return {
        'date': date,
        'total_calories': total_calories,
        'total_protein': total_protein,
        'meals_count': len(meals),
        'meals': meals_data
    }

# Модели для рутин
class MorningRoutine(Base):
    __tablename__ = 'morning_routines'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    chat_id: Mapped[int] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    actions: Mapped[str] = mapped_column(nullable=False)  # JSON строка с последовательностью действий
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)

class EveningRoutine(Base):
    __tablename__ = 'evening_routines'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    chat_id: Mapped[int] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    actions: Mapped[str] = mapped_column(nullable=False)  # JSON строка с последовательностью действий
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)

class RoutineProgress(Base):
    __tablename__ = 'routine_progress'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    chat_id: Mapped[int] = mapped_column(nullable=False)
    routine_type: Mapped[str] = mapped_column(nullable=False)  # 'morning' или 'evening'
    routine_id: Mapped[int] = mapped_column(nullable=False)
    current_action_index: Mapped[int] = mapped_column(default=0)
    is_completed: Mapped[bool] = mapped_column(default=False)
    date: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)

class MorningTesting(Base):
    __tablename__ = 'morning_testing'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    chat_id: Mapped[int] = mapped_column(nullable=False)
    date: Mapped[str] = mapped_column(nullable=False)
    sleep_hours: Mapped[float] = mapped_column(nullable=False)
    wake_up_count: Mapped[int] = mapped_column(nullable=False)
    health_condition: Mapped[int] = mapped_column(nullable=False)  # от 1 до 10
    muscle_fatigue: Mapped[int] = mapped_column(nullable=False)  # от 1 до 10
    health_complaints: Mapped[Optional[str]] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)

# Модель для общих правил
class Rule(Base):
    __tablename__ = 'rules'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    chat_id: Mapped[int] = mapped_column(nullable=False)
    rule_text: Mapped[str] = mapped_column(nullable=False)
    reminder_time: Mapped[Optional[str]] = mapped_column(nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now)

# Функции для работы с рутинами
def create_morning_routine(chat_id, name, actions):
    with Session(engine) as session:
        routine = MorningRoutine(
            chat_id=chat_id,
            name=name,
            actions=actions
        )
        session.add(routine)
        session.commit()
        return routine.id

def create_evening_routine(chat_id, name, actions):
    with Session(engine) as session:
        routine = EveningRoutine(
            chat_id=chat_id,
            name=name,
            actions=actions
        )
        session.add(routine)
        session.commit()
        return routine.id

def get_morning_routines(chat_id):
    with Session(engine) as session:
        routines = session.query(MorningRoutine).filter(
            MorningRoutine.chat_id == chat_id,
            MorningRoutine.is_active == True
        ).all()
        return routines

def get_evening_routines(chat_id):
    with Session(engine) as session:
        routines = session.query(EveningRoutine).filter(
            EveningRoutine.chat_id == chat_id,
            EveningRoutine.is_active == True
        ).all()
        return routines

def get_routine_by_id(routine_type, routine_id):
    with Session(engine) as session:
        if routine_type == 'morning':
            routine = session.query(MorningRoutine).filter(MorningRoutine.id == routine_id).first()
        else:
            routine = session.query(EveningRoutine).filter(EveningRoutine.id == routine_id).first()
        return routine

def create_routine_progress(chat_id, routine_type, routine_id, date):
    with Session(engine) as session:
        progress = RoutineProgress(
            chat_id=chat_id,
            routine_type=routine_type,
            routine_id=routine_id,
            date=date
        )
        session.add(progress)
        session.commit()
        return progress.id

def get_routine_progress(chat_id, routine_type, date):
    with Session(engine) as session:
        progress = session.query(RoutineProgress).filter(
            RoutineProgress.chat_id == chat_id,
            RoutineProgress.routine_type == routine_type,
            RoutineProgress.date == date,
            RoutineProgress.is_completed == False
        ).first()
        return progress

def update_routine_progress(progress_id, current_action_index, is_completed=False):
    with Session(engine) as session:
        progress = session.query(RoutineProgress).filter(RoutineProgress.id == progress_id).first()
        if progress:
            progress.current_action_index = current_action_index
            progress.is_completed = is_completed
            session.commit()
            return True
        return False

def save_morning_testing(chat_id, date, sleep_hours, wake_up_count, health_condition, muscle_fatigue, health_complaints=None):
    with Session(engine) as session:
        testing = MorningTesting(
            chat_id=chat_id,
            date=date,
            sleep_hours=sleep_hours,
            wake_up_count=wake_up_count,
            health_condition=health_condition,
            muscle_fatigue=muscle_fatigue,
            health_complaints=health_complaints
        )
        session.add(testing)
        session.commit()
        return testing.id

def get_morning_testing(chat_id, date):
    with Session(engine) as session:
        testing = session.query(MorningTesting).filter(
            MorningTesting.chat_id == chat_id,
            MorningTesting.date == date
        ).first()
        return testing

# Функции для работы с правилами
def add_rule(chat_id, rule_text, reminder_time=None):
    with Session(engine) as session:
        rule = Rule(
            chat_id=chat_id,
            rule_text=rule_text,
            reminder_time=reminder_time
        )
        session.add(rule)
        session.commit()
        return rule.id

def get_rules(chat_id, active_only=True):
    with Session(engine) as session:
        query = session.query(Rule).filter(Rule.chat_id == chat_id)
        if active_only:
            query = query.filter(Rule.is_active == True)
        rules = query.order_by(Rule.created_at.desc()).all()
        return rules

def get_rule_by_id(rule_id):
    with Session(engine) as session:
        rule = session.query(Rule).filter(Rule.id == rule_id).first()
        return rule

def update_rule(rule_id, rule_text=None, reminder_time=None, is_active=None):
    with Session(engine) as session:
        rule = session.query(Rule).filter(Rule.id == rule_id).first()
        if rule:
            if rule_text is not None:
                rule.rule_text = rule_text
            if reminder_time is not None:
                rule.reminder_time = reminder_time
            if is_active is not None:
                rule.is_active = is_active
            rule.updated_at = datetime.now()
            session.commit()
            return True
        return False

def delete_rule(rule_id):
    with Session(engine) as session:
        rule = session.query(Rule).filter(Rule.id == rule_id).first()
        if rule:
            session.delete(rule)
            session.commit()
            return True
        return False

def toggle_rule_status(rule_id):
    with Session(engine) as session:
        rule = session.query(Rule).filter(Rule.id == rule_id).first()
        if rule:
            rule.is_active = not rule.is_active
            rule.updated_at = datetime.now()
            session.commit()
            return rule.is_active
        return None

# Модели для спорта
class Exercise(Base):
    __tablename__ = 'exercises'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)

class WorkoutPlan(Base):
    __tablename__ = 'workout_plans'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    chat_id: Mapped[int] = mapped_column(nullable=False)
    date: Mapped[str] = mapped_column(nullable=False)
    workout_type: Mapped[str] = mapped_column(nullable=False)  # 'cardio' или 'strength'
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    
    # Для силовых тренировок
    strength_exercises: Mapped[list['StrengthExercise']] = relationship(back_populates='workout_plan')
    
    # Для кардио тренировок
    cardio_details: Mapped[Optional['CardioDetails']] = relationship(back_populates='workout_plan')

class StrengthExercise(Base):
    __tablename__ = 'strength_exercises'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    workout_plan_id: Mapped[int] = mapped_column(ForeignKey('workout_plans.id'))
    exercise_id: Mapped[int] = mapped_column(ForeignKey('exercises.id'))
    sets: Mapped[int] = mapped_column(nullable=False)
    weight: Mapped[float] = mapped_column(nullable=False)
    reps: Mapped[int] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    
    workout_plan: Mapped['WorkoutPlan'] = relationship(back_populates='strength_exercises')
    exercise: Mapped['Exercise'] = relationship()

class CardioDetails(Base):
    __tablename__ = 'cardio_details'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    workout_plan_id: Mapped[int] = mapped_column(ForeignKey('workout_plans.id'))
    duration: Mapped[int] = mapped_column(nullable=False)  # в минутах
    distance: Mapped[float] = mapped_column(nullable=False)  # в километрах
    target_intensity: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    
    workout_plan: Mapped['WorkoutPlan'] = relationship(back_populates='cardio_details')

class WorkoutJournal(Base):
    __tablename__ = 'workout_journal'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    chat_id: Mapped[int] = mapped_column(nullable=False)
    date: Mapped[str] = mapped_column(nullable=False)
    workout_type: Mapped[str] = mapped_column(nullable=False)  # 'cardio' или 'strength'
    duration: Mapped[int] = mapped_column(nullable=False)  # в минутах
    overall_feeling: Mapped[int] = mapped_column(nullable=False)  # от 1 до 10
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    
    # Для кардио
    activity: Mapped[Optional[str]] = mapped_column(nullable=True)
    distance: Mapped[Optional[float]] = mapped_column(nullable=True)
    avg_heart_rate: Mapped[Optional[int]] = mapped_column(nullable=True)
    
    # Для силовых
    strength_sets: Mapped[list['StrengthSet']] = relationship(back_populates='workout_journal')

class StrengthSet(Base):
    __tablename__ = 'strength_sets'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    workout_journal_id: Mapped[int] = mapped_column(ForeignKey('workout_journal.id'))
    exercise_id: Mapped[int] = mapped_column(ForeignKey('exercises.id'))
    weight: Mapped[float] = mapped_column(nullable=False)
    reps: Mapped[int] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    
    workout_journal: Mapped['WorkoutJournal'] = relationship(back_populates='strength_sets')
    exercise: Mapped['Exercise'] = relationship()

class SportGoal(Base):
    __tablename__ = 'sport_goals'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    chat_id: Mapped[int] = mapped_column(nullable=False, unique=True)
    goal_text: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now)

# Функции для работы со спортом
def add_exercise(name):
    with Session(engine) as session:
        exercise = Exercise(name=name)
        session.add(exercise)
        session.commit()
        return exercise.id

def get_all_exercises():
    with Session(engine) as session:
        exercises = session.query(Exercise).all()
        return exercises

def get_exercise_by_id(exercise_id):
    with Session(engine) as session:
        exercise = session.query(Exercise).filter(Exercise.id == exercise_id).first()
        return exercise

def create_workout_plan(chat_id, date, workout_type):
    with Session(engine) as session:
        plan = WorkoutPlan(chat_id=chat_id, date=date, workout_type=workout_type)
        session.add(plan)
        session.commit()
        return plan.id

def add_strength_exercise_to_plan(workout_plan_id, exercise_id, sets, weight, reps):
    with Session(engine) as session:
        strength_exercise = StrengthExercise(
            workout_plan_id=workout_plan_id,
            exercise_id=exercise_id,
            sets=sets,
            weight=weight,
            reps=reps
        )
        session.add(strength_exercise)
        session.commit()
        return strength_exercise.id

def add_cardio_details_to_plan(workout_plan_id, duration, distance, target_intensity):
    with Session(engine) as session:
        cardio_details = CardioDetails(
            workout_plan_id=workout_plan_id,
            duration=duration,
            distance=distance,
            target_intensity=target_intensity
        )
        session.add(cardio_details)
        session.commit()
        return cardio_details.id

def get_workout_plans_by_date(chat_id, date):
    with Session(engine) as session:
        plans = session.query(WorkoutPlan).filter(
            WorkoutPlan.chat_id == chat_id,
            WorkoutPlan.date == date
        ).all()
        return plans

def create_workout_journal_entry(chat_id, date, workout_type, duration, overall_feeling, 
                                activity=None, distance=None, avg_heart_rate=None):
    with Session(engine) as session:
        journal_entry = WorkoutJournal(
            chat_id=chat_id,
            date=date,
            workout_type=workout_type,
            duration=duration,
            overall_feeling=overall_feeling,
            activity=activity,
            distance=distance,
            avg_heart_rate=avg_heart_rate
        )
        session.add(journal_entry)
        session.commit()
        return journal_entry.id

def add_strength_set_to_journal(workout_journal_id, exercise_id, weight, reps):
    with Session(engine) as session:
        strength_set = StrengthSet(
            workout_journal_id=workout_journal_id,
            exercise_id=exercise_id,
            weight=weight,
            reps=reps
        )
        session.add(strength_set)
        session.commit()
        return strength_set.id

def set_sport_goal(chat_id, goal_text):
    with Session(engine) as session:
        goal = session.query(SportGoal).filter(SportGoal.chat_id == chat_id).first()
        if goal:
            goal.goal_text = goal_text
            goal.updated_at = datetime.now()
        else:
            goal = SportGoal(chat_id=chat_id, goal_text=goal_text)
            session.add(goal)
        session.commit()
        return goal.id

def get_sport_goal(chat_id):
    with Session(engine) as session:
        goal = session.query(SportGoal).filter(SportGoal.chat_id == chat_id).first()
        return goal

def get_workout_journal_by_date(chat_id, date):
    with Session(engine) as session:
        journal_entries = session.query(WorkoutJournal).filter(
            WorkoutJournal.chat_id == chat_id,
            WorkoutJournal.date == date
        ).all()
        return journal_entries

def get_strength_sets_by_journal(workout_journal_id):
    with Session(engine) as session:
        sets = session.query(StrengthSet).filter(
            StrengthSet.workout_journal_id == workout_journal_id
        ).all()
        return sets

# Модели для теста правил
class RuleTest(Base):
    __tablename__ = 'rule_tests'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    chat_id: Mapped[int] = mapped_column(nullable=False)
    date: Mapped[str] = mapped_column(nullable=False)
    all_rules_followed: Mapped[bool] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)

class RuleViolation(Base):
    __tablename__ = 'rule_violations'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    rule_test_id: Mapped[int] = mapped_column(ForeignKey('rule_tests.id'))
    rule_id: Mapped[int] = mapped_column(ForeignKey('rules.id'))
    reason: Mapped[str] = mapped_column(nullable=False)
    exception: Mapped[Optional[str]] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    
    rule_test: Mapped['RuleTest'] = relationship()
    rule: Mapped['Rule'] = relationship()

# Модели для анализа
class Analysis(Base):
    __tablename__ = 'analyses'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    chat_id: Mapped[int] = mapped_column(nullable=False)
    title: Mapped[str] = mapped_column(nullable=False)
    situation: Mapped[str] = mapped_column(nullable=False)  # Что произошло
    reason: Mapped[str] = mapped_column(nullable=False)  # Почему это произошло
    prevention: Mapped[str] = mapped_column(nullable=False)  # Как не допустить в будущем
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)

class AnalysisReview(Base):
    __tablename__ = 'analysis_reviews'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    analysis_id: Mapped[int] = mapped_column(ForeignKey('analyses.id'))
    chat_id: Mapped[int] = mapped_column(nullable=False)
    was_helpful: Mapped[bool] = mapped_column(nullable=False)
    alternative_solution: Mapped[Optional[str]] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    
    analysis: Mapped['Analysis'] = relationship()

# Функции для работы с тестом правил
def create_rule_test(chat_id, date, all_rules_followed):
    with Session(engine) as session:
        rule_test = RuleTest(
            chat_id=chat_id,
            date=date,
            all_rules_followed=all_rules_followed
        )
        session.add(rule_test)
        session.commit()
        return rule_test.id

def add_rule_violation(rule_test_id, rule_id, reason, exception=None):
    with Session(engine) as session:
        violation = RuleViolation(
            rule_test_id=rule_test_id,
            rule_id=rule_id,
            reason=reason,
            exception=exception
        )
        session.add(violation)
        session.commit()
        return violation.id

def get_rule_test_by_date(chat_id, date):
    with Session(engine) as session:
        rule_test = session.query(RuleTest).filter(
            RuleTest.chat_id == chat_id,
            RuleTest.date == date
        ).first()
        return rule_test

def get_rule_violations_by_test(rule_test_id):
    with Session(engine) as session:
        violations = session.query(RuleViolation).filter(
            RuleViolation.rule_test_id == rule_test_id
        ).all()
        return violations

def get_rule_violation_history(rule_id, limit=10):
    """Получить историю нарушений конкретного правила"""
    with Session(engine) as session:
        violations = session.query(RuleViolation).filter(
            RuleViolation.rule_id == rule_id
        ).order_by(RuleViolation.created_at.desc()).limit(limit).all()
        return violations

# Функции для работы с анализом
def create_analysis(chat_id, title, situation, reason, prevention):
    with Session(engine) as session:
        analysis = Analysis(
            chat_id=chat_id,
            title=title,
            situation=situation,
            reason=reason,
            prevention=prevention
        )
        session.add(analysis)
        session.commit()
        return analysis.id

def get_analyses(chat_id, limit=20):
    with Session(engine) as session:
        analyses = session.query(Analysis).filter(
            Analysis.chat_id == chat_id
        ).order_by(Analysis.created_at.desc()).limit(limit).all()
        return analyses

def get_analysis_by_id(analysis_id):
    with Session(engine) as session:
        analysis = session.query(Analysis).filter(
            Analysis.id == analysis_id
        ).first()
        return analysis

def add_analysis_review(analysis_id, chat_id, was_helpful, alternative_solution=None):
    with Session(engine) as session:
        review = AnalysisReview(
            analysis_id=analysis_id,
            chat_id=chat_id,
            was_helpful=was_helpful,
            alternative_solution=alternative_solution
        )
        session.add(review)
        session.commit()
        return review.id

def get_analysis_reviews(analysis_id):
    with Session(engine) as session:
        reviews = session.query(AnalysisReview).filter(
            AnalysisReview.analysis_id == analysis_id
        ).all()
        return reviews