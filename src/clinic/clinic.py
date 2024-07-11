"""
Clinic Model
"""

import uuid

from src.person.person import Person


class Clinic:
    """
    Represents a clinic.

    Attributes:
        __id (str): The unique id of the clinic.
        __name (str): The name of the clinic.
        __practitioners (dict): a dictionary of practitioners
    """

    def __init__(self, name: str) -> None:
        """
        Initialize a new clinic.

        Args:
            name (str): The name of the clinic.
        """
        self.__id = f"clinic-{str(uuid.uuid4())}"
        self.__name = name
        self.__practitioners: dict[str, Person] = {}

    @property
    def id(self) -> str:
        """
        Get the id of the clinic.

        Returns:
            str: The id of the clinic.
        """
        return self.__id

    @property
    def name(self) -> str:
        """
        Get the name of the clinic.

        Returns:
            str: The name of the clinic.
        """
        return self.__name

    @name.setter
    def name(self, name: str) -> None:
        """
        Set the name of the clinic.

        Args:
            name (str): The new name of the clinic.
        """
        self.__name = name

    def add_practitioner(self, practitioner: Person) -> None:
        """
        Add a new practitioner to the clinic practitioners

        Args:
            practitioner (Person): the new practitioner to add
        """
        if practitioner.id not in self.__practitioners:
            self.__practitioners.update({practitioner.id: practitioner})

    def has_practitioner(self, practitioner_id: str) -> bool:
        """
        Check if a practitioner is among clinic practitioners

        Args:
            practitioner_id (str): ID of the practitioner to check
        """
        return practitioner_id in self.__practitioners
