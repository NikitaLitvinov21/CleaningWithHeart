from datetime import datetime, timezone
from threading import Thread
from time import sleep
from typing import NoReturn

from common.messages.twilio_client import TwilioClient
from services.booking_service import BookingService
from services.message_logs_services import MessageLogsService


class TwilioWorker:

    def __init__(self, config: dict, interval_seconds: int = 60):
        self.job = None
        self.interval_seconds = interval_seconds
        self.twilio_client = TwilioClient(config)
        self.booking_service = BookingService()
        self.message_logs_services = MessageLogsService()
        self.message = config["message"]

    def run(self) -> bool:
        if not self.job:
            self.job = Thread(target=self.sending_message)
            self.job.start()
        return self.job.is_alive()

    def sending_message(self) -> NoReturn:
        while True:
            try:
                datetime_now = datetime.now(tz=timezone.utc)
                bookings: list = self.booking_service.retrieve_all_bookings(
                    current_time=datetime_now, only_not_notified=True
                )
                for booking in bookings:
                    print(f"TwilioWorker catch {booking.to_dict()}")
                    customer = booking.customer
                    if customer and customer.phone_number:
                        self.booking_service.set_as_notified(
                            booking_id=booking.id,
                        )
                        self.twilio_client.send_sms(
                            message_body=self.message,
                            receiver=customer.international_phone_number,
                        )
                        self.message_logs_services.create_message_log(
                            target_customer_name=customer.full_name,
                            target_phone_number=customer.phone_number,
                            message=self.message,
                            notify_at=booking.notify_at,
                            sent_at=datetime_now,
                        )
            except Exception as exceptions:
                print(f"TwilioWorker: {exceptions.__class__}, {exceptions}")

            sleep(self.interval_seconds)
