from typing import TYPE_CHECKING
from sqlalchemy import Boolean, BigInteger, Column, ForeignKey, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship
from bot.database.abstracts import ModelPrettyPrint
from bot.database.base import Base

if TYPE_CHECKING:
    from .job_vacancy_categories import JobVacancyCategory

user_subscription_association = Table(
    "user_subscriptions",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("category_id", ForeignKey("job_vacancy_categories.id"), primary_key=True),
)


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
    subscribed_categories: Mapped[list["JobVacancyCategory"]] = relationship(
        "JobVacancyCategory",
        secondary=user_subscription_association,
        back_populates="subscribed_users",
    )
