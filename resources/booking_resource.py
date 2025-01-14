from typing import Optional

from flask import Response, json
from flask_restful import Resource

from models.booking import Booking
from services.booking_service import BookingService


class BookingResource(Resource):

    def __init__(self):
        self.booking_service = BookingService()

    def get(self, booking_id: int):

        booking: Optional[Booking] = self.booking_service.retrieve_booking_by_id(
            booking_id=booking_id
        )
        if booking:
            return Response(
                status=200,
                content_type="application/json",
                response=json.dumps(booking.to_dict()),
            )
        else:
            return Response(
                status=404,
                content_type="application/json",
                response=json.dumps({"message": "Booking not found!"}),
            )
