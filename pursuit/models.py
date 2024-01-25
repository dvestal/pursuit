# pylint: disable=missing-module-docstring, missing-class-docstring

from flask_login import UserMixin
from sqlalchemy.orm import Mapped, mapped_column
from . import db

class User(UserMixin, db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    online: Mapped[bool] = mapped_column(default=False)
    sid: Mapped[str] = mapped_column(default=None, nullable=True)
    tank: Mapped[str] = mapped_column(default=None, nullable=True)
    bot: Mapped[bool] = mapped_column(default=False, nullable=True)
