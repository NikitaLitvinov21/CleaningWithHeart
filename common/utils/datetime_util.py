from datetime import datetime

ISO8601_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S"


def datetime_to_iso8601(datetime_instance: datetime) -> str:
    return datetime_instance.strftime(ISO8601_DATETIME_FORMAT)
