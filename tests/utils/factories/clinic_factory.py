"""
Factory for Clinic
"""

from src.clinic.clinic import Clinic
from tests.utils.mocks.clinic_mock import ClinicMock


# pylint: disable=too-few-public-methods
class ClinicFactory:
    """Factory for instantiating clinics"""

    @staticmethod
    def get_clinic(**kwargs) -> Clinic:
        """
        Instantiate a new Clinic

        Args:
            kwargs: arbitrary arguments
        Returns:
            Clinic: a new Clinic instance
        """

        clinic_data = ClinicMock.get_data(**kwargs)

        return Clinic(name=clinic_data["name"])
