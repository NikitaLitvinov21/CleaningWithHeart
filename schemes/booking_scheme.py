from datetime import datetime
from typing import Annotated, Union

from flask import Response, json, request
from pydantic import EmailStr, Field, StringConstraints, ValidationError

from common.utils.form_request_util import convert_str_to_bool, is_checkbox_on
from enums.building_type import BuildingType
from enums.selected_service import SelectedService
from schemes.scheme import Scheme

str_regexp = r"^[^\d\!\@\#\$\%\^\&\*\=\+\~\/\+\;\:\?\{\}]*$"


class BookingScheme(Scheme):

    first_name: Annotated[
        str,
        StringConstraints(
            min_length=1,
            max_length=30,
            pattern=str_regexp,
            strip_whitespace=True,
        ),
    ]
    last_name: Annotated[
        str,
        StringConstraints(
            min_length=0,
            max_length=30,
            pattern=str_regexp,
            strip_whitespace=True,
        ),
    ]
    phone_number: Annotated[
        str,
        StringConstraints(
            min_length=11,
            max_length=11,
            pattern=r"^1\d{10}$",
        ),
    ]
    email: EmailStr
    street: Annotated[
        str,
        StringConstraints(
            min_length=1,
            max_length=30,
            strip_whitespace=True,
        ),
    ]
    start_datetime: datetime
    selected_service: SelectedService
    clean_oven: bool = Field(default=False)
    clean_windows: bool = Field(default=False)
    clean_basement: bool = Field(default=False)
    move_in_cleaning: bool = Field(default=False)
    move_out_cleaning: bool = Field(default=False)
    clean_fridge: bool = Field(default=False)
    building: BuildingType
    rooms_number: int
    square_feet: int
    use_equipment: bool


def validate_by_booking_scheme():

    def decorator(func):

        def wrapper(self, *args, **kwargs):
            try:
                data: dict = request.json
                print(data)
                first_name: str = data.get("first_name")
                last_name: str = data.get("last_name", "")
                phone_number: str = data.get("phone_number")
                email: Union[EmailStr, str] = data.get("email")
                street: str = data.get("street")
                start_datetime = datetime.fromisoformat(data.get("start_datetime"))
                selected_service: Union[SelectedService, str] = data.get(
                    "selected_service"
                )

                # Checkboxes
                clean_oven: bool = is_checkbox_on(data.get("clean_oven"))
                clean_windows: bool = is_checkbox_on(data.get("clean_windows"))
                clean_basement: bool = is_checkbox_on(data.get("clean_basement"))
                move_in_cleaning: bool = is_checkbox_on(data.get("move_in_cleaning"))
                move_out_cleaning: bool = is_checkbox_on(data.get("move_out_cleaning"))
                clean_fridge: bool = is_checkbox_on(data.get("clean_fridge"))

                building: Union[BuildingType, str] = data.get("building")
                rooms_number = abs(int(data.get("rooms_number")))
                square_feet = abs(int(data.get("square_feet")))
                use_equipment = convert_str_to_bool(data.get("use_equipment"))

                booking = BookingScheme(
                    first_name=first_name,
                    last_name=last_name,
                    phone_number=phone_number,
                    email=email,
                    street=street,
                    start_datetime=start_datetime,
                    selected_service=selected_service,
                    clean_oven=clean_oven,
                    clean_windows=clean_windows,
                    clean_basement=clean_basement,
                    move_in_cleaning=move_in_cleaning,
                    move_out_cleaning=move_out_cleaning,
                    clean_fridge=clean_fridge,
                    building=building,
                    rooms_number=rooms_number,
                    square_feet=square_feet,
                    use_equipment=use_equipment,
                )
                print(booking)

            except ValidationError as e:
                return Response(
                    status=422,
                    content_type="application/json",
                    response=json.dumps(e.json()),
                )
            except ValueError as e:
                return Response(
                    status=400,
                    content_type="application/json",
                    response=json.dumps('{"message": "' + str(e) + '" }'),
                )
            return func(self, booking, *args, **kwargs)

        return wrapper

    return decorator
