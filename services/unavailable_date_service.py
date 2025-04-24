from sqlalchemy.orm import Session
from datetime import datetime
from common.utils.transaction import transaction
from database.connector import get_session
from models.unavailable_date import UnavailableDate
from common.exceptions.entity_not_found_exception import EntityNotFoundError
from typing import Optional, List


class UnavailableDateService:

    @transaction
    def create_unavailable_date(
        self,
        start_datetime: datetime,
        finish_datetime: datetime,
        session: Session,
    ) -> UnavailableDate:
        entry = UnavailableDate(
            start_datetime=start_datetime,
            finish_datetime=finish_datetime,
        )
        session.add(entry)
        return entry

    @transaction
    def delete_unavailable_date(self, id_: int, session: Session) -> None:
        entry: UnavailableDate = self.retrieve_by_id(id_, session)
        session.delete(entry)

    def retrieve_by_id(
        self, id_: int, session: Optional[Session] = None
    ) -> UnavailableDate:
        created_here = False
        if session is None:
            session = get_session()
            created_here = True

        try:
            entry = (
                session.query(UnavailableDate).filter(UnavailableDate.id == id_).first()
            )
            if not entry:
                raise EntityNotFoundError("Unavailable date not found")
            return entry
        finally:
            if created_here:
                session.close()

    @transaction
    def retrieve_all(self, session: Session) -> List[UnavailableDate]:
        return session.query(UnavailableDate).all()
