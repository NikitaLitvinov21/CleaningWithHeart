from datetime import datetime
from typing import Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from models.base import Base


class Booking(Base):

    __tablename__ = "bookings"

    first_name: Mapped[str] = mapped_column(String(length=30), nullable=False)
    last_name: Mapped[Optional[str]] = mapped_column(String(length=30), nullable=False)
    phone_number: Mapped[str] = mapped_column(String(length=11), nullable=False)
    street: Mapped[str]
    datetime_local: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )
