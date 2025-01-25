from datetime import timedelta
from typing import List, Optional

from flask import Response, json
from flask_restful import Resource

from models.booking import Booking
from schemes.booking_scheme import BookingScheme, validate_by_booking_scheme
from services.booking_service import BookingService


class BookingsResource(Resource):

    def __init__(self):
        self.booking_service = BookingService()

    def get(self):

        bookings: Optional[List[Booking]] = self.booking_service.retrieve_bookings()

        return Response(
            status=200,
            content_type="application/json",
            response=json.dumps([booking.to_dict() for booking in bookings]),
        )

    @validate_by_booking_scheme()
    def post(self, booking: BookingScheme) -> Response:

        self.booking_service.create_booking(
            first_name=booking.first_name,
            last_name=booking.last_name,
            phone_number=booking.phone_number,
            email=booking.email,
            street=booking.street,
            start_datetime=booking.start_datetime,
            finish_datetime=booking.finish_datetime,
            selected_service=booking.selected_service,
            has_clean_oven=booking.has_clean_oven,
            has_clean_windows=booking.has_clean_windows,
            has_clean_basement=booking.has_clean_basement,
            has_move_in_cleaning=booking.has_move_in_cleaning,
            has_move_out_cleaning=booking.has_move_out_cleaning,
            has_clean_fridge=booking.has_clean_fridge,
            building=booking.building,
            rooms_number=booking.rooms_number,
            square_feet=booking.square_feet,
            has_own_equipment=booking.has_own_equipment,
        )

        return Response(
            status=201,
            content_type="application/json",
            response=json.dumps({"message": "Your booking has been accepted!"}),
        )
