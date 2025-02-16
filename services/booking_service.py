from datetime import datetime, timedelta
from typing import List, Optional

from sqlalchemy.orm import Session, joinedload

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
            .options(joinedload(Booking.customer))
            .limit(
                limit=limit,
            )
            .offset(offset_value)
            .all()
        )
        return bookings

    @transaction
    def retrieve_all_bookings(
        self,
        session: Session,
        older_then: Optional[datetime] = None,
        only_not_notified: Optional[datetime] = False,
    ) -> List[Booking]:
        query = session.query(Booking).options(joinedload(Booking.customer))

        if older_then:
            query = query.filter(
                Booking.start_datetime - timedelta(hours=1) < older_then,
            )

        if only_not_notified:
            query = query.filter(
                Booking.has_customer_been_notified == False,  # noqa
            )

        return query.all()

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
                .options(joinedload(Booking.customer))
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
        customer_id: int,
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
        cleaning_master_name: Optional[str],
        session: Session,
    ) -> None:
        booking = Booking(
            customer_id=customer_id,
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
            cleaning_master_name=cleaning_master_name,
        )
        session.add(booking)

    @transaction
    def update_booking(
        self,
        booking_id: int,
        customer_id: int,
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
        cleaning_master_name: Optional[str],
        session: Session,
    ) -> None:
        booking: Booking = self.retrieve_booking_by_id(
            booking_id=booking_id, session=session
        )
        booking.customer_id = customer_id
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
        booking.cleaning_master_name = cleaning_master_name

    @transaction
    def update_booking_range(
        self,
        booking_id: int,
        start_datetime: datetime,
        finish_datetime: datetime,
        session: Session,
    ) -> None:
        booking: Booking = self.retrieve_booking_by_id(
            booking_id=booking_id, session=session
        )
        booking.start_datetime = start_datetime
        booking.finish_datetime = finish_datetime

    @transaction
    def set_as_notified(
        self,
        booking_id: int,
        has_customer_been_notified: bool,
        session: Session,
    ) -> None:
        booking: Booking = self.retrieve_booking_by_id(
            booking_id=booking_id, session=session
        )
        booking.has_customer_been_notified = has_customer_been_notified

    @transaction
    def delete_booking(
        self,
        booking_id: int,
        session: Session,
    ) -> None:
        booking: Optional[Booking] = self.retrieve_booking_by_id(
            booking_id=booking_id, session=session
        )
        session.delete(booking)
