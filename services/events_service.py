from datetime import datetime
from typing import List

from sqlalchemy.orm import Session

from common.utils.transaction import transaction
from database.connector import get_session
from models.booking import Booking
from schemes.event_scheme import EventScheme


class EventsService:

    @transaction
    def retrieve_events(
        self,
        start_datetime: datetime,
        finish_datetime: datetime,
        session: Session = get_session(),
    ) -> List[EventScheme]:

        bookings: List[Booking] = (
            session.query(Booking)
            .with_entities(
                Booking.id,
                Booking.first_name,
                Booking.last_name,
                Booking.start_datetime,
                Booking.finish_datetime,
            )
            .filter(
                Booking.start_datetime < finish_datetime,
                Booking.finish_datetime > start_datetime,
            )
            .all()
        )

        events = []

        for booking in bookings:

            title = booking.first_name + " " + booking.last_name

            events.append(
                EventScheme(
                    id=booking.id,
                    title=title,
                    start_datetime=booking.start_datetime,
                    finish_datetime=booking.finish_datetime,
                )
            )

        return events
