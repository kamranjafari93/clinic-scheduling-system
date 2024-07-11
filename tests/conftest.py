"""
Global conftest file for storing fixtures
"""

import pytest
from faker import Faker

from tests.utils.faker_providers.appointment_provider import AppointmentProvider
from tests.utils.faker_providers.appointment_type_provider import (
    AppointmentTypeProvider,
)


@pytest.fixture(scope="session")
def faker_instance():
    """A faker instance with pre-configured settings"""
    app_faker = Faker()
    app_faker.seed_instance(12345)
    app_faker.add_provider(AppointmentProvider)
    app_faker.add_provider(AppointmentTypeProvider)
    yield app_faker
