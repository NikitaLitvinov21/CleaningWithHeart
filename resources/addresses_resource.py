from typing import List

from flask import Response, json, request
from flask_restful import Resource
from requests import HTTPError

from services.addresses_service import AddressesService


class AddressesResource(Resource):

    def __init__(self):
        self.addresses_service = AddressesService()

    # login not required here!
    def get(self) -> Response:
        message: str = "Your search query is too short!"
        search: str = request.args.get("search", "")

        if len(search) > 0:
            try:
                addresses: List[str] = self.addresses_service.find_addresses(
                    search=search,
                )
                return Response(
                    status=200,
                    content_type="application/json",
                    response=json.dumps(
                        {"addresses": addresses},
                    ),
                )
            except HTTPError as error:
                message = error.strerror
            except Exception as exception:
                message = str(exception)

        return Response(
            status=400,
            content_type="application/json",
            response=json.dumps(
                {"message": message},
            ),
        )
