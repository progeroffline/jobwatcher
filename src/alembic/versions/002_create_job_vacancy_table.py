"""Create job vacancy table

Revision ID: 002
Revises: 001
Create Date: 2024-11-10 06:08:39.154429

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '002'
down_revision: Union[str, None] = '001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('job_vacancies',
    sa.Column('id', sa.BigInteger(), autoincrement=False, nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('company', sa.String(), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('url', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.alter_column('users', 'name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('users', 'username',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('users', 'is_admin',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    op.create_unique_constraint(None, 'users', ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.alter_column('users', 'is_admin',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    op.alter_column('users', 'username',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('users', 'name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.drop_table('job_vacancies')
    # ### end Alembic commands ###