from flask import Response, json
from flask_login import login_required
from flask_restful import Resource

from common.exceptions.entity_not_found_exception import EntityNotFoundException
from models.booking import Booking
from schemes.booking_scheme import BookingScheme, validate_by_booking_scheme
from services.booking_service import BookingService


class BookingResource(Resource):

    def __init__(self):
        self.booking_service = BookingService()

    @login_required
    def get(self, booking_id: int):
        try:
            booking: Booking = self.booking_service.retrieve_booking_by_id(
                booking_id=booking_id
            )
            return Response(
                status=200,
                content_type="application/json",
                response=json.dumps(booking.to_dict()),
            )
        except EntityNotFoundException as e:
            return Response(
                status=404,
                content_type="application/json",
                response=json.dumps({"message": str(e)}),
            )

    @login_required
    @validate_by_booking_scheme()
    def put(self, booking_id: int, booking: BookingScheme) -> Response:
        try:
            self.booking_service.update_booking(
                booking_id=booking_id,
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
                status=200,
                content_type="application/json",
                response=json.dumps({"message": "Booking updated successfully!"}),
            )
        except EntityNotFoundException as e:
            return Response(
                status=404,
                content_type="application/json",
                response=json.dumps({"message": str(e)}),
            )

    @login_required
    def delete(self, booking_id: int) -> Response:
        try:
            self.booking_service.delete_booking(booking_id=booking_id)
            return Response(
                status=200,
                content_type="application/json",
                response=json.dumps({"message": "Booking deleted successfully!"}),
            )
        except EntityNotFoundException as e:
            return Response(
                status=404,
                content_type="application/json",
                response=json.dumps({"message": str(e)}),
            )
