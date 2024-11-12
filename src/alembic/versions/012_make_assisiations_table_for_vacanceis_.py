"""Make assisiations table for vacanceis and locations

Revision ID: 012
Revises: 011
Create Date: 2024-11-12 16:57:33.046044

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '012'
down_revision: Union[str, None] = '011'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('job_vacancy_location_association',
    sa.Column('job_vacancy_id', sa.String(), nullable=False),
    sa.Column('location_id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['job_vacancy_id'], ['job_vacancies.id'], ),
    sa.ForeignKeyConstraint(['location_id'], ['job_vacancies_locations.id'], ),
    sa.PrimaryKeyConstraint('job_vacancy_id', 'location_id')
    )
    op.drop_constraint('job_vacancies_location_id_fkey', 'job_vacancies', type_='foreignkey')
    op.drop_column('job_vacancies', 'location_id')
    op.alter_column('job_vacancies_locations', 'id',
               existing_type=sa.INTEGER(),
               type_=sa.BigInteger(),
               existing_nullable=False,
               autoincrement=True,
               existing_server_default=sa.text("nextval('job_vacancies_locations_id_seq'::regclass)"))
    op.create_unique_constraint(None, 'job_vacancies_locations', ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'job_vacancies_locations', type_='unique')
    op.alter_column('job_vacancies_locations', 'id',
               existing_type=sa.BigInteger(),
               type_=sa.INTEGER(),
               existing_nullable=False,
               autoincrement=True,
               existing_server_default=sa.text("nextval('job_vacancies_locations_id_seq'::regclass)"))
    op.add_column('job_vacancies', sa.Column('location_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.create_foreign_key('job_vacancies_location_id_fkey', 'job_vacancies', 'job_vacancies_locations', ['location_id'], ['id'])
    op.drop_table('job_vacancy_location_association')
    # ### end Alembic commands ###