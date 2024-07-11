"""
Person Factory for creating person objects
"""

from typing import Type

from src.person.patient import Patient
from src.person.person import Person
from src.person.practitioner import Practitioner


# pylint: disable=too-few-public-methods
class PersonFactory:
    """Person Factory class"""

    @staticmethod
    def create_person(
        person_class: Type[Person] | Type[Practitioner] | Type[Patient], name: str
    ) -> Person | Practitioner | Patient:
        """
        Factory method to create objects of types Person.

        Args:
            person_class (class): The class of the person to instantiate.
            name (str): The name of the person.

        Returns:
            Person: An instance of a Person subclass.
        """

        if issubclass(person_class, Practitioner):
            return Practitioner(name)

        if issubclass(person_class, Patient):
            return Patient(name)

        if issubclass(person_class, Person):
            return Person(name)

        raise ValueError("person_class must be a subclass of Person")
