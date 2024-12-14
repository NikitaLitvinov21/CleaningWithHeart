from flask import Response
from flask_restful import Resource

from schemes.booking_scheme import BookingScheme
from utils.validate_by_scheme import validate_by_scheme


class BookingResource(Resource):

    @validate_by_scheme(BookingScheme)
    def post(self, booking: BookingScheme) -> Response:
        print(booking)
        return Response(
            status=201,
            content_type="application/json",
            response='{"message": "Your booking has been accepted!"}',
        )
