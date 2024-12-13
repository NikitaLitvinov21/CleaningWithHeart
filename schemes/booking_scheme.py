from datetime import datetime

from pydantic import constr

from schemes.scheme import Scheme

str_regexp = "^[^\d\!\@\#\$\%\^\&\*\=\+\~\/\+\;\:\?\{\}]*$"


class BookingScheme(Scheme):

    first_name: constr(
        min_length=1,
        max_length=30,
        regex=str_regexp,
    )
    last_name: constr(
        min_length=1,
        max_length=30,
        regex=str_regexp,
    )
    phone_number: constr(
        min_length=11,
        max_length=11,
        regex="^1\d{10}$",
    )
    street: constr(
        min_length=1,
        max_length=30,
    )
    datetime_local: datetime
