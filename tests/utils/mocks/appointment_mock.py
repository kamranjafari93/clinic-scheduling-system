"""
Mock generator for Appointment
"""

from src.appointment.appointment import AppointmentService
from tests.utils.factories.person_factory import PersonFactory
from tests.utils.faker_providers.appointment_type_provider import (
    AppointmentTypeProvider,
)


# pylint: disable=too-few-public-methods
class AppointmentMock:
    """Mocking an Appointment model"""

    @staticmethod
    def get_data(**kwargs):
        """Get mock data for appointment"""

        return {
            "start_date_time": kwargs.get(
                "start_date_time", AppointmentService.generate_start_date_time()
            ),
            "appointment_type": kwargs.get(
                "appointment_type", AppointmentTypeProvider.appointment_type()
            ),
            "patient": kwargs.get("patient", PersonFactory.get_patient()),
        }
