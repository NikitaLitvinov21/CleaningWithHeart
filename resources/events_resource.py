from typing import List

from flask import Response, json, request
from flask_login import login_required
from flask_restful import Resource

from models.booking import Booking
from services.booking_service import BookingService


class EventsResource(Resource):

    def __init__(self):
        self.booking_service = BookingService()

    @login_required
    def get(self) -> Response:
        try:
            bookings: List[Booking] = self.booking_service.retrieve_bookings(
                limit=int(request.args.get("limit", 20)),
                page=int(request.args.get("page", 1)),
            )
            booking_count: int = self.booking_service.retrieve_booking_count()
            return Response(
                status=200,
                content_type="application/json",
                response=json.dumps(
                    {
                        "events": [booking.as_event() for booking in bookings],
                        "count": booking_count,
                    }
                ),
            )
        except (ValueError, TypeError) as e:
            return Response(
                status=400,
                content_type="application/json",
                response=json.dumps({"message": str(e)}),
            )
