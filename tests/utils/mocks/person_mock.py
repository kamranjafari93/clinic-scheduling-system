"""
Mock generator for Person
"""

from faker import Faker


# pylint: disable=too-few-public-methods
class PersonMock:
    """Mocking a Person model"""

    @staticmethod
    def get_data(**kwargs):
        """Get mock data for person"""

        faker = Faker()
        return {"name": kwargs.get("name", faker.name())}
