"""
Test Cases for Clinic Model
"""

from tests.utils.factories.clinic_factory import ClinicFactory
from tests.utils.factories.person_factory import PersonFactory


class TestClinic:
    """Test cases for clinic model"""

    def test_id_property_getter(self):
        """Test getting the ID of the clinic"""

        my_clinic = ClinicFactory.get_clinic()
        assert my_clinic.id is not None and isinstance(my_clinic.id, str)

    def test_name_property_getter(self, faker_instance):
        """Test name property getter"""

        name = faker_instance.company()
        my_clinic = ClinicFactory.get_clinic(name=name)
        assert name == my_clinic.name

    def test_name_property_setter(self, faker_instance):
        """Test name property setter"""

        name = faker_instance.company()
        my_clinic = ClinicFactory.get_clinic()
        my_clinic.name = name
        assert name == my_clinic.name

    def test_add_practitioner(self):
        """Test adding a new practitioner to the clinic"""

        new_person = PersonFactory.get_person()
        my_clinic = ClinicFactory.get_clinic()
        my_clinic.add_practitioner(new_person)
        assert my_clinic.has_practitioner(new_person.id)

        # check for duplicate add
        my_clinic.add_practitioner(new_person)
        assert my_clinic.has_practitioner(new_person.id)

    def test_add_practitioner_multiple_people(self):
        """Test adding several practitioner to the clinic"""

        for _ in range(3):
            new_person = PersonFactory.get_person()
            my_clinic = ClinicFactory.get_clinic()
            my_clinic.add_practitioner(new_person)
            assert my_clinic.has_practitioner(new_person.id)
