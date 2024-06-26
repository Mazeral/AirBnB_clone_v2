#!/usr/bin/python3
"""
This module defines a base class for all models in our hbnb clone.
"""

import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime

time = "%Y-%m-%dT%H:%M:%S.%f"

if models.storage_t == "db":
    Base = declarative_base()
else:
    Base = object


class BaseModel:
    """
    A base class for all hbnb models.

    Attributes:
        id (str): Unique identifier for each model instance.
        created_at (datetime): Date and time when the model\
        instance was created.
        updated_at (datetime): Date and time when\
        the model instance was last updated.

    Methods:
        __init__(self, *args, **kwargs)
            Initializes a new model instance.

        __str__(self)
            Returns a string representation of the instance.

        save(self)
            Updates the updated_at attribute with the current\
            date and time when the instance is changed.

        to_dict(self)
            Converts the instance into a dictionary format.

        delete(self)
            Deletes the model instance from the storage.
    """
    def __init__(self, *args, **kwargs):
        """
        Initializes a new model instance.

        If no keyword arguments are provided, generates a new UUID for the id attribute,
        sets the created_at and updated_at attributes to the current date and time.

        If keyword arguments are provided, converts the 'created_at' and 'updated_at'
        attributes to datetime objects and updates the instance attributes with the
        provided keyword arguments.
        """
        if models.storage_t == "db":
            id = Column(String(60),
                   primary_key=True,
                   nullable=False)

            created_at = Column(DateTime,
                   nullable=False,
                   default=datetime.utcnow())

            updated_at = Column(DateTime,
                   nullable=False,
                   default=datetime.utcnow())
            
        else:
            pass
            if not kwargs:
                from models import storage
                self.id = str(uuid.uuid4())
                self.created_at = datetime.now()
                self.updated_at = datetime.now()
            else:
                for key, value in kwargs.items():
                    if key == 'created_at' or key == 'updated_at':
                        value = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f')
                    if key != '__class__':
                        setattr(self, key, value)
                if 'id' not in kwargs:
                    self.id = str(uuid.uuid4())
                if 'created_at' not in kwargs:
                    self.created_at = datetime.utcnow()
                if 'updated_at' not in kwargs:
                    self.updated_at = datetime.utcnow()

    def __str__(self):
        """
        Returns a string representation of the instance.

        Returns:
            str: A string representation of the instance in the format '[class_name] (id) {attributes}'.
        """
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """
        Updates the updated_at attribute with the current date and time when the instance is changed.

        Saves the instance to the storage.
        """
        from models import storage
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """
        Converts the instance into a dictionary format.

        Returns:
            dict: A dictionary representation of the instance.
        """
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({'__class__':
                          (str(type(self)).split('.')[-1]).split('\'')[0]})
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        if '_sa_instance_state' in dictionary:
            del dictionary['_sa_instance_state']
        return dictionary

    id = Column(String(60),
                primary_key=True,
                nullable=False)
    created_at = Column(DateTime,
                        nullable=False,
                        default=datetime.utcnow())
    updated_at = Column(DateTime,
                        nullable=False,
                        default=datetime.utcnow())

    def delete(self):
        """
        Deletes the model instance from the storage.
        """
        from models import storage
        storage.delete(self)
