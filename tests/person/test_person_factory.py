"""
Test Cases for Person Factory
"""

import pytest

from src.clinic.clinic import Clinic
from src.person.person_factory import PersonFactory
from src.person.practitioner import Practitioner


class TestPersonFactory:
    """Test cases for person factory"""

    def test_valid_class_for_person_factory(self, faker_instance):
        """Test passing valid class to person factory"""

        practitioner = PersonFactory.create_person(
            Practitioner, name=faker_instance.name()
        )
        assert isinstance(practitioner, Practitioner)

    def test_invalid_class_for_person_factory(self, faker_instance):
        """Test passing invalid class to person factory"""

        with pytest.raises(ValueError):
            PersonFactory.create_person(Clinic, name=faker_instance.name())
