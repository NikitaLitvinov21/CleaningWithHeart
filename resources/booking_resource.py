from datetime import timedelta

from flask import Response, json
from flask_restful import Resource

from schemes.booking_scheme import BookingScheme, validate_by_booking_scheme
from services.booking_service import BookingService


class BookingResource(Resource):

    def __init__(self):
        self.booking_service = BookingService()

    @validate_by_booking_scheme()
    def post(self, booking: BookingScheme) -> Response:

        default_cleaning_duration = timedelta(hours=2)

        self.booking_service.create_booking(
            first_name=booking.first_name,
            last_name=booking.last_name,
            phone_number=booking.phone_number,
            email=booking.email,
            street=booking.street,
            start_datetime=booking.start_datetime,
            finish_datetime=booking.start_datetime + default_cleaning_duration,
            selected_service=booking.selected_service,
            clean_oven=booking.clean_oven,
            clean_windows=booking.clean_windows,
            clean_basement=booking.clean_basement,
            move_in_cleaning=booking.move_in_cleaning,
            move_out_cleaning=booking.move_out_cleaning,
            clean_fridge=booking.clean_fridge,
            building=booking.building,
            rooms_number=booking.rooms_number,
            square_feet=booking.square_feet,
            use_equipment=booking.use_equipment,
        )

        return Response(
            status=201,
            content_type="application/json",
            response=json.dumps('{"message": "Your booking has been accepted!"}'),
        )
