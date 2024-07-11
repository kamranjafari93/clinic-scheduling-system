"""
Mock generator for Clinic
"""

from faker import Faker


# pylint: disable=too-few-public-methods
class ClinicMock:
    """Mocking a Clinic model"""

    @staticmethod
    def get_data(**kwargs):
        """Get mock data for clinic"""

        faker = Faker()

        return {"name": kwargs.get("name", faker.company())}
