"""
Factory for Person, Practitioner and Patient
"""

from typing import cast

from src.person.patient import Patient
from src.person.person import Person
from src.person.person_factory import PersonFactory as PersonFactoryCreator
from src.person.practitioner import Practitioner
from tests.utils.mocks.patient_mock import PatientMock
from tests.utils.mocks.person_mock import PersonMock
from tests.utils.mocks.practitioner_mock import PractitionerMock


class PersonFactory:
    """Factory for instantiating persons, practitioner and patients"""

    @staticmethod
    def get_person(**kwargs) -> Person:
        """
        Instantiate a new Person

        Args:
            kwargs: arbitrary arguments
        Returns:
            Person: a new Person instance
        """

        person_data = PersonMock.get_data(**kwargs)
        return PersonFactoryCreator.create_person(Person, name=person_data["name"])

    @staticmethod
    def get_practitioner(**kwargs) -> Practitioner:
        """
        Instantiate a new Practitioner

        Args:
            kwargs: arbitrary arguments
        Returns:
            Practitioner: a new Practitioner instance
        """

        practitioner_data = PractitionerMock.get_data(**kwargs)

        return cast(
            Practitioner,
            PersonFactoryCreator.create_person(
                Practitioner, name=practitioner_data["name"]
            ),
        )

    @staticmethod
    def get_patient(**kwargs) -> Patient:
        """
        Instantiate a new Patient

        Args:
            kwargs: arbitrary arguments
        Returns:
            Patient: a new Patient instance
        """

        patient_data = PatientMock.get_data(**kwargs)

        return cast(
            Patient,
            PersonFactoryCreator.create_person(Patient, name=patient_data["name"]),
        )
