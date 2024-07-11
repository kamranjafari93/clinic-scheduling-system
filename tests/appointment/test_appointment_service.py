"""
Test Cases for Appointment Service
"""

import datetime

import pytest

from src.appointment.appointment import AppointmentService as ApntmntSrvc
from src.appointment.appointment_constants import (
    APPOINTMENT_END_TIME,
    APPOINTMENT_MINIMUM_HOURS_DEADLINE,
    APPOINTMENT_START_TIME,
)
from src.appointment.appointment_types import AppointmentType
from src.helpers import app_date_time


class TestAppointmentService:
    """Test cases for appointment service"""

    def test_is_start_date_time_valid(self, faker_instance):
        """Test to see if is_start_date_time_valid validates inputs correctly"""

        # faker provider should generate a correct date_time
        correct_date_time = faker_instance.appointment_start_date_time()
        assert ApntmntSrvc.is_start_date_time_valid(correct_date_time) is True

        # faker provider should generate a correct date_time with our input
        correct_date_time = faker_instance.appointment_start_date_time(
            year=2024, month=8, day=2, hour=21, minute=24
        )
        assert ApntmntSrvc.is_start_date_time_valid(correct_date_time) is True

        # check if service methods flag these incorrect date_times
        incorrect_date_time = f"20231103{APPOINTMENT_END_TIME}00"  # Hour out of range
        assert ApntmntSrvc.is_start_date_time_valid(incorrect_date_time) is False

        incorrect_date_time = "202302301430"  # not existing date: 30th Feb
        assert ApntmntSrvc.is_start_date_time_valid(incorrect_date_time) is False

        incorrect_date_time = "202311031420"  # Wrong minute
        assert ApntmntSrvc.is_start_date_time_valid(incorrect_date_time) is False

        incorrect_date_time = "202311330830"  # Wrong day
        assert ApntmntSrvc.is_start_date_time_valid(incorrect_date_time) is False

        incorrect_date_time = "202313250830"  # Wrong month
        assert ApntmntSrvc.is_start_date_time_valid(incorrect_date_time) is False

        incorrect_date_time = "210013250830"  # Wrong year
        assert ApntmntSrvc.is_start_date_time_valid(incorrect_date_time) is False

        incorrect_date_time = "24113830"  # Wrong format of (202401130930)
        assert ApntmntSrvc.is_start_date_time_valid(incorrect_date_time) is False

    def test_create_all_possible_time_slots_past(self):
        """Test create_all_possible_time_slots for past dates"""

        # no possible time slot for past dates
        past_date_possible_time_slots = ApntmntSrvc.create_all_possible_time_slots(
            "2023-01-01"
        )
        assert len(past_date_possible_time_slots) == 0

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
    def test_create_all_possible_time_slots_today(self, now_hours_minutes: str):
        """Test create_all_possible_time_slots for today"""

        real_now = app_date_time.get_now()
        configured_now = f"{real_now.strftime('%Y%m%d')}{now_hours_minutes}"
        now = app_date_time.get_now(configured_now)
        today_possible_time_slots = ApntmntSrvc.create_all_possible_time_slots(
            now.strftime("%Y-%m-%d"), configured_now=configured_now
        )

        if now.hour > APPOINTMENT_END_TIME:
            assert not today_possible_time_slots
        else:
            if now.minute < 30:
                next_half_hour = now.replace(minute=30, second=0, microsecond=0)
            else:
                next_half_hour = now.replace(
                    hour=now.hour + 1, minute=0, second=0, microsecond=0
                )

            while next_half_hour < now + datetime.timedelta(hours=2):
                time_slot = (
                    f"{next_half_hour.year:04d}{next_half_hour.month:02d}{next_half_hour.day:02d}"
                    f"{next_half_hour.hour:02d}{next_half_hour.minute:02d}"
                )
                assert time_slot not in today_possible_time_slots
                next_half_hour += datetime.timedelta(minutes=30)

    def test_create_all_possible_time_slots_future(self):
        """Test create_all_possible_time_slots for future dates"""

        future_date = app_date_time.get_future(30)
        future_possible_time_slots = ApntmntSrvc.create_all_possible_time_slots(
            future_date.strftime("%Y-%m-%d")
        )

        all_possible_slots = ((APPOINTMENT_END_TIME - APPOINTMENT_START_TIME) * 2) + 1
        assert len(future_possible_time_slots) == all_possible_slots

    def test_extract_all_available_time_slots_past(self, faker_instance):
        """Test extract_all_possible_time_slots for past dates"""

        # no possible time slot for past dates
        past_date_possible_time_slots = ApntmntSrvc.create_all_possible_time_slots(
            "2023-01-01"
        )
        past_date_available_times = ApntmntSrvc.extract_all_available_time_slots(
            past_date_possible_time_slots, faker_instance.appointment_type(), {}
        )

        assert len(past_date_available_times) == 0

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
    def test_extract_all_available_time_slots_today(self, now_hours_minutes: str):
        """Test extract_all_possible_time_slots for check-ins (30 minutes) today"""

        real_now = app_date_time.get_now()
        configured_now = f"{real_now.strftime('%Y%m%d')}{now_hours_minutes}"
        now = app_date_time.get_now(configured_now)
        today_possible_time_slots = ApntmntSrvc.create_all_possible_time_slots(
            now.strftime("%Y-%m-%d"), configured_now=configured_now
        )
        today_available_times = ApntmntSrvc.extract_all_available_time_slots(
            today_possible_time_slots, AppointmentType.CHECK_INS, {}
        )

        configured_now_instance = datetime.datetime.strptime(
            configured_now, "%Y%m%d%H%M"
        )
        end_time_instance = datetime.datetime.strptime(
            f"{real_now.strftime('%Y%m%d')}"
            f"{APPOINTMENT_END_TIME - APPOINTMENT_MINIMUM_HOURS_DEADLINE}00",
            "%Y%m%d%H%M",
        )

        if (
            configured_now_instance.hour
            >= APPOINTMENT_END_TIME - APPOINTMENT_MINIMUM_HOURS_DEADLINE
        ):
            assert len(today_available_times) == 0
        elif (
            configured_now_instance.hour
            < APPOINTMENT_START_TIME - APPOINTMENT_MINIMUM_HOURS_DEADLINE
        ):
            assert (
                len(today_available_times)
                == (APPOINTMENT_END_TIME - APPOINTMENT_START_TIME) * 2
            )
        else:
            minutes_difference = (
                (abs(configured_now_instance - end_time_instance)).total_seconds()
            ) / 60
            assert len(today_available_times) == int(minutes_difference // 30)

    def test_extract_all_available_time_slots_future(self):
        """Test extract_all_possible_time_slots for future"""

        # future possible time slots
        future_date = app_date_time.get_future(30)
        future_possible_time_slots = ApntmntSrvc.create_all_possible_time_slots(
            future_date.strftime("%Y-%m-%d")
        )

        future_available_times = ApntmntSrvc.extract_all_available_time_slots(
            future_possible_time_slots, AppointmentType.CHECK_INS, {}
        )

        assert len(future_possible_time_slots) == len(future_available_times) + 1
