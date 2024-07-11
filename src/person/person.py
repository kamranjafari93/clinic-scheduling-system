"""
Person Model
"""

import uuid
from abc import ABC


class Person(ABC):
    """
    Represents a person.

    Attributes:
        __id (str): The unique id of the person.
        _name (str): The name of the person.
    """

    def __init__(self, name: str) -> None:
        """
        Initialize a new person.

        Args:
            name (str): The name of the person.
        """
        self.__id = f"person-{str(uuid.uuid4())}"
        self._name = name

    @property
    def id(self) -> str:
        """
        Get the id of the person.

        Returns:
            str: The id of the person.
        """
        return self.__id

    @property
    def name(self) -> str:
        """
        Get the name of the person.

        Returns:
            str: The name of the person.
        """
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        """
        Set the name of the person.

        Args:
            name (str): The new name of the person.
        """
        self._name = name
