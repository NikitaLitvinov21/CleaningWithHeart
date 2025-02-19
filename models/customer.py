from typing import Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base


class Customer(Base):
    __tablename__ = "customers"

    first_name: Mapped[str] = mapped_column(
        String(length=32),
        nullable=False,
    )
    last_name: Mapped[Optional[str]] = mapped_column(
        String(length=32),
        nullable=True,
    )
    phone_number: Mapped[str] = mapped_column(
        String(12),
        unique=True,
        nullable=False,
    )
    email: Mapped[str] = mapped_column(String(319), nullable=False)
    street: Mapped[str] = mapped_column(String(length=255), nullable=False)
    special_notes: Mapped[Optional[str]] = mapped_column(nullable=True)

    bookings = relationship("Booking", back_populates="customer", cascade="all,delete")

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    @property
    def international_phone_number(self):
        return f"+{self.phone_number}"

    def to_dict(self):
        return {
            "id": self.id,
            "firstName": self.first_name,
            "lastName": self.last_name,
            "fullName": self.full_name,
            "phoneNumber": self.phone_number,
            "email": self.email,
            "street": self.street,
            "specialNotes": self.special_notes,
        }
