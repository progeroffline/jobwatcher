from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    Table,
    Text,
    inspect,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from bot.database.abstracts import ModelPrettyPrint
from bot.database.base import Base


job_vacancy_location_association = Table(
    "job_vacancy_location_association",
    Base.metadata,
    Column("job_vacancy_id", ForeignKey("job_vacancies.id"), primary_key=True),
    Column("location_id", ForeignKey("job_vacancies_locations.id"), primary_key=True),
)


class JobVacancy(ModelPrettyPrint):
    __tablename__ = "job_vacancies"

    id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
        unique=True,
        autoincrement=False,
    )
    title: Mapped[str] = mapped_column(String, default="")
    company: Mapped[str] = mapped_column(String, default="")
    description: Mapped[str] = mapped_column(Text, default="")
    min_salary: Mapped[int] = mapped_column(Integer, default=0)
    max_salary: Mapped[int] = mapped_column(Integer, default=0)
    salary_currency: Mapped[str] = mapped_column(String, default="")
    salary_period: Mapped[str] = mapped_column(String, default="")
    sent_to_channel: Mapped[bool] = mapped_column(Boolean, default=False)
    url: Mapped[str] = mapped_column(String, default="")

    locations: Mapped[list["JobVacancyLocation"]] = relationship(
        "JobVacancyLocation",
        secondary=job_vacancy_location_association,
        back_populates="vacancies",
    )

    def to_dict(self):
        data = {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
        data["locations"] = [location.to_dict() for location in self.locations]
        return data


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

    vacancies: Mapped[list[JobVacancy]] = relationship(
        "JobVacancy",
        secondary=job_vacancy_location_association,
        back_populates="locations",
    )

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
