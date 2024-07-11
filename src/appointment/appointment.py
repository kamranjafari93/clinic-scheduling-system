"""
Appointment Model: -
Appointment Service:
Providing utilities needed to work with Appointment model
"""

import datetime
import random
import re
import uuid
from typing import Optional, Set

import pytz

from src.appointment.appointment_constants import (
    APPOINTMENT_END_TIME,
    APPOINTMENT_MINIMUM_HOURS_DEADLINE,
    APPOINTMENT_MINUTES,
    APPOINTMENT_START_TIME,
)
from src.appointment.appointment_types import AppointmentType
from src.helpers import app_date_time
from src.person.patient import Patient


class Appointment:
    """
    Represents an Appointment.

    Attributes:
        __id (str): The unique id of the appointment.
        __start_date_time (str): The start date and time of the appointment.
        __appointment_type (AppointmentType): type of the appointment
        __patient (Patient): The patient who has booked the appointment
    """

    def __init__(
        self, start_date_time: str, appointment_type: AppointmentType, patient: Patient
    ) -> None:
        """
        Initialize a new appointment.

        Args:
            start_date_time (str): The start date and time of the appointment.
            appointment_type (AppointmentType): Type of the appointment
            patient (Patient): The patient who has booked the appointment
        """
        self.__id = f"appointment-{str(uuid.uuid4())}"
        self.__start_date_time = start_date_time
        self.__appointment_type = appointment_type
        self.__patient = patient

    @property
    def id(self) -> str:
        """
        Get the id of the appointment.

        Returns:
            str: The id of the clinic.
        """
        return self.__id

    @property
    def start_date_time(self) -> str:
        """
        Get the start date and time of the appointment

        Returns:
            str: The start date and time of the appointment.
        """
        return self.__start_date_time

    @property
    def appointment_type(self) -> AppointmentType:
        """
        Get the type of the appointment

        Returns:
            AppointmentType: The type of the appointment.
        """
        return self.__appointment_type

    @property
    def patient(self) -> Patient:
        """
        Get the patient of the appointment

        Returns:
            Patient: The patient of the appointment.
        """
        return self.__patient


class AppointmentService:
    """A service class to facilitate interactions with Appointment model"""

    @staticmethod
    def is_start_date_time_valid(start_date_time: str) -> bool:
        """
        This method validates the provided start_date_time.
        The acceptable format is 'YYYYMMDDHHMM' like 202405031600
        All other constraints is also considered like 9am-17pm, etc

        Args:
            start_date_time (str): start date_time of the appointment
        Returns:
            bool: whether the provided format is correct or not
        """

        def create_hours_regex(start: int, end: int):
            """create regex for hours"""
            hours = [f"{h:02d}" for h in range(start, end)]
            return f"({'|'.join(hours)})"

        def create_minutes_regex(minutes: Set):
            """create regex for minutes"""
            return f"({'|'.join(f'{m:02d}' for m in minutes)})"

        # Pattern "YYYYMMDDHHMM" : YYYY(2000-2099) MM(01-12) DD(01-31) HH(09-16) MM(00|30)
        start_time = APPOINTMENT_START_TIME
        end_time = APPOINTMENT_END_TIME

        pattern = (
            r"^(?P<year>20\d{2})"
            "(?P<month>0[1-9]|1[0-2])"
            "(?P<day>0[1-9]|[12]\\d|3[01])"
            f"(?P<hour>{create_hours_regex(start_time, end_time)})"
            f"(?P<minute>{create_minutes_regex(APPOINTMENT_MINUTES)})$"
        )
        date_time_regex = re.compile(pattern)

        match = date_time_regex.fullmatch(start_date_time)
        if not match:
            return False

        # checking if the datetime truly exists (leap year or other scenarios)
        year, month, day, hour, minute = map(
            int,
            [
                match.group("year"),
                match.group("month"),
                match.group("day"),
                match.group("hour"),
                match.group("minute"),
            ],
        )

        try:
            datetime.datetime(year, month, day, hour, minute)
            return True
        except ValueError:
            return False

    @staticmethod
    def generate_start_date_time(
        year: Optional[int] = None,
        month: Optional[int] = None,
        day: Optional[int] = None,
        hour: Optional[int] = None,
        minute: Optional[int] = None,
    ) -> str:
        """
        Generate a valid appointment start_date_time in the format 'YYYYMMDDHHMM'

        Args:
            year (Optional[int]): Year of the appointment (2000-2099 if not specified).
            month (Optional[int]): Month of the appointment (1-12 if not specified).
            day (Optional[int]): Day of the appointment (1-31 if not specified).
            hour (Optional[int]): Hour of the appointment (9-16 if not specified).
            minute (Optional[int]): Minute of the appointment (0, 30 if not specified).

        if the provided arguments are wrong, this method use its own default valid ranges

        Returns:
            str: Representing the start date time of the appointment in 'YYYYMMDDHHMM'.
        """
        if year is None:
            year = random.randint(2000, 2099)

        if month is None:
            month = random.randint(1, 12)

        last_day_of_month = (
            datetime.datetime(year, month, 1) + datetime.timedelta(days=31)
        ).replace(day=1) - datetime.timedelta(days=1)
        last_day = last_day_of_month.day

        if day is None or day < 1 or day > last_day:
            day = random.randint(1, last_day)

        if (
            hour is None
            or hour < APPOINTMENT_START_TIME
            or hour > APPOINTMENT_END_TIME - APPOINTMENT_MINIMUM_HOURS_DEADLINE
        ):
            hour = random.randint(
                APPOINTMENT_START_TIME,
                APPOINTMENT_END_TIME - APPOINTMENT_MINIMUM_HOURS_DEADLINE,
            )

        if minute not in list(APPOINTMENT_MINUTES):
            minute = random.choice(list(APPOINTMENT_MINUTES))

        return f"{year:04d}{month:02d}{day:02d}{hour:02d}{minute:02d}"

    @staticmethod
    def create_all_possible_time_slots(
        requested_date: str, configured_now: Optional[str] = None
    ) -> dict[str, None]:
        """
        This method creates a dictionary consisting of all possible keys
        for a specific date

        Args:
            requested_date (str): date of the appointment => e.g 2024-05-04
            configured_now (Optional[str]): Optional now parameter for configuring NOW
                           (specific scenarios or test cases). format: 'YYYYMMDDHHMM'
        Returns:
            dict[str, None]: A dictionary of all possible time slots
        """
        schedule: dict[str, None] = {}

        now = app_date_time.get_now(configured_now)
        req_date = datetime.datetime.strptime(requested_date, "%Y-%m-%d")

        start_time = APPOINTMENT_START_TIME

        if now.date() > req_date.date():
            return schedule

        if now.date() == req_date.date():
            if now.hour >= APPOINTMENT_END_TIME - APPOINTMENT_MINIMUM_HOURS_DEADLINE:
                return schedule

            if now.hour > APPOINTMENT_START_TIME:
                start_time = now.hour

        for hour in range(start_time, APPOINTMENT_END_TIME + 1):
            for minute in APPOINTMENT_MINUTES:
                if hour == APPOINTMENT_END_TIME and minute != 0:
                    break

                key = (
                    f"{req_date.year:04d}{req_date.month:02d}"
                    f"{req_date.day:02d}{hour:02d}{minute:02d}"
                )

                # make sure deadline timespan is met
                key_date_time = datetime.datetime.strptime(key, "%Y%m%d%H%M")
                vancouver_timezone = pytz.timezone("America/Vancouver")
                key_date_time_timezone = vancouver_timezone.localize(key_date_time)
                if app_date_time.is_timespan_difference_acceptable(
                    key_date_time_timezone, now
                ):
                    schedule[key] = None

        return schedule

    @staticmethod
    def extract_all_available_time_slots(
        possible_time_slots: dict[str, None],
        requested_appointment_type: AppointmentType,
        current_schedule: dict[str, Appointment],
    ) -> dict[str, None]:
        """
        This method extracts all available time slots from a possible schedule

        Args:
            possible_time_slots (dict[str, None]): possible time slots
            requested_appointment_type (AppointmentType): type of the appointment
            current_schedule (dict[str, None]): current booked appointments
        Returns:
            dict[str, None]: A dictionary of all available time slots
        """
        available_time_slots: dict[str, None] = {}

        if not possible_time_slots:
            return available_time_slots

        available_time_slots = {
            start_date_time: None
            for start_date_time, _ in possible_time_slots.items()
            if start_date_time not in current_schedule
        }

        available_time_slots_filtered: dict[str, None] = {}
        for slot in available_time_slots:
            datetime_slot = datetime.datetime.strptime(slot, "%Y%m%d%H%M")

            next_slots = []
            if requested_appointment_type == AppointmentType.CHECK_INS:
                next_slots = [datetime_slot + datetime.timedelta(minutes=30)]
            elif requested_appointment_type == AppointmentType.STANDARD:
                next_slots = [
                    datetime_slot + datetime.timedelta(minutes=30),
                    datetime_slot + datetime.timedelta(hours=1),
                ]
            elif requested_appointment_type == AppointmentType.INITIAL_CONSULTATION:
                next_slots = [
                    datetime_slot + datetime.timedelta(minutes=30),
                    datetime_slot + datetime.timedelta(hours=1),
                    datetime_slot + datetime.timedelta(hours=1, minutes=30),
                ]

            should_add = True
            for next_slot in next_slots:
                formatted_next_slot = next_slot.strftime("%Y%m%d%H%M")
                if formatted_next_slot not in available_time_slots:
                    should_add = False

            if should_add:
                available_time_slots_filtered[slot] = None

        return available_time_slots_filtered
