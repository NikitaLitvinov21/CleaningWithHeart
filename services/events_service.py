from datetime import datetime
from typing import List

from sqlalchemy.orm import Session

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
            .with_entities(
                Booking.id,
                Booking.first_name,
                Booking.last_name,
                Booking.start_datetime,
                Booking.finish_datetime,
                Booking.selected_service,
            )
            .filter(
                Booking.start_datetime < finish_datetime,
                Booking.finish_datetime > start_datetime,
            )
            .all()
        )

        events = []

        for booking in bookings:

            customer_fullname = booking.first_name + " " + booking.last_name

            title = (
                customer_fullname + " / " + booking.selected_service.replace("_", " ")
            )

            events.append(
                EventScheme(
                    id=booking.id,
                    title=title,
                    start_datetime=booking.start_datetime,
                    finish_datetime=booking.finish_datetime,
                )
            )

        return events
