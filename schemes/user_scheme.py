from datetime import date
from typing import Annotated, Optional

from pydantic import StringConstraints

from schemes.scheme import Scheme


class UserScheme(Scheme):

    username: str
    password: str
    first_name: Optional[str]
    last_name: Optional[str]
    phone_number: Annotated[
        str,
        StringConstraints(
            min_length=11,
            max_length=11,
            pattern=r"^1\d{10}$",
        ),
    ]
    email_address: Optional[str]
    birth_date: Optional[date]
