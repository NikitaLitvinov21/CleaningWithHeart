from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base


class MessageLog(Base):
    __tablename__ = "message_logs"

    target_customer_name: Mapped[str]
    target_phone_number: Mapped[str]
    message: Mapped[str]
    notify_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    sent_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
