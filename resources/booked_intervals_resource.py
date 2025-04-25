from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from flask import Response, json
from flask_restful import Resource
from services.booking_service import BookingService


class BookedIntervalsResource(Resource):
    def __init__(self):
        self.booking_service = BookingService()

    def get(self) -> Response:
        try:
            utc = ZoneInfo("UTC")
            toronto = ZoneInfo("America/Toronto")

            now_utc = datetime.now(utc) - timedelta(days=1)
            max_utc = now_utc + timedelta(days=60)
            bookings = self.booking_service.retrieve_bookings_in_range(now_utc, max_utc)

            intervals = [
                {
                    "from": b.start_datetime.astimezone(toronto).isoformat(),
                    "to": b.finish_datetime.astimezone(toronto).isoformat(),
                }
                for b in bookings
                if b.start_datetime and b.finish_datetime
            ]

            return Response(
                status=200,
                content_type="application/json",
                response=json.dumps({"intervals": intervals}),
            )
        except Exception as e:
            return Response(
                status=500,
                content_type="application/json",
                response=json.dumps({"message": str(e)}),
            )
