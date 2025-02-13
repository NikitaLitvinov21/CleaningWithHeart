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
    last_name: Mapped[Optional[str]] = mapped_column(
        String(length=32),
        nullable=False,
    )
    phone_number: Mapped[str] = mapped_column(
        String(length=11), nullable=False,
    )
    email: Mapped[str] = mapped_column(String(length=319), nullable=False)
    street: Mapped[str] = mapped_column(String(255))
    cleaning_master_name: Mapped[str] = mapped_column(
        String(length=64), nullable=True,
    )
    start_datetime: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    finish_datetime: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    selected_service: Mapped[SelectedService]
    has_clean_oven: Mapped[bool]
    has_clean_windows: Mapped[bool]
    has_clean_basement: Mapped[bool]
    has_move_in_cleaning: Mapped[bool]
    has_move_out_cleaning: Mapped[bool]
    has_clean_fridge: Mapped[bool]
    building: Mapped[BuildingType]
    rooms_number: Mapped[int]
    square_feet: Mapped[int]
    has_own_equipment: Mapped[bool]

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "firstName": self.first_name,
            "lastName": self.last_name,
            "phoneNumber": self.phone_number,
            "email": self.email,
            "cleaningMasterName": self.cleaning_master_name,
            "street": self.street,
            "startDatetime": datetime_to_iso8601(self.start_datetime),
            "finishDatetime": datetime_to_iso8601(self.finish_datetime),
            "selectedService": self.selected_service,
            "hasCleanOven": self.has_clean_oven,
            "hasCleanWindows": self.has_clean_windows,
            "hasCleanBasement": self.has_clean_basement,
            "hasMoveInCleaning": self.has_move_in_cleaning,
            "hasCleanFridge": self.has_clean_fridge,
            "building": self.building,
            "roomsNumber": self.rooms_number,
            "squareFeet": self.square_feet,
            "hasOwnEquipment": self.has_own_equipment,
            # ? Inherit from Base
            "createdAt": datetime_to_iso8601(self.created_at),
            "updatedAt": datetime_to_iso8601(self.updated_at),
        }
