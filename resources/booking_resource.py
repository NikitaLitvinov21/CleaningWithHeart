from flask_restful import Resource

from schemes.booking_scheme import BookingScheme
from utils.validate_by_scheme import validate_by_scheme


class BookingResource(Resource):

    @validate_by_scheme(BookingScheme)
    def post(self, booking: BookingScheme) -> dict:
        print(booking)
        return {"message": "Flask comes alive!"}
