"""
Test Cases for Appointment Model
"""

from tests.utils.factories.appointment_factory import AppointmentFactory
from tests.utils.factories.person_factory import PersonFactory


class TestAppointment:
    """Test cases for appointment model"""

    def test_id_property_getter(self):
        """Test getting the ID of the appointment"""

        appointment = AppointmentFactory.get_appointment()
        assert appointment.id is not None and isinstance(appointment.id, str)

    def test_patient_getter_property(self, faker_instance):
        """Test patient of the appointment"""

        name = faker_instance.name()
        patient = PersonFactory.get_practitioner(name=name)

        appointment = AppointmentFactory.get_appointment(patient=patient)
        assert appointment.patient.name == name
