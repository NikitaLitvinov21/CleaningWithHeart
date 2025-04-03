from datetime import datetime
from typing import Final, Optional
from zoneinfo import ZoneInfo

import pytz

from config import get_config

timezone_local = get_config("timezone")
ISO8601_DATETIME_FORMAT: Final = "%Y-%m-%dT%H:%M:%S"


def datetime_to_iso8601(datetime_instance: datetime) -> str:
    return datetime_instance.strftime(ISO8601_DATETIME_FORMAT)


def datetime_to_str(dt: Optional[datetime]) -> Optional[str]:
    """Convert datetime to local datetime string."""

    if dt is None:
        return ""
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=ZoneInfo("UTC"))
    dt = dt.astimezone(ZoneInfo(timezone_local))
    return dt.strftime(ISO8601_DATETIME_FORMAT)


def iso_string_to_datetime_utc(iso_string: str) -> datetime:

    client_time = datetime.fromisoformat(iso_string)

    # If the time already contains a time zone, simply convert to UTC
    if client_time.tzinfo is not None:
        return client_time.astimezone(pytz.UTC)

    # If not, we localize to the client's time zone
    client_timezone = pytz.timezone(timezone_local)
    localized_client_time: datetime = client_timezone.localize(client_time)

    # Convert to UTC
    return localized_client_time.astimezone(pytz.UTC)
