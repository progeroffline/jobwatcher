from sqlalchemy import Boolean, BigInteger, ForeignKey, Integer, String, Text, inspect
from sqlalchemy.orm import Mapped, mapped_column, relationship
from bot.database.abstracts import ModelPrettyPrint


class User(ModelPrettyPrint):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        unique=True,
        autoincrement=False,
    )
    name: Mapped[str] = mapped_column(String, default="")
    username: Mapped[str] = mapped_column(String, default="")
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)


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

    location_id: Mapped[int] = mapped_column(ForeignKey("job_vacancies_locations.id"))
    location: Mapped["JobVacancyLocation"] = relationship(
        "JobVacancyLocation", back_populates="vacancies"
    )

    def to_dict(self):
        data = {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
        if self.location:
            data["location"] = self.location.to_dict()
        return data


class JobVacancyLocation(ModelPrettyPrint):
    __tablename__ = "job_vacancies_locations"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        unique=True,
        autoincrement=True,
    )
    continent: Mapped[str] = mapped_column(String, default="")
    country: Mapped[str] = mapped_column(String, default="")
    city: Mapped[str] = mapped_column(String, default="")

    vacancies: Mapped[list[JobVacancy]] = relationship(
        "JobVacancy",
        back_populates="location",
    )

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}


class Channel(ModelPrettyPrint):
    __tablename__ = "channels"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        unique=True,
        autoincrement=False,
    )
    title: Mapped[str] = mapped_column(String, default="")
    post_interval: Mapped[int] = mapped_column(Integer, default=1)
