from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session

from common.exceptions.entity_not_found_exception import EntityNotFoundException
from database.connector import get_session
from enums.building_type import BuildingType
from enums.selected_service import SelectedService
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
        has_clean_oven: bool,
        has_clean_windows: bool,
        has_clean_basement: bool,
        has_move_in_cleaning: bool,
        has_move_out_cleaning: bool,
        has_clean_fridge: bool,
        building: BuildingType,
        rooms_number: int,
        square_feet: int,
        has_own_equipment: bool,
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
            has_clean_oven=has_clean_oven,
            has_clean_windows=has_clean_windows,
            has_clean_basement=has_clean_basement,
            has_move_in_cleaning=has_move_in_cleaning,
            has_move_out_cleaning=has_move_out_cleaning,
            has_clean_fridge=has_clean_fridge,
            building=building,
            rooms_number=rooms_number,
            square_feet=square_feet,
            has_own_equipment=has_own_equipment,
        )
        session.add(booking)
        session.commit()
        session.close()

    def retrieve_bookings(
        self,
        session: Session = get_session(),
    ) -> Optional[List[Booking]]:
        return session.query(Booking).all()

    def retrieve_booking_by_id(
        self,
        booking_id: int,
        session: Session = get_session(),
    ) -> Optional[Booking]:
        return session.query(Booking).filter(Booking.id == booking_id).first()

    def update_booking(
        self,
        booking_id: int,
        first_name: str,
        last_name: str,
        phone_number: str,
        email: str,
        street: str,
        start_datetime: datetime,
        finish_datetime: datetime,
        selected_service: SelectedService,
        has_clean_oven: bool,
        has_clean_windows: bool,
        has_clean_basement: bool,
        has_move_in_cleaning: bool,
        has_move_out_cleaning: bool,
        has_clean_fridge: bool,
        building: BuildingType,
        rooms_number: int,
        square_feet: int,
        has_own_equipment: bool,
        session: Session = get_session(),
    ) -> None:
        booking: Optional[Booking] = self.retrieve_booking_by_id(
            booking_id=booking_id, session=session
        )
        if booking:
            booking.first_name = first_name
            booking.last_name = last_name
            booking.phone_number = phone_number
            booking.email = email
            booking.street = street
            booking.start_datetime = start_datetime
            booking.finish_datetime = finish_datetime
            booking.selected_service = selected_service
            booking.has_clean_oven = has_clean_oven
            booking.has_clean_windows = has_clean_windows
            booking.has_clean_basement = has_clean_basement
            booking.has_move_in_cleaning = has_move_in_cleaning
            booking.has_move_out_cleaning = has_move_out_cleaning
            booking.has_clean_fridge = has_clean_fridge
            booking.building = building
            booking.rooms_number = rooms_number
            booking.square_feet = square_feet
            booking.has_own_equipment = has_own_equipment
            session.commit()
            session.close()
        else:
            raise EntityNotFoundException("Booking not found!")

    def delete_booking(
        self,
        booking_id: int,
        session: Session = get_session(),
    ) -> None:
        booking: Optional[Booking] = self.retrieve_booking_by_id(
            booking_id=booking_id, session=session
        )
        if booking:
            session.delete(booking)
            session.commit()
            session.close()
        else:
            raise EntityNotFoundException("Booking not found!")
