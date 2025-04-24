from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column

from common.utils.datetime_util import datetime_to_str
from models.base import Base


class UnavailableDate(Base):
    __tablename__ = "unavailable_dates"

    start_datetime: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    finish_datetime: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )

    def to_dict(self):
        return {
            "id": self.id,
            "startDatetime": datetime_to_str(self.start_datetime),
            "finishDatetime": datetime_to_str(self.finish_datetime),
        }
