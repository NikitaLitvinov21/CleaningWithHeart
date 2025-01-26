from typing import List

from flask import Response, json, request
from flask_login import login_required
from flask_restful import Resource

from models.booking import Booking
from schemes.booking_scheme import BookingScheme, validate_by_booking_scheme
from services.booking_service import BookingService


class BookingsResource(Resource):

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
                        "bookings": [booking.to_dict() for booking in bookings],
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

    @login_required
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
