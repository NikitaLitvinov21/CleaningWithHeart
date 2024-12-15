from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from database.connector import get_session
from models.booking import Booking


class BookingService:

    def create_booking(
        self,
        first_name: str,
        phone_number: str,
        street: str,
        datetime_local: datetime,
        last_name: Optional[str] = None,
        session: Session = get_session(),
    ):
        booking = Booking(
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            street=street,
            datetime_local=datetime_local,
        )
        session.add(booking)
        session.commit()
        session.close()
