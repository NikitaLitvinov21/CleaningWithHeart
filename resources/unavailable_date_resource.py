from datetime import datetime

from flask import Response, json, request
from flask_login import login_required
from flask_restful import Resource

from common.utils.datetime_util import iso_string_to_datetime_utc
from services.unavailable_date_service import UnavailableDateService


class UnavailableDateResource(Resource):
    def __init__(self):
        self.service = UnavailableDateService()

    @login_required
    def post(self) -> Response:
        data = request.get_json()
        try:
            start_datetime: datetime = iso_string_to_datetime_utc(
                data.get("startDatetime")
            )
            finish_datetime: datetime = iso_string_to_datetime_utc(
                data.get("finishDatetime")
            )
        except Exception:
            return Response(
                status=400,
                content_type="application/json",
                response=json.dumps({"message": "Invalid datetime format"}),
            )

        entry = self.service.create_unavailable_date(
            start_datetime=start_datetime,
            finish_datetime=finish_datetime,
        )
        return Response(
            status=201,
            content_type="application/json",
            response=json.dumps(entry.to_dict()),
        )

    @login_required
    def get(self) -> Response:
        entries = self.service.retrieve_all()
        return Response(
            status=200,
            content_type="application/json",
            response=json.dumps([entry.to_dict() for entry in entries]),
        )

    @login_required
    def delete(self, id_: int) -> Response:
        self.service.delete_unavailable_date(id_)
        return Response(
            status=200,
            content_type="application/json",
            response=json.dumps({"message": "Unavailable date removed"}),
        )
