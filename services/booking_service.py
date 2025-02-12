from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session

from common.exceptions.entity_not_found_exception import EntityNotFoundException
from common.utils.transaction import transaction
from database.connector import get_session
from enums.building_type import BuildingType
from enums.selected_service import SelectedService
from models.booking import Booking


class BookingService:

    @transaction
    def retrieve_bookings(
        self,
        limit: int,
        page: int,
        session: Session,
    ) -> List[Booking]:
        offset_value = (page - 1) * limit

        bookings: List[Booking] = (
            session.query(Booking)
            .limit(
                limit=limit,
            )
            .offset(offset_value)
            .all()
        )
        return bookings

    def retrieve_booking_by_id(
        self,
        booking_id: int,
        session: Optional[Session] = None,
    ) -> Booking:
        is_session_created_here: bool = False
        if session is None:
            session = get_session()
            is_session_created_here = True

        try:
            booking: Optional[Booking] = (
                session.query(Booking)
                .filter(
                    Booking.id == booking_id,
                )
                .first()
            )
            if booking:
                return booking
            else:
                raise EntityNotFoundException("Booking not found!")
        finally:
            if is_session_created_here:
                session.close()

    @transaction
    def retrieve_booking_count(
        self,
        session: Session,
    ) -> int:
        return session.query(Booking).count()

    @transaction
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

    @transaction
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
        else:
            raise EntityNotFoundException("Booking not found!")

    @transaction
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
        else:
            raise EntityNotFoundException("Booking not found!")
