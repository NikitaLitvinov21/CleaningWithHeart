from datetime import datetime

from common.utils.datetime_util import datetime_to_str
from schemes.scheme import Scheme


class EventScheme(Scheme):
    id: int
    title: str
    start_datetime: datetime
    finish_datetime: datetime

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "start": datetime_to_str(self.start_datetime),
            "end": datetime_to_str(self.finish_datetime),
        }
