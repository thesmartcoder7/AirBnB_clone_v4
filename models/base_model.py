#!/usr/bin/python3
"""
Module that contains the BaseModel class.
"""

from datetime import datetime
import models
from os import getenv
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import uuid

time_format = "%Y-%m-%dT%H:%M:%S.%f"

if models.storage_t == "db":
    Base = declarative_base()
else:
    Base = object


class BaseModel:
    """
    The BaseModel class from which future classes will be derived.

    Attributes (if used with a database):
        id (str): The unique identifier for the model instance.
        created_at (datetime): The datetime when the instance was created.
        updated_at (datetime): The datetime when the instance was last updated.

    Methods:
        __init__: Initializes a new BaseModel instance.
        __str__: Returns a string representation of the BaseModel instance.
        save: Updates the 'updated_at' attribute with the current datetime.
        to_dict: Converts the BaseModel instance to a dictionary.
        delete: Deletes the current instance from storage (if applicable).
    """

    if models.storage_t == "db":
        id = Column(String(60), primary_key=True)
        created_at = Column(DateTime, default=datetime.utcnow)
        updated_at = Column(DateTime, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """
        Initializes a new BaseModel instance.

        Args:
            *args: Positional arguments.
            **kwargs: Keyword arguments.
        """
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)
            if kwargs.get("created_at", None) and isinstance(
                    self.created_at, str):
                self.created_at = datetime.strptime(
                        kwargs["created_at"], time_format
                    )
            else:
                self.created_at = datetime.utcnow()
            if kwargs.get("updated_at", None) and isinstance(
                    self.updated_at, str):
                self.updated_at = datetime.strptime(
                        kwargs["updated_at"], time_format
                    )
            else:
                self.updated_at = datetime.utcnow()
            if kwargs.get("id", None) is None:
                self.id = str(uuid.uuid4())
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = self.created_at

    def __str__(self):
        """
        Returns a string representation of the BaseModel instance.
        """
        dictionary = self.__dict__.copy()
        if models.storage_t != 'db':
            dictionary.pop("_sa_instance_state", None)
        return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id,
                                         dictionary)

    def save(self):
        """
        Updates the 'updated_at' attribute with the current datetime
        and saves the instance to storage.
        """
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """
        Converts the BaseModel instance to a dictionary.

        Returns:
            dict: A dictionary representation of the BaseModel instance.
        """
        new_dict = self.__dict__.copy()
        if "created_at" in new_dict:
            new_dict["created_at"] = new_dict["created_at"].strftime(
                time_format)
        if "updated_at" in new_dict:
            new_dict["updated_at"] = new_dict["updated_at"].strftime(
                time_format)
        new_dict["__class__"] = self.__class__.__name__
        new_dict.pop("_sa_instance_state", None)

        return new_dict

    def delete(self):
        """
        Deletes the current instance from storage (if applicable).
        """
        models.storage.delete(self)
