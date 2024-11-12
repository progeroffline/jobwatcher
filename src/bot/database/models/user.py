from sqlalchemy import Boolean, BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column
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
