from dataclasses import dataclass
from sqlalchemy.orm import Mapped, mapped_column
from app.shared.orm import db


@dataclass
class User(db.Model):

    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column()
    permission: Mapped[str] = mapped_column(default="read-only")
    role: Mapped[str] = mapped_column(default="user")
    is_online: Mapped[bool] = mapped_column(default=False)
    token: Mapped[str] = mapped_column(nullable=True)
