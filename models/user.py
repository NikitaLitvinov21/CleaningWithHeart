from datetime import date
from typing import Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column  # , relationship

from models.base import Base


class User(Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    first_name: Mapped[Optional[str]]
    last_name: Mapped[Optional[str]]
    phone_number: Mapped[Optional[str]] = mapped_column(String(12))
    email_address: Mapped[Optional[str]]
    birth_date: Mapped[Optional[date]]

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def to_dict(self):
        return {
            "id": str(self.id),
            "username": self.username,
            "phoneNumber": self.phone_number,
            "firstName": self.first_name,
            "lastName": self.last_name,
            "fullName": self.full_name,
            "emailAddress": self.email_address,
            # ? Inherit from Base
            "createdAt": str(self.created_at),
            "updatedAt": str(self.updated_at),
        }
