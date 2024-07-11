"""
Appointment Types Enum
"""

from enum import Enum


class AppointmentType(Enum):
    """
    Enum representing different types of appointments based on duration.

    Attributes:
        INITIAL_CONSULTATION (str): 90 minutes initial consultation
        STANDARD (str): 60 minutes standard appointment
        CHECK_INS (str): A brief 30 minutes check-in appointment
    """

    INITIAL_CONSULTATION = "90 minutes"
    STANDARD = "60 minutes"
    CHECK_INS = "30 minutes"
