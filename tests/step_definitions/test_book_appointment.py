"""
Feature test for book_appointment.feature
"""

# pylint: disable=redefined-outer-name

import datetime
import os

import pytest
from pytest_bdd import given, scenarios, then, when

from src.appointment.appointment_types import AppointmentType
from src.helpers.app_date_time import get_future
from tests.utils.factories.appointment_factory import AppointmentFactory
from tests.utils.factories.person_factory import PersonFactory

current_dir = os.path.dirname(__file__)
feature_file_path = os.path.join(
    current_dir, "..", "features", "book_appointment.feature"
)
scenarios(feature_file_path)


@pytest.fixture
def tomorrow_9am() -> datetime.datetime:
    """Tomorrow 9am Fixture"""
    return get_future(days=1).replace(hour=9, minute=00)


@pytest.fixture
@given("the practitioner schedule is empty for tomorrow 9am standard appointment")
def init_practitioner():
    """Initialize the practitioner"""
    return PersonFactory.get_practitioner()


@pytest.fixture
@given("the practitioner has an initial appointment for tomorrow 9am")
def init_practitioner_with_appointment(tomorrow_9am):
    """Initialize the practitioner with an initial appointment"""
    practitioner = PersonFactory.get_practitioner()

    appointment = AppointmentFactory.get_appointment(
        start_date_time=tomorrow_9am.strftime("%Y%m%d%H%M"),
        appointment_type=AppointmentType.INITIAL_CONSULTATION,
    )

    practitioner.add_appointment(appointment)
    return practitioner


@when("the patient books a standard appointment for a tomorrow 9am")
def book_standard_appointment(init_practitioner, tomorrow_9am):
    """Book an appointment for tomorrow 9am"""
    appointment = AppointmentFactory.get_appointment(
        start_date_time=tomorrow_9am.strftime("%Y%m%d%H%M"),
        appointment_type=AppointmentType.STANDARD,
    )
    init_practitioner.add_appointment(appointment)


@when("the patient tries booking a standard appointment for a tomorrow 9am")
def try_booking_standard_appointment(init_practitioner_with_appointment, tomorrow_9am):
    """Try booking an appointment for tomorrow 9am and fail"""
    appointment = AppointmentFactory.get_appointment(
        start_date_time=tomorrow_9am.strftime("%Y%m%d%H%M"),
        appointment_type=AppointmentType.STANDARD,
    )
    try:
        init_practitioner_with_appointment.add_appointment(appointment)
    except ValueError:
        pass


@then(
    "the practitioner can see the new standard appointment on their schedule for tomorrow 9am"
)
def check_new_appointment(init_practitioner, tomorrow_9am):
    """Check practitioners schedule to verify booking is confirmed"""
    schedule = init_practitioner.get_schedule(tomorrow_9am.strftime("%Y-%m-%d"))
    assert tomorrow_9am.strftime("%Y%m%d%H%M") in schedule


@then(
    "the practitioner see the old initial appointment on their schedule for tomorrow 9am"
)
def check_old_appointment(init_practitioner_with_appointment, tomorrow_9am):
    """Check practitioners schedule to verify booking is NOT confirmed"""
    schedule = init_practitioner_with_appointment.get_schedule(
        tomorrow_9am.strftime("%Y-%m-%d")
    )
    key = tomorrow_9am.strftime("%Y%m%d%H%M")
    assert (
        key in schedule
        and schedule[key].appointment_type == AppointmentType.INITIAL_CONSULTATION
    )
