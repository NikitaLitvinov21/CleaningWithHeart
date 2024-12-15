from datetime import datetime
from typing import Annotated

from pydantic import StringConstraints

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
    street: Annotated[
        str,
        StringConstraints(
            min_length=1,
            max_length=30,
            strip_whitespace=True,
        ),
    ]
    datetime_local: datetime
