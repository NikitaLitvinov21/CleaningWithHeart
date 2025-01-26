from typing import Annotated, Optional, Union

from flask import Response, json, request
from pydantic import EmailStr, StringConstraints, ValidationError

from schemes.scheme import Scheme

str_regexp = r"^[^\d\!\@\#\$\%\^\&\*\=\+\~\/\+\;\:\?\{\}]*$"


class CustomerScheme(Scheme):
    first_name: Annotated[
        str,
        StringConstraints(
            min_length=1,
            max_length=30,
            pattern=str_regexp,
            strip_whitespace=True,
        ),
    ]
    last_name: Optional[
        Annotated[
            str,
            StringConstraints(
                min_length=0,
                max_length=30,
                pattern=str_regexp,
                strip_whitespace=True,
            ),
        ]
    ] = None
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
            max_length=255,
            strip_whitespace=True,
        ),
    ]
    special_notes: Optional[str] = None


def validate_by_customer_scheme():
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            try:
                data: dict = request.json
                first_name: str = data.get("firstName")
                last_name: str = data.get("lastName", "")
                phone_number: str = data.get("phoneNumber")
                email: Union[EmailStr, str] = data.get("email")
                street: str = data.get("street")
                special_notes: Optional[str] = data.get("specialNotes")

                customer = CustomerScheme(
                    first_name=first_name,
                    last_name=last_name,
                    phone_number=phone_number,
                    email=email,
                    street=street,
                    special_notes=special_notes,
                )

            except ValidationError as e:
                return Response(
                    status=422,
                    content_type="application/json",
                    response=e.json(),
                )
            except (ValueError, TypeError) as e:
                return Response(
                    status=400,
                    content_type="application/json",
                    response=json.dumps({"message": str(e)}),
                )
            return func(self, customer=customer, *args, **kwargs)

        return wrapper

    return decorator
