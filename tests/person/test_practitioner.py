"""
Test Cases for Practitioner Model
"""

import datetime

import pytest
import pytz

from src.appointment.appointment import AppointmentService as ApntmntSrvc
from src.appointment.appointment_constants import (
    APPOINTMENT_END_TIME,
    APPOINTMENT_MINIMUM_HOURS_DEADLINE,
    APPOINTMENT_START_TIME,
)
from src.appointment.appointment_types import AppointmentType
from src.helpers import app_date_time
from tests.utils.factories.appointment_factory import AppointmentFactory
from tests.utils.factories.person_factory import PersonFactory


class TestPractitioner:
    """Test cases for practitioner model"""

    def test_id_property_getter(self):
        """Test getting the ID of the practitioner"""

        practitioner = PersonFactory.get_practitioner()
        assert practitioner.id is not None and isinstance(practitioner.id, str)

    def test_name_property_setter_getter(self, faker_instance):
        """Test name property getter and setter"""

        name = faker_instance.name()
        practitioner = PersonFactory.get_practitioner(name=name)
        assert name == practitioner.name

    def test_get_today_schedule(self):
        """Test get_today_schedule method"""

        practitioner = PersonFactory.get_practitioner()
        assert practitioner.get_today_schedule() == {}

    def test_get_schedule(self):
        """Test get_schedule method for a specific date"""
        future_date = app_date_time.get_future(1)

        practitioner = PersonFactory.get_practitioner()
        assert not practitioner.get_schedule(future_date.strftime("%Y-%m-%d"))

    def test_get_available_appointments_past(self):
        """
        Test get_available_appointments method
        Past availability should be empty
        """

        practitioner = PersonFactory.get_practitioner()
        practitioner_today_availability = practitioner.get_available_appointments(
            "2023-01-01", AppointmentType.CHECK_INS
        )

        assert len(practitioner_today_availability) == 0

    @pytest.mark.parametrize(
        "now_hours_minutes",
        [
            "0000",
            "0420",
            "1220",
            "2045",
            "2200",
            "2230",
            "2325",
            "2355",
            f"{APPOINTMENT_START_TIME - APPOINTMENT_MINIMUM_HOURS_DEADLINE:02}00",
            f"{APPOINTMENT_START_TIME - APPOINTMENT_MINIMUM_HOURS_DEADLINE:02}30",
            f"{APPOINTMENT_START_TIME - 1:02}30",
            f"{APPOINTMENT_START_TIME:02}30",
            f"{APPOINTMENT_START_TIME + 1:02}00",
            f"{APPOINTMENT_END_TIME:02}00",
            f"{APPOINTMENT_END_TIME - APPOINTMENT_MINIMUM_HOURS_DEADLINE:02}00",
            f"{APPOINTMENT_END_TIME - APPOINTMENT_MINIMUM_HOURS_DEADLINE:02}30",
        ],
    )
    def test_get_available_appointments_today(self, now_hours_minutes: str):
        """
        Test get_available_appointments method
        Today availability should be as equal to all possible slots as schedule is empty
        """
        real_now = app_date_time.get_now()
        configured_now = f"{real_now.strftime('%Y%m%d')}{now_hours_minutes}"
        now = app_date_time.get_now(configured_now)
        now_formatted = now.strftime("%Y-%m-%d")

        practitioner = PersonFactory.get_practitioner()
        practitioner_today_availability = practitioner.get_available_appointments(
            now_formatted, AppointmentType.CHECK_INS, configured_now=configured_now
        )

        today_possible_time_slots = ApntmntSrvc.create_all_possible_time_slots(
            now_formatted, configured_now=configured_now
        )

        assert len(practitioner_today_availability) == (
            len(today_possible_time_slots) - 1 if today_possible_time_slots else 0
        )

    def test_get_available_appointments_future(self):
        """
        Test get_available_appointments method
        Future availability should be as equal to all possible slots as schedule is empty
        """
        future_date = app_date_time.get_future(30)
        future_formatted = future_date.strftime("%Y-%m-%d")

        practitioner = PersonFactory.get_practitioner()
        practitioner_today_availability = practitioner.get_available_appointments(
            future_formatted, AppointmentType.CHECK_INS
        )

        today_possible_time_slots = ApntmntSrvc.create_all_possible_time_slots(
            future_formatted
        )

        assert (
            len(practitioner_today_availability) == len(today_possible_time_slots) - 1
        )

    @pytest.mark.parametrize(
        "now_hours_minutes",
        [
            "0000",
            "0420",
            "1220",
            "2045",
            "2200",
            "2230",
            "2325",
            "2355",
            f"{APPOINTMENT_START_TIME - APPOINTMENT_MINIMUM_HOURS_DEADLINE:02}00",
            f"{APPOINTMENT_START_TIME - APPOINTMENT_MINIMUM_HOURS_DEADLINE:02}30",
            f"{APPOINTMENT_START_TIME - 1:02}30",
            f"{APPOINTMENT_START_TIME:02}30",
            f"{APPOINTMENT_START_TIME + 1:02}00",
            f"{APPOINTMENT_END_TIME:02}00",
            f"{APPOINTMENT_END_TIME - APPOINTMENT_MINIMUM_HOURS_DEADLINE:02}00",
            f"{APPOINTMENT_END_TIME - APPOINTMENT_MINIMUM_HOURS_DEADLINE:02}30",
        ],
    )
    def test_add_appointment_today(self, now_hours_minutes: str):
        """
        Test get_add_appointment method
        Check if it is possible to add a new appointment for today
        """
        real_now = app_date_time.get_now()
        configured_now = f"{real_now.strftime('%Y%m%d')}{now_hours_minutes}"
        now = app_date_time.get_now(configured_now)
        now_formatted = now.strftime("%Y%m%d%H%M")

        appointment = AppointmentFactory.get_appointment(
            start_date_time=now_formatted,
            appointment_type=AppointmentType.CHECK_INS,
        )

        appointment_start_date_time = datetime.datetime.strptime(
            appointment.start_date_time, "%Y%m%d%H%M"
        )
        tz = pytz.timezone("America/Vancouver")
        appointment_start_date_time = tz.localize(appointment_start_date_time)

        practitioner = PersonFactory.get_practitioner()

        if (now.hour >= APPOINTMENT_END_TIME - APPOINTMENT_MINIMUM_HOURS_DEADLINE) or (
            not app_date_time.is_timespan_difference_acceptable(
                now, appointment_start_date_time
            )
        ):
            with pytest.raises(ValueError):
                practitioner.add_appointment(appointment)
        else:
            assert practitioner.add_appointment(appointment) is True

    def test_add_appointment_future(self):
        """
        Test get_add_appointment method
        Check if it is possible to add a new appointment for future
        """
        future_date = app_date_time.get_future(30)
        future_formatted = future_date.replace(hour=12, minute=30).strftime(
            "%Y%m%d%H%M"
        )

        appointment_standard = AppointmentFactory.get_appointment(
            start_date_time=future_formatted, appointment_type=AppointmentType.STANDARD
        )
        practitioner_1 = PersonFactory.get_practitioner()
        assert practitioner_1.add_appointment(appointment_standard) is True

        appointment_initial = AppointmentFactory.get_appointment(
            start_date_time=future_formatted,
            appointment_type=AppointmentType.INITIAL_CONSULTATION,
        )
        practitioner_2 = PersonFactory.get_practitioner()
        assert practitioner_2.add_appointment(appointment_initial) is True

        practitioner_3 = PersonFactory.get_practitioner()
        appointment_check_in = AppointmentFactory.get_appointment(
            start_date_time=future_formatted, appointment_type=AppointmentType.CHECK_INS
        )
        assert practitioner_3.add_appointment(appointment_check_in) is True
