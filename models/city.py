#!/usr/bin/python
"""
This module holds the City class.
City represents a city in the HBNB project.
"""

import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class City(BaseModel, Base):
    """
    Representation of city.

    Attributes:
        state_id (str): The id of the state the city belongs to.
        name (str): The name of the city.
        places (list): A list of Place instances that belong to the city.
    """
    if models.storage_t == "db":
        # Table name for the database
        __tablename__ = 'cities'

        # Columns for the table
        state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
        name = Column(String(128), nullable=False)

        # Relationship with Place class
        places = relationship("Place", backref="cities")
    else:
        # Default values for attributes if not using a database
        state_id = ""
        name = ""

    def __init__(self, *args, **kwargs):
        """
        Initializes a City instance.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(*args, **kwargs)
