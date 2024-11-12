"""Add locations table and connect it to job vacancies by id

Revision ID: 011
Revises: 010
Create Date: 2024-11-12 16:41:20.833068

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '011'
down_revision: Union[str, None] = '010'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('job_vacancies_locations',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('continent', sa.String(), nullable=False),
    sa.Column('country', sa.String(), nullable=False),
    sa.Column('city', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.add_column('job_vacancies', sa.Column('location_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'job_vacancies', 'job_vacancies_locations', ['location_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'job_vacancies', type_='foreignkey')
    op.drop_column('job_vacancies', 'location_id')
    op.drop_table('job_vacancies_locations')
    # ### end Alembic commands ###
