from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from enums.building_type import BuildingType
from enums.selected_service import SelectedService
from database.connector import get_session
from models.booking import Booking


class BookingService:

    def create_booking(
        self,
        first_name: str,
        last_name: str,
        phone_number: str,
        email: str,
        street: str,
        start_datetime: datetime,
        finish_datetime: datetime,
        selected_service: SelectedService,
        clean_oven: bool,
        clean_windows: bool,
        clean_basement: bool,
        move_in_cleaning: bool,
        move_out_cleaning: bool,
        clean_fridge: bool,
        building: BuildingType,
        rooms_number: int,
        square_feet: int,
        use_equipment: bool,
        session: Session = get_session(),
    ) -> None:
        booking = Booking(
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            email=email,
            street=street,
            start_datetime=start_datetime,
            finish_datetime=finish_datetime,
            selected_service=selected_service,
            clean_oven=clean_oven,
            clean_windows=clean_windows,
            clean_basement=clean_basement,
            move_in_cleaning=move_in_cleaning,
            move_out_cleaning=move_out_cleaning,
            clean_fridge=clean_fridge,
            building=building,
            rooms_number=rooms_number,
            square_feet=square_feet,
            use_equipment=use_equipment,
        )
        session.add(booking)
        session.commit()
        session.close()
