"""
Factory for Appointment
"""

from src.appointment.appointment import Appointment
from tests.utils.mocks.appointment_mock import AppointmentMock


# pylint: disable=too-few-public-methods
class AppointmentFactory:
    """Factory for instantiating appointments"""

    @staticmethod
    def get_appointment(**kwargs) -> Appointment:
        """
        Instantiate a new Appointment

        Args:
            kwargs: arbitrary arguments:
        Returns:
            Appointment: a new Appointment instance
        """

        appointment_data = AppointmentMock.get_data(**kwargs)

        return Appointment(
            start_date_time=appointment_data["start_date_time"],
            appointment_type=appointment_data["appointment_type"],
            patient=appointment_data["patient"],
        )
