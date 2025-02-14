from datetime import datetime, timedelta
from typing import List, Optional, Union

from flask import Response, json, request
from flask_login import login_required
from flask_restful import Resource
from pydantic import EmailStr, ValidationError

from enums.building_type import BuildingType
from enums.selected_service import SelectedService
from models.booking import Booking
from models.customer import Customer
from schemes.booking_scheme import BookingScheme
from schemes.customer_scheme import CustomerScheme
from services.booking_service import BookingService
from services.customer_service import CustomerService


class BookingsResource(Resource):

    def __init__(self):
        self.booking_service = BookingService()
        self.customer_service = CustomerService()

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

    # login not required here!
    def post(self) -> Response:

        try:
            data: dict = request.json
            customer_id = (
                int(
                    data["customerId"],
                )
                if data["customerId"]
                else None
            )
            first_name: str = data.get("firstName")
            last_name: str = data.get("lastName", "")
            phone_number: str = data.get("phoneNumber")
            email: Union[EmailStr, str] = data.get("email")
            street: str = data.get("street")
            start_datetime = datetime.fromisoformat(
                data.get("startDatetime"),
            )
            cleaning_master_name: str = data.get("cleaningMasterName") or None
            default_cleaning_duration = timedelta(hours=2)
            finish_datetime: datetime = (
                datetime.fromisoformat(data.get("finishDatetime"))
                if data.get("finishDatetime")
                else start_datetime + default_cleaning_duration
            )
            selected_service: Union[SelectedService, str] = data.get(
                "selectedService",
            )

            # Checkboxes
            has_clean_oven = bool(data.get("hasCleanOven"))
            has_clean_windows = bool(data.get("hasCleanWindows"))
            has_clean_basement = bool(data.get("hasCleanBasement"))
            has_move_in_cleaning = bool(data.get("hasMoveInCleaning"))
            has_move_out_cleaning = bool(data.get("hasMoveOutCleaning"))
            has_clean_fridge = bool(data.get("hasCleanFridge"))
            building: Union[BuildingType, str] = data.get("building")
            rooms_number = abs(int(data.get("roomsNumber")))
            square_feet = abs(int(data.get("squareFeet")))
            has_own_equipment = bool(data.get("hasOwnEquipment"))

            customer_scheme: Optional[CustomerScheme] = None

            if not customer_id:
                customer_scheme = CustomerScheme(
                    first_name=first_name,
                    last_name=last_name,
                    phone_number=phone_number,
                    email=email,
                    street=street,
                )

            booking_scheme = BookingScheme(
                start_datetime=start_datetime,
                finish_datetime=finish_datetime,
                selected_service=selected_service,
                has_clean_oven=has_clean_oven,
                has_clean_windows=has_clean_windows,
                has_clean_basement=has_clean_basement,
                has_move_in_cleaning=has_move_in_cleaning,
                has_move_out_cleaning=has_move_out_cleaning,
                has_clean_fridge=has_clean_fridge,
                cleaning_master_name=cleaning_master_name,
                building=building,
                rooms_number=rooms_number,
                square_feet=square_feet,
                has_own_equipment=has_own_equipment,
            )
            if customer_scheme:
                print(customer_scheme)
            print(booking_scheme)

        except ValidationError as error:
            return Response(
                status=422,
                content_type="application/json",
                response=error.json(),
            )
        except KeyError as error:
            return Response(
                status=400,
                content_type="application/json",
                response=json.dumps({"message": "Invalid key: " + str(error)}),
            )
        except (ValueError, TypeError) as error:
            return Response(
                status=400,
                content_type="application/json",
                response=json.dumps({"message": str(error)}),
            )

        if not customer_id:
            customer_id: Optional[int] = (
                self.customer_service.retrieve_customer_id_by_phone_number(
                    phone_number=customer_scheme.phone_number
                )
            )

        if not customer_id:
            customer: Customer = self.customer_service.create_customer(
                first_name=customer_scheme.first_name,
                last_name=customer_scheme.last_name,
                phone_number=customer_scheme.phone_number,
                email=customer_scheme.email,
                street=customer_scheme.street,
            )
            customer_id = customer.id

        self.booking_service.create_booking(
            customer_id=customer_id,
            start_datetime=booking_scheme.start_datetime,
            finish_datetime=booking_scheme.finish_datetime,
            selected_service=booking_scheme.selected_service,
            has_clean_oven=booking_scheme.has_clean_oven,
            has_clean_windows=booking_scheme.has_clean_windows,
            has_clean_basement=booking_scheme.has_clean_basement,
            has_move_in_cleaning=booking_scheme.has_move_in_cleaning,
            has_move_out_cleaning=booking_scheme.has_move_out_cleaning,
            has_clean_fridge=booking_scheme.has_clean_fridge,
            building=booking_scheme.building,
            rooms_number=booking_scheme.rooms_number,
            square_feet=booking_scheme.square_feet,
            has_own_equipment=booking_scheme.has_own_equipment,
            cleaning_master_name=booking_scheme.cleaning_master_name,
        )

        return Response(
            status=201,
            content_type="application/json",
            response=json.dumps({"message": "Your booking has been accepted!"}),
        )
