from typing import TYPE_CHECKING
from sqlalchemy import (
    Boolean,
    ForeignKey,
    Integer,
    String,
    Text,
    inspect,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from bot.database.abstracts import ModelPrettyPrint
from bot.database.mixins import AuditMixin
from bot.database.models.job_vacancy_location import (
    job_vacancy_location_association,
)

if TYPE_CHECKING:
    from .job_vacancy_location import JobVacancyLocation
    from .job_vacancy_categories import JobVacancyCategory


class JobVacancy(ModelPrettyPrint, AuditMixin):
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

    category_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("job_vacancy_categories.id"),
        nullable=False,
    )

    category: Mapped["JobVacancyCategory"] = relationship(
        "JobVacancyCategory", back_populates="vacancies"
    )

    def to_dict(self):
        data = {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
        data["locations"] = [location.to_dict() for location in self.locations]
        return data
