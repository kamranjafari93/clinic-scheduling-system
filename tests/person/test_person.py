"""
Test Cases for Person Model
"""

from tests.utils.factories.person_factory import PersonFactory


class TestPerson:
    """Test cases for person model"""

    def test_id_property_getter(self):
        """Test getting the ID of the person"""

        person = PersonFactory.get_person()
        assert person.id is not None and isinstance(person.id, str)

    def test_name_property_getter(self, faker_instance):
        """Test name property getter"""

        name = faker_instance.name()
        person = PersonFactory.get_person(name=name)
        assert name == person.name

    def test_name_property_setter(self, faker_instance):
        """Test name property setter"""

        name = faker_instance.name()
        person = PersonFactory.get_person()
        person.name = name
        assert name == person.name
