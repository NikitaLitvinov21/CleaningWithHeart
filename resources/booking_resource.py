from flask import Response
from flask_restful import Resource

from schemes.booking_scheme import BookingScheme
from services.booking_service import BookingService
from utils.validate_by_scheme import validate_by_scheme


class BookingResource(Resource):

    def __init__(self):
        self.booking_service = BookingService()

    @validate_by_scheme(BookingScheme)
    def post(self, booking: BookingScheme) -> Response:

        self.booking_service.create_booking(
            first_name=booking.first_name,
            last_name=booking.last_name,
            phone_number=booking.phone_number,
            street=booking.street,
            datetime_local=booking.datetime_local,
        )

        return Response(
            status=201,
            content_type="application/json",
            response='{"message": "Your booking has been accepted!"}',
        )
