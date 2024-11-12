from sqlalchemy import BigInteger, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from bot.database.abstracts import ModelPrettyPrint


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
