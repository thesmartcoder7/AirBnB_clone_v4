#!/usr/bin/python3
"""Module that defines the User class."""

import hashlib
from os import getenv
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
import models

# Constants for configuration
STORAGE_TYPE = getenv("HBNB_TYPE_STORAGE", "fs")


class User(BaseModel, Base):
    """
    User class represents users in the application.

    This class defines the User model, including properties and methods for
    working with user data.

    Attributes:
        __tablename__ (str): The name of the database table for User objects.
        email (str): The email address associated with the user.
        _password (str): The hashed password of the user.
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        places (Relationship): A relationship to the Place model.
        reviews (Relationship): A relationship to the Review model.
    """

    if STORAGE_TYPE == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        _password = Column("password", String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user",
                              cascade="all, delete-orphan")
        reviews = relationship("Review", backref="user",
                               cascade="all, delete-orphan")
    else:
        email = ""
        _password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        """
        Initialize a new User instance.

        Args:
            *args: Positional arguments.
            **kwargs: Keyword arguments.
        """
        super().__init__(*args, **kwargs)

    @property
    def password(self):
        """
        The password property.

        Returns:
            str: The hashed password of the user.
        """
        return self._password

    @password.setter
    def password(self, value):
        """
        Set the user's password.

        Args:
            value (str): The plaintext password to be hashed.
        """
        self._password = hashlib.md5(value.encode('utf8')).hexdigest()

    def to_dict(self):
        """
        Convert the User instance to a dictionary.

        Returns:
            dict: A dictionary representation of the User instance.
        """
        new_dict = super().to_dict()
        if STORAGE_TYPE == "db":
            new_dict.pop("password", None)
        return new_dict
