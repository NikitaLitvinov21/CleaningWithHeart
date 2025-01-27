from flask import Response, json
from flask_login import login_required
from flask_restful import Resource

from common.exceptions.entity_not_found_exception import EntityNotFoundException
from models.customer import Customer
from schemes.customer_scheme import CustomerScheme, validate_by_customer_scheme
from services.customer_service import CustomerService


class CustomerResource(Resource):
    def __init__(self):
        self.customer_service = CustomerService()

    @login_required
    def get(self, customer_id: int) -> Response:
        try:
            customer: Customer = self.customer_service.retrieve_customer_by_id(
                customer_id=customer_id
            )
            return Response(
                status=200,
                content_type="application/json",
                response=json.dumps(customer.to_dict()),
            )
        except EntityNotFoundException as e:
            return Response(
                status=404,
                content_type="application/json",
                response=json.dumps({"message": str(e)}),
            )

    @login_required
    @validate_by_customer_scheme()
    def put(self, customer_id: int, customer: CustomerScheme) -> Response:
        try:
            self.customer_service.update_customer(
                customer_id=customer_id,
                first_name=customer.first_name,
                last_name=customer.last_name,
                phone_number=customer.phone_number,
                email=customer.email,
                street=customer.street,
                special_notes=customer.special_notes,
            )
            return Response(
                status=200,
                content_type="application/json",
                response=json.dumps({"message": "Customer updated successfully!"}),
            )
        except EntityNotFoundException as e:
            return Response(
                status=404,
                content_type="application/json",
                response=json.dumps({"message": str(e)}),
            )

    @login_required
    def delete(self, customer_id: int) -> Response:
        try:
            self.customer_service.delete_customer(customer_id=customer_id)
            return Response(
                status=200,
                content_type="application/json",
                response=json.dumps({"message": "Customer deleted successfully!"}),
            )
        except EntityNotFoundException as e:
            return Response(
                status=404,
                content_type="application/json",
                response=json.dumps({"message": str(e)}),
            )
