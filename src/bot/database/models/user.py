from typing import TYPE_CHECKING
from sqlalchemy import Boolean, BigInteger, Column, ForeignKey, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship
from bot.database.abstracts import ModelPrettyPrint
from bot.database.base import Base
from bot.database.mixins import AuditMixin

if TYPE_CHECKING:
    from .job_vacancy_categories import JobVacancyCategory

user_category_subscription_association = Table(
    "user_category_subscriptions",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("category_id", ForeignKey("job_vacancy_categories.id"), primary_key=True),
)


class User(ModelPrettyPrint, AuditMixin):
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
    keyword: Mapped[str] = mapped_column(String, default="", nullable=True)
    subscribed_categories: Mapped[list["JobVacancyCategory"]] = relationship(
        "JobVacancyCategory",
        secondary=user_category_subscription_association,
        back_populates="subscribed_users",
    )
    subscribed_regions: Mapped[list["UserRegionSubscription"]] = relationship(
        "UserRegionSubscription",
        lazy="selectin",
        back_populates="user",
    )


class UserRegionSubscription(ModelPrettyPrint):
    __tablename__ = "user_region_subscription"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"))
    region: Mapped[str] = mapped_column(String)
    user: Mapped["User"] = relationship("User", back_populates="subscribed_regions")
