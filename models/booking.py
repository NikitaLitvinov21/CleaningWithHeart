from datetime import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common.utils.datetime_util import datetime_to_iso8601
from enums.building_type import BuildingType
from enums.selected_service import SelectedService
from models.base import Base


class Booking(Base):
    __tablename__ = "bookings"

    customer_id = mapped_column(BigInteger, ForeignKey("customers.id"))
    has_customer_been_notified: Mapped[bool] = mapped_column(default=False)
    cleaning_master_name: Mapped[str] = mapped_column(
        String(length=64),
        nullable=True,
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

    customer = relationship("Customer", back_populates="bookings")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "cleaningMasterName": self.cleaning_master_name,
            "startDatetime": datetime_to_iso8601(self.start_datetime),
            "finishDatetime": datetime_to_iso8601(self.finish_datetime),
            "selectedService": self.selected_service,
            "hasCleanOven": self.has_clean_oven,
            "hasCleanWindows": self.has_clean_windows,
            "hasCleanBasement": self.has_clean_basement,
            "hasMoveInCleaning": self.has_move_in_cleaning,
            "hasMoveOutCleaning": self.has_move_out_cleaning,
            "hasCleanFridge": self.has_clean_fridge,
            "building": self.building,
            "roomsNumber": self.rooms_number,
            "squareFeet": self.square_feet,
            "hasOwnEquipment": self.has_own_equipment,
            "customer": self.customer.to_dict(),
            # ? Inherit from Base
            "createdAt": datetime_to_iso8601(self.created_at),
            "updatedAt": datetime_to_iso8601(self.updated_at),
        }
