from flask import Response, request
from pydantic import ValidationError


def validate_by_scheme(scheme: type):
    """
    Decorator for validating input data via Pydantic scheme (use ClassName).

    Example of use:
    class BookingResource(Resource):

        @validate_by_scheme(BookingScheme)
        def post(self, booking: BookingScheme) -> dict:
            print(booking)
            ...
    """

    def decorator(func):
        def wrapper(self, *args, **kwargs):
            try:
                request_data = scheme(**request.json)
            except ValidationError as e:
                return Response(
                    status=422,
                    content_type="application/json",
                    response='{"Validating error": ' + str(e.errors()) + "}",
                )
            return func(self, request_data, *args, **kwargs)

        return wrapper

    return decorator
