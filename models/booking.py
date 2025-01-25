from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from common.utils.datetime_util import datetime_to_iso8601
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

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "firstName": self.first_name,
            "lastName": self.last_name,
            "phoneNumber": self.phone_number,
            "email": self.email,
            "street": self.street,
            "startDatetime": datetime_to_iso8601(self.start_datetime),
            "finishDatetime": datetime_to_iso8601(self.finish_datetime),
            "selectedService": self.selected_service,
            "cleanOven": self.clean_oven,
            "cleanWindows": self.clean_windows,
            "cleanBasement": self.clean_basement,
            "moveInCleaning": self.move_in_cleaning,
            "cleanFridge": self.clean_fridge,
            "building": self.building,
            "roomsNumber": self.rooms_number,
            "squareFeet": self.square_feet,
            "useEquipment": self.use_equipment,
            # ? Inherit from Base
            "createdAt": datetime_to_iso8601(self.created_at),
            "updatedAt": datetime_to_iso8601(self.updated_at),
        }

    def as_event(self) -> dict:
        return {
            "id": self.id,
            "title": self.first_name + " " + self.last_name,
            "start": self.start_datetime,
            "end": self.finish_datetime,
        }
