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
    r_1: Mapped[Optional[date]] = mapped_column(Date)
    r_2: Mapped[Optional[date]] = mapped_column(Date)
    r_3: Mapped[Optional[date]] = mapped_column(Date)
    r_4: Mapped[Optional[date]] = mapped_column(Date)
    r_5: Mapped[Optional[date]] = mapped_column(Date)
    sentances: Mapped[list['Sentances']] = relationship(back_populates='word')


class Sentances(Base):
    __tablename__ = 'english_sentances'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    chat_id: Mapped[int] = mapped_column(ForeignKey('user_words.user_id'))
    sentance: Mapped[str] = mapped_column(nullable=False, default='Sentance wasnt saved')

    word : Mapped['Word'] = relationship(back_populates='sentances')

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
