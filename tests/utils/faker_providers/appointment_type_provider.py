"""
Appointment Types Faker Provider
"""

import random

from faker.providers import BaseProvider

from src.appointment.appointment_types import AppointmentType


# pylint: disable=too-few-public-methods
class AppointmentTypeProvider(BaseProvider):
    """Extending AppointmentType as a provider for faker"""

    @staticmethod
    def appointment_type():
        """Randomly choosing an appointment type"""
        return random.choice(list(AppointmentType)).value
