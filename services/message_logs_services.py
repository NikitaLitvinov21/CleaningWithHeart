from datetime import datetime

from sqlalchemy.orm import Session

from common.utils.transaction import transaction
from models.message_log import MessageLog


class MessageLogsService:

    @transaction
    def create_message_log(
        self,
        target_customer_name: str,
        target_phone_number: str,
        message: str,
        notify_at: datetime,
        sent_at: datetime,
        session: Session,
    ) -> None:
        message_log = MessageLog(
            target_customer_name=target_customer_name,
            target_phone_number=target_phone_number,
            message=message,
            notify_at=notify_at,
            sent_at=sent_at,
        )
        session.add(message_log)
