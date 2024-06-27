#!/usr/bin/python3
"""
    Module containing BaseModel
"""

import models
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from os import environ
from datetime import datetime
from uuid import uuid4


# Check the environment variable for the storage engine
storage_engine = environ.get("HBNB_TYPE_STORAGE")

# If the storage engine is set to 'db', use SQLAlchemy's declarative base
if (storage_engine == "db"):
    Base = declarative_base()


class BaseModel():
    """
    Base class to define all common attributes and methods for other classes.
    Inherits from SQLAlchemy's declarative base if the storage engine is set to 'db',
    otherwise inherits from the object class.
    """

    # Define the columns for the BaseModel class
    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """
        Initializes a BaseModel instance.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        # If keyword arguments are provided, set the attributes based on the keys
        if kwargs:
            for key in kwargs:
                if key == "__class__":
                    continue
                elif key in ("created_at", "updated_at"):
                    # If the key is 'created_at' or 'updated_at', parse it as a datetime object
                    iso = "%Y-%m-%dT%H:%M:%S.%f"
                    setattr(self, key, datetime.strptime(kwargs[key], iso))
                else:
                    # Otherwise, set the attribute as is
                    setattr(self, key, kwargs[key])
                # Set the id as a UUID
                self.id = str(uuid4())
        else:
            # If no keyword arguments are provided, set the id as a UUID and set the created_at
            # and updated_at fields to the current datetime
            self.id = str(uuid4())
            self.created_at = self.updated_at = datetime.now()

    def __str__(self):
        """
        Return a string representation of a Model.

        Returns:
            str: The class name, id, and dict of attributes.
        """
        return "[{}] ({}) {}".format(self.__class__.__name__,
                                     self.id, self.__dict__)

    def save(self):
        """
        Update the latest updation time of a model.
        """
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """
        Return a custom representation of a model.

        Returns:
            dict: A dictionary containing the class name, id, and attributes.
        """
        custom = self.__dict__.copy()
        custom_dict = {}
        custom_dict.update({"__class__": self.__class__.__name__})
        for key in list(custom):
            if key in ("created_at", "updated_at"):
                # If the key is 'created_at' or 'updated_at', format it as a string
                custom_dict.update({key: getattr(self, key).isoformat()})
            elif key == "_sa_instance_state":
                # Remove the SQLAlchemy instance state attribute
                custom.pop(key)
            else:
                # Otherwise, include the attribute in the dictionary
                custom_dict.update({key: getattr(self, key)})
        return custom_dict

    def delete(self):
        """
        Delete the current instance from the storage.
        """
        k = "{}.{}".format(type(self).__name__, self.id)
        del models.storage.__objects[k]
