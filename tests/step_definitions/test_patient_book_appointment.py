"""
Feature test for patient_book_appointment.feature
"""

# pylint: disable=redefined-outer-name

import os

import pytest
from pytest_bdd import given, scenarios, then, when

from src.appointment.appointment_types import AppointmentType
from src.helpers.app_date_time import get_now
from tests.utils.factories.appointment_factory import AppointmentFactory
from tests.utils.factories.person_factory import PersonFactory

current_dir = os.path.dirname(__file__)
feature_file_path = os.path.join(
    current_dir, "..", "features", "patient_book_appointment.feature"
)
scenarios(feature_file_path)


@pytest.fixture(scope="session")
def practitioner():
    """Initialize the practitioner"""
    return PersonFactory.get_practitioner()


@pytest.fixture(scope="session")
def practitioner_2():
    """Initialize the practitioner"""
    return PersonFactory.get_practitioner()


@pytest.fixture(scope="session")
def configured_now() -> str:
    """configured_now"""
    real_now = get_now()
    return f"{real_now.strftime('%Y%m%d')}0530"


@given("the practitioner schedule is filled with some appointments")
def init_practitioner_with_appointments(practitioner, configured_now):
    """Inject some appointments to the practitioner's schedule"""
    previous_appointments = [
        ("0900", AppointmentType.INITIAL_CONSULTATION),
        ("1030", AppointmentType.CHECK_INS),
        ("1100", AppointmentType.CHECK_INS),
        ("1500", AppointmentType.STANDARD),
        ("1600", AppointmentType.STANDARD),
    ]

    real_now = get_now()

    for item in previous_appointments:
        start_date_time = f"{real_now.strftime('%Y%m%d')}{item[0]}"
        appointment = AppointmentFactory.get_appointment(
            start_date_time=start_date_time,
            appointment_type=item[1],
        )
        practitioner.add_appointment(appointment, configured_now=configured_now)


@given("the practitioner schedule is filled with some appointments in the morning")
def init_practitioner_with_appointments_morning(practitioner_2, configured_now):
    """Inject some appointments to the practitioner's schedule"""
    previous_appointments = [
        ("0900", AppointmentType.INITIAL_CONSULTATION),
        ("1030", AppointmentType.CHECK_INS),
        ("1100", AppointmentType.STANDARD),
    ]

    real_now = get_now()

    for item in previous_appointments:
        start_date_time = f"{real_now.strftime('%Y%m%d')}{item[0]}"
        appointment = AppointmentFactory.get_appointment(
            start_date_time=start_date_time,
            appointment_type=item[1],
        )
        practitioner_2.add_appointment(appointment, configured_now=configured_now)


@when("the patient books a standard appointment for an available time slot")
def book_standard_appointment(practitioner, configured_now):
    """Book a standard appointment for today at 14"""
    patient = PersonFactory.get_patient(name="John Doe")

    real_now = get_now()
    appointment = AppointmentFactory.get_appointment(
        start_date_time=f"{real_now.strftime('%Y%m%d')}1300",
        appointment_type=AppointmentType.STANDARD,
        patient=patient,
    )
    practitioner.add_appointment(appointment, configured_now=configured_now)


@when("the patient books a initial appointment for an unavailable time slot")
def book_initial_appointment(practitioner_2, configured_now):
    """Book an initial appointment for today at 10 which is not available"""
    patient = PersonFactory.get_patient(name="John Smith")

    real_now = get_now()
    appointment = AppointmentFactory.get_appointment(
        start_date_time=f"{real_now.strftime('%Y%m%d')}1000",
        appointment_type=AppointmentType.INITIAL_CONSULTATION,
        patient=patient,
    )

    try:
        practitioner_2.add_appointment(appointment, configured_now=configured_now)
    except ValueError:
        pass


@then(
    "the practitioner can see the new standard appointment on their schedule for that patient"
)
def check_new_appointment(practitioner, configured_now):
    """Check practitioners schedule to verify booking is confirmed"""
    real_now = get_now()
    schedule = practitioner.get_today_schedule(configured_now=configured_now)

    key = f"{real_now.strftime('%Y%m%d')}1300"
    assert (
        key in schedule
        and schedule[key].appointment_type == AppointmentType.STANDARD
        and schedule[key].patient.name == "John Doe"
    )


@then("the appointment is not added to the schedule of the practitioner")
def check_unavailable_appointment(practitioner_2, configured_now):
    """Check practitioners schedule to verify booking is not confirmed"""
    real_now = get_now()
    schedule = practitioner_2.get_today_schedule(configured_now=configured_now)

    key = f"{real_now.strftime('%Y%m%d')}1000"
    assert key not in schedule
