from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from enums.building_type import BuildingType
from enums.selected_service import SelectedService
from models.base import Base


class Booking(Base):

    __tablename__ = "bookings"

    first_name: Mapped[str] = mapped_column(String(length=32), nullable=False)
    last_name: Mapped[Optional[str]] = mapped_column(String(length=32), nullable=False)
    phone_number: Mapped[str] = mapped_column(String(length=11), nullable=False)
    email: Mapped[str] = mapped_column(String(length=319), nullable=False)
    street: Mapped[str]
    start_datetime: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    finish_datetime: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    selected_service: Mapped[SelectedService]
    clean_oven: Mapped[bool]
    clean_windows: Mapped[bool]
    clean_basement: Mapped[bool]
    move_in_cleaning: Mapped[bool]
    move_out_cleaning: Mapped[bool]
    clean_fridge: Mapped[bool]
    building: Mapped[BuildingType]
    rooms_number: Mapped[int]
    square_feet: Mapped[int]
    use_equipment: Mapped[bool]
