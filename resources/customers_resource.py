from typing import List

from flask import Response, json, request
from flask_login import login_required
from flask_restful import Resource

from common.utils.queryparams_util import get_bool_from_arg
from models.customer import Customer
from schemes.customer_scheme import CustomerScheme, validate_by_customer_scheme
from services.customer_service import CustomerService


class CustomersResource(Resource):
    def __init__(self):
        self.customer_service = CustomerService()

    @login_required
    def get(self) -> Response:
        try:
            only_names = get_bool_from_arg("only_names")
            customers: List[Customer] = self.customer_service.retrieve_customers(
                limit=int(request.args.get("limit", 20)),
                page=int(request.args.get("page", 1)),
                only_names=only_names,
            )
            customers_count: int = self.customer_service.retrieve_customer_count()

            if only_names:
                customers_dict: List[dict] = [
                    {
                        "id": customer.id,
                        "name": customer.first_name + " " + customer.last_name,
                    }
                    for customer in customers
                ]
            else:
                customers_dict = [customer.to_dict() for customer in customers]

            return Response(
                status=200,
                content_type="application/json",
                response=json.dumps(
                    {
                        "customers": customers_dict,
                        "count": customers_count,
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
    @validate_by_customer_scheme()
    def post(self, customer: CustomerScheme) -> Response:
        if self.customer_service.is_customer_exists(
            phone_number=customer.phone_number,
        ):
            message = "The customer with this phone number already exists!"
            return Response(
                status=409,
                content_type="application/json",
                response=json.dumps(
                    {
                        "message": message,
                    },
                ),
            )

        self.customer_service.create_customer(
            first_name=customer.first_name,
            last_name=customer.last_name,
            phone_number=customer.phone_number,
            email=customer.email,
            street=customer.street,
            special_notes=customer.special_notes,
        )
        return Response(
            status=201,
            content_type="application/json",
            response=json.dumps({"message": "Customer created successfully!"}),
        )
