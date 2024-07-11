"""
Appointment Faker Provider
"""

from typing import Optional

from faker.providers import BaseProvider

from src.appointment.appointment import AppointmentService


# pylint: disable=too-few-public-methods
class AppointmentProvider(BaseProvider):
    """Extending Appointment as a provider for faker"""

    @staticmethod
    def appointment_start_date_time(
        year: Optional[int] = None,
        month: Optional[int] = None,
        day: Optional[int] = None,
        hour: Optional[int] = None,
        minute: Optional[int] = None,
    ) -> str:
        """
        This method uses AppointmentService generate_start_date_time method
        to generate a valid start_date_time
        """

        return AppointmentService.generate_start_date_time(
            year, month, day, hour, minute
        )
