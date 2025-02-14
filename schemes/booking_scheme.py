from datetime import datetime
from typing import Annotated, Optional

from pydantic import Field, StringConstraints

from enums.building_type import BuildingType
from enums.selected_service import SelectedService
from schemes.scheme import Scheme

str_regexp = r"^[^\d\!\@\#\$\%\^\&\*\=\+\~\/\+\;\:\?\{\}]*$"


class BookingScheme(Scheme):
    customer_id: Optional[int] = None
    cleaning_master_name: Optional[
        Annotated[
            str,
            StringConstraints(
                min_length=0,
                max_length=255,
                pattern=str_regexp,
                strip_whitespace=True,
            ),
        ]
    ]
    start_datetime: datetime
    finish_datetime: datetime
    selected_service: SelectedService
    has_clean_oven: bool = Field(default=False)
    has_clean_windows: bool = Field(default=False)
    has_clean_basement: bool = Field(default=False)
    has_move_in_cleaning: bool = Field(default=False)
    has_move_out_cleaning: bool = Field(default=False)
    has_clean_fridge: bool = Field(default=False)
    building: BuildingType
    rooms_number: int
    square_feet: int
    has_own_equipment: bool
