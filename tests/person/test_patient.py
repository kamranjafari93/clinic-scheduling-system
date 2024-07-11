"""
Test Cases for Patient Model
"""

from tests.utils.factories.person_factory import PersonFactory


class TestPatient:
    """Test cases for patient model"""

    def test_id_property_getter(self):
        """Test getting the ID of the patient"""

        patient = PersonFactory.get_patient()
        assert patient.id is not None and isinstance(patient.id, str)

    def test_name_property_setter_getter(self, faker_instance):
        """Test name property getter and setter"""

        name = faker_instance.name()
        patient = PersonFactory.get_patient(name=name)
        assert name == patient.name
