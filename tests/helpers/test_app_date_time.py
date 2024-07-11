"""
Test Cases App Date Time helpers
"""

import datetime

import pytz

from src.appointment.appointment_constants import APPOINTMENT_MINIMUM_HOURS_DEADLINE
from src.helpers import app_date_time


def test_get_now_without_argument():
    """Test get_now method on default mode"""
    method_now = app_date_time.get_now()

    tz = pytz.timezone("America/Vancouver")
    real_now = datetime.datetime.now(tz)

    assert (
        method_now.date() == real_now.date()
        and method_now.hour == real_now.hour
        and method_now.minute == real_now.minute
    )


def test_get_now_with_argument():
    """Test get_now method with a configured argument"""
    method_now = app_date_time.get_now(now="202401201430")

    assert (
        method_now.year == 2024
        and method_now.month == 1
        and method_now.day == 20
        and method_now.hour == 14
        and method_now.minute == 30
    )


def test_get_future():
    """Test get_future method"""
    method_future = app_date_time.get_future()

    tz = pytz.timezone("America/Vancouver")
    real_future = datetime.datetime.now(tz) + datetime.timedelta(days=30)

    assert (
        method_future.date() == real_future.date()
        and method_future.hour == real_future.hour
        and method_future.minute == real_future.minute
    )


def test_is_timespan_difference_acceptable():
    """Test is_timespan_difference_acceptable method"""
    tz = pytz.timezone("America/Vancouver")
    now = app_date_time.get_now()
    eligible_future = datetime.datetime.now(tz) + datetime.timedelta(
        hours=APPOINTMENT_MINIMUM_HOURS_DEADLINE + 1
    )
    not_eligible_future = datetime.datetime.now(tz) + datetime.timedelta(
        hours=APPOINTMENT_MINIMUM_HOURS_DEADLINE - 1
    )

    assert app_date_time.is_timespan_difference_acceptable(now, eligible_future) is True

    assert (
        app_date_time.is_timespan_difference_acceptable(now, not_eligible_future)
        is False
    )
