"""
Mock generator for Patient
"""

from faker import Faker


# pylint: disable=too-few-public-methods
class PatientMock:
    """Mocking a Patient model"""

    @staticmethod
    def get_data(**kwargs):
        """Get mock data for patient"""

        faker = Faker()

        return {"name": kwargs.get("name", faker.name())}
