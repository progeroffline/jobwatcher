from typing import TYPE_CHECKING
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from bot.database.abstracts import ModelPrettyPrint
from bot.database.models.user import user_subscription_association

if TYPE_CHECKING:
    from .user import User
    from .job_vacancy import JobVacancy
    from .job_vacancy_service_id import JobVacancyCategoryServiceID


class JobVacancyCategory(ModelPrettyPrint):
    __tablename__ = "job_vacancy_categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    service_ids: Mapped[list["JobVacancyCategoryServiceID"]] = relationship(
        "JobVacancyCategoryServiceID", back_populates="subcategory"
    )

    vacancies: Mapped[list["JobVacancy"]] = relationship(
        "JobVacancy",
        back_populates="category",
    )

    subscribed_users: Mapped[list["User"]] = relationship(
        "User",
        secondary=user_subscription_association,
        back_populates="subscribed_categories",
    )
