"""Изменил даты с Даты на стр

Revision ID: 3710f9f9c408
Revises: f56243fb25d0
Create Date: 2025-09-25 12:14:40.495501

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3710f9f9c408'
down_revision: Union[str, Sequence[str], None] = 'f56243fb25d0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # SQLite не поддерживает ALTER COLUMN, поэтому создаем новую таблицу
    # Создаем новую таблицу с правильными типами
    op.create_table('user_words_new',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('en_word', sa.String(), nullable=False),
        sa.Column('p_speech', sa.String(), nullable=False),
        sa.Column('transl', sa.String(), nullable=False),
        sa.Column('date_created', sa.Date(), nullable=True),
        sa.Column('r_1', sa.String(), nullable=False),
        sa.Column('r_2', sa.String(), nullable=False),
        sa.Column('r_3', sa.String(), nullable=False),
        sa.Column('r_4', sa.String(), nullable=False),
        sa.Column('r_5', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Копируем данные из старой таблицы
    op.execute('''
        INSERT INTO user_words_new (id, user_id, en_word, p_speech, transl, date_created, r_1, r_2, r_3, r_4, r_5)
        SELECT id, user_id, en_word, p_speech, transl, date_created, 
               COALESCE(r_1, '2024-01-01'), COALESCE(r_2, '2024-01-01'), 
               COALESCE(r_3, '2024-01-01'), COALESCE(r_4, '2024-01-01'), 
               COALESCE(r_5, '2024-01-01')
        FROM user_words
    ''')
    
    # Удаляем старую таблицу
    op.drop_table('user_words')
    
    # Переименовываем новую таблицу
    op.rename_table('user_words_new', 'user_words')


def downgrade() -> None:
    """Downgrade schema."""
    # Создаем таблицу с исходными типами DATE
    op.create_table('user_words_old',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('en_word', sa.String(), nullable=False),
        sa.Column('p_speech', sa.String(), nullable=False),
        sa.Column('transl', sa.String(), nullable=False),
        sa.Column('date_created', sa.Date(), nullable=True),
        sa.Column('r_1', sa.DATE(), nullable=True),
        sa.Column('r_2', sa.DATE(), nullable=True),
        sa.Column('r_3', sa.DATE(), nullable=True),
        sa.Column('r_4', sa.DATE(), nullable=True),
        sa.Column('r_5', sa.DATE(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Копируем данные обратно
    op.execute('''
        INSERT INTO user_words_old (id, user_id, en_word, p_speech, transl, date_created, r_1, r_2, r_3, r_4, r_5)
        SELECT id, user_id, en_word, p_speech, transl, date_created, 
               CASE WHEN r_1 = '2024-01-01' THEN NULL ELSE r_1 END,
               CASE WHEN r_2 = '2024-01-01' THEN NULL ELSE r_2 END,
               CASE WHEN r_3 = '2024-01-01' THEN NULL ELSE r_3 END,
               CASE WHEN r_4 = '2024-01-01' THEN NULL ELSE r_4 END,
               CASE WHEN r_5 = '2024-01-01' THEN NULL ELSE r_5 END
        FROM user_words
    ''')
    
    # Удаляем новую таблицу
    op.drop_table('user_words')
    
    # Переименовываем старую таблицу
    op.rename_table('user_words_old', 'user_words')
