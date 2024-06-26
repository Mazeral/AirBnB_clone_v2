#!/usr/bin/python3
"""
This module defines a base class for all models in our hbnb clone.
"""

import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime

Base = declarative_base()

class BaseModel(Base):
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
        if not kwargs:
            from models import storage
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
        else:
            kwargs['updated_at'] = datetime.strptime(kwargs['updated_at'],
                                                     '%Y-%m-%dT%H:%M:%S.%f')
            kwargs['created_at'] = datetime.strptime(kwargs['created_at'],
                                                     '%Y-%m-%dT%H:%M:%S.%f')
            del kwargs['__class__']
            self.__dict__.update(kwargs)
            for key, item in kwargs.items():
                if key not in ['created_at', 'updated_at']:
                    setattr(self, key, item)

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
        if '_sa_instance_state' in dictionary.keys():
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
