#!/usr/bin/python3
"""
    Contains State class to represent states of cities.
"""

from models.base_model import BaseModel, Base
import models
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from os import environ

storage_engine = environ.get("HBNB_TYPE_STORAGE")


class State(BaseModel, Base):
    """
    State class: class to represent states of cities.

    Attributes:
        name (str): The name of the state.
        cities (list): A list of City instances that belong to the state.
    """
    if (storage_engine == 'db'):
        # Define the table name for the database
        __tablename__ = "states"

        # Define the columns for the state table
        name = Column(String(128), nullable=False)

        # Define the relationship between the state and city tables
        cities = relationship("City", backref="state")
    else:
        # Initialize the name attribute for non-database storage
        name = ""

        @property
        def cities(self):
            """
            Returns a list of City instances that belong to the state.

            Returns:
                result (list): A list of City instances.
            """
            result = []
            # Iterate over all city instances in the storage
            for j, i in models.storage.all(models.city.City).items():
                # Check if the city belongs to the state
                if (i.state_id == self.id):
                    result.append(i)
            return result