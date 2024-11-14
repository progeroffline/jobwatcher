from typing import TYPE_CHECKING
from sqlalchemy import BigInteger, Column, ForeignKey, String, Table, inspect
from sqlalchemy.orm import Mapped, mapped_column, relationship
from bot.database.abstracts import ModelPrettyPrint
from bot.database.base import Base


if TYPE_CHECKING:
    from .job_vacancy import JobVacancy


job_vacancy_location_association = Table(
    "job_vacancy_location_association",
    Base.metadata,
    Column("job_vacancy_id", ForeignKey("job_vacancies.id"), primary_key=True),
    Column("location_id", ForeignKey("job_vacancies_locations.id"), primary_key=True),
)


class JobVacancyLocation(ModelPrettyPrint):
    __tablename__ = "job_vacancies_locations"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        unique=True,
    )
    continent: Mapped[str] = mapped_column(String, default="")
    country: Mapped[str] = mapped_column(String, default="")
    city: Mapped[str] = mapped_column(String, default="")

    vacancies: Mapped[list["JobVacancy"]] = relationship(
        "JobVacancy",
        secondary=job_vacancy_location_association,
        back_populates="locations",
    )

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
