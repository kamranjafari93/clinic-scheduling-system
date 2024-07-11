"""
App date time helpers
"""

import datetime
from typing import Optional

import pytz

from src.appointment.appointment_constants import APPOINTMENT_MINIMUM_HOURS_DEADLINE


def get_now(now: Optional[str] = None) -> datetime.datetime:
    """Returns the current datetime in the America/Vancouver timezone,
    or a specified datetime interpreted as being in that timezone.

    Args:
        now (Optional[str]): A datetime string in the format 'YYYYMMDDHHMM'
            that will be used as the current datetime. If None, the actual current
            datetime will be used.

    Returns:
        datetime.datetime: The current or specified datetime in the America/Vancouver timezone.
    """
    tz = pytz.timezone("America/Vancouver")
    if now:
        now_datetime = datetime.datetime.strptime(now, "%Y%m%d%H%M")
        now_datetime = tz.localize(now_datetime)
    else:
        now_datetime = datetime.datetime.now(tz)

    return now_datetime


def get_future(days: int = 30) -> datetime.datetime:
    """Returns 30 days later datetime in the America/Vancouver timezone,
    or a specified future datetime in DAYS interpreted as being in that timezone.

    Args:
        days (int): future datetime will be made based on these number of days

    Returns:
        datetime.datetime: The future or specified datetime in the America/Vancouver timezone.
    """
    tz = pytz.timezone("America/Vancouver")
    return datetime.datetime.now(tz) + datetime.timedelta(days=days)


def is_timespan_difference_acceptable(
    date_1: datetime.datetime, date_2: datetime.datetime
) -> bool:
    """Check if the difference between two datetime objects is more than the
        booking limitation.

    Args:
        date_1 (datetime.datetime): date 1 to compare
        date_2 (datetime.datetime): date 1 to compare

    Returns:
        bool: whether the difference is acceptable or not
    """

    time_difference = abs(date_1 - date_2)
    minimum_deadline_hours = datetime.timedelta(
        hours=APPOINTMENT_MINIMUM_HOURS_DEADLINE
    )

    return time_difference >= minimum_deadline_hours
