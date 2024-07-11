"""
Mock generator for Practitioner
"""

from faker import Faker


# pylint: disable=too-few-public-methods
class PractitionerMock:
    """Mocking a Practitioner model"""

    @staticmethod
    def get_data(**kwargs):
        """Get mock data for practitioner"""

        faker = Faker()

        return {"name": kwargs.get("name", faker.name())}
