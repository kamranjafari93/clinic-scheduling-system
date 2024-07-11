"""
Practitioner Model
"""

import datetime
from typing import Optional

import pytz

from src.appointment.appointment import Appointment, AppointmentService
from src.appointment.appointment_types import AppointmentType
from src.person.person import Person


class Practitioner(Person):
    """
    Represents a practitioner.

    Attributes:
        __schedule (dict[str, Appointment]): The practitioner's schedule
    """

    def __init__(self, name: str):
        """
        Initialize a new practitioner

        Args:
            name (str): The practitioner's name that is passed to the Person parent class
        """
        super().__init__(name)

        self.__schedule: dict[str, Appointment] = {}

    def get_today_schedule(
        self, configured_now: Optional[str] = None
    ) -> dict[str, Appointment]:
        """
        Get the list of today's schedule

        Args:
            configured_now (Optional[str]): Optional now parameter for configuring NOW
               (specific scenarios or test cases). format: 'YYYYMMDDHHMM'
        Returns:
            dict[str, Appointment]: The list of today schedules
        """
        if not configured_now:
            tz = pytz.timezone("America/Vancouver")
            now = datetime.datetime.now(tz).strftime("%Y%m%d%H%M")
        else:
            now = configured_now

        return {
            start_date_time: appointment
            for start_date_time, appointment in self.__schedule.items()
            if start_date_time >= now
        }

    def get_schedule(self, requested_date: str) -> dict[str, Appointment]:
        """
        Get the list of a specific date schedule

        Args:
            requested_date (str): the date to check schedule for in YYYY-MM-DD format
        Returns:
            dict[str, Appointment]: The list of provided date schedule
        """

        tz = pytz.timezone("America/Vancouver")
        req_date = datetime.datetime.strptime(requested_date, "%Y-%m-%d")
        tz.localize(req_date)

        possible_time_slots = AppointmentService.create_all_possible_time_slots(
            requested_date
        )

        return {
            start_date_time: self.__schedule[start_date_time]
            for start_date_time, appointment in possible_time_slots.items()
            if start_date_time in self.__schedule
        }

    def get_available_appointments(
        self,
        start_date: str,
        appointment_type: AppointmentType,
        configured_now: Optional[str] = None,
    ) -> dict[str, None]:
        """
        Get available time slots for a specific date and appointment type

        Args:
            start_date (str): start date to check in YYYY-MM-DD format
            appointment_type (AppointmentType): Type of appointment to check availability for
            configured_now (Optional[str]): Optional now parameter for configuring NOW
                           (specific scenarios or test cases). format: 'YYYYMMDDHHMM'
        Returns:
            dict[str, None]: A list of available time slots to book
        """
        possible_time_slots = AppointmentService.create_all_possible_time_slots(
            start_date, configured_now=configured_now
        )

        return AppointmentService.extract_all_available_time_slots(
            possible_time_slots, appointment_type, self.__schedule
        )

    def add_appointment(
        self, appointment: Appointment, configured_now: Optional[str] = None
    ) -> bool:
        """
        Add a new appointment to practitioner's schedule

        Args:
            appointment (appointment): New appointment to be added
            configured_now (Optional[str]): Optional now parameter for configuring NOW
                           (specific scenarios or test cases). format: 'YYYYMMDDHHMM'
        Raises:
            ValueError: If 'start_date_time' is currently booked
        Returns:
            bool: whether it was successful or not
        """
        tz = pytz.timezone("America/Vancouver")
        start_date_time_instance = datetime.datetime.strptime(
            appointment.start_date_time, "%Y%m%d%H%M"
        )
        start_date_time_instance = tz.localize(start_date_time_instance)

        available_appointments = self.get_available_appointments(
            start_date_time_instance.strftime("%Y-%m-%d"),
            appointment.appointment_type,
            configured_now=configured_now,
        )

        if appointment.start_date_time not in available_appointments:
            raise ValueError("This time slot is not available to book!")

        self.__schedule.update({appointment.start_date_time: appointment})

        return True
