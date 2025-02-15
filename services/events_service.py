from datetime import datetime
from typing import List

from sqlalchemy.orm import Session, joinedload

from common.utils.transaction import transaction
from models.booking import Booking
from schemes.event_scheme import EventScheme


class EventsService:

    @transaction
    def retrieve_events(
        self,
        start_datetime: datetime,
        finish_datetime: datetime,
        session: Session,
    ) -> List[EventScheme]:

        bookings: List[Booking] = (
            session.query(Booking)
            .options(joinedload(Booking.customer))
            .filter(
                Booking.start_datetime < finish_datetime,
                Booking.finish_datetime > start_datetime,
            )
            .all()
        )

        events = []

        for booking in bookings:

            customer_fullname = booking.customer.full_name

            selected_service = booking.selected_service.replace("_", " ")

            title = customer_fullname + " / " + selected_service

            events.append(
                EventScheme(
                    id=booking.id,
                    title=title,
                    start_datetime=booking.start_datetime,
                    finish_datetime=booking.finish_datetime,
                )
            )

        return events
