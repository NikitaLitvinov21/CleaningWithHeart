from datetime import datetime
from typing import List

from flask import Response, json, request
from flask_login import login_required
from flask_restful import Resource

from schemes.event_scheme import EventScheme
from services.events_service import EventsService


class EventsResource(Resource):

    def __init__(self):
        self.events_service = EventsService()

    @login_required
    def get(self) -> Response:

        try:
            start_datetime = datetime.fromisoformat(request.args["start"])
            finish_datetime = datetime.fromisoformat(request.args["end"])
        except ValueError:
            return Response(
                status=400,
                content_type="application/json",
                response=json.dumps({"message": "Incorrect start and end!"}),
            )

        try:
            events: List[EventScheme] = self.events_service.retrieve_events(
                start_datetime=start_datetime,
                finish_datetime=finish_datetime,
            )
            return Response(
                status=200,
                content_type="application/json",
                response=json.dumps([event.to_dict() for event in events]),
            )
        except ValueError as e:
            return Response(
                status=400,
                content_type="application/json",
                response=json.dumps({"message": str(e)}),
            )
