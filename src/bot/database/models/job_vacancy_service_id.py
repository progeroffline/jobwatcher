from typing import TYPE_CHECKING
from sqlalchemy import (
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from bot.database.abstracts import ModelPrettyPrint

if TYPE_CHECKING:
    from .job_vacancy_categories import JobVacancyCategory


class JobVacancyCategoryServiceID(ModelPrettyPrint):
    __tablename__ = "job_vacancy_categories_service_ids"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    service_name: Mapped[str] = mapped_column(String, nullable=False)
    service_id: Mapped[str] = mapped_column(String, nullable=False, unique=False)

    category_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("job_vacancy_categories.id"), nullable=False
    )
    subcategory: Mapped["JobVacancyCategory"] = relationship(
        "JobVacancyCategory", back_populates="service_ids"
    )
