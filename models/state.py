#!/usr/bin/python3
"""
This module defines the State class which represents a state in the HBNB project.
"""

import models
from models.base_model import BaseModel, Base
from models.city import City
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """
    Representation of a state in the HBNB project.

    Attributes:
        name (str): The name of the state.
        cities (list): A list of City instances that belong to the state.
    """

    # Table name if storage type is db
    if models.storage_t == "db":
        __tablename__ = 'states'
        name = Column(String(128), nullable=False)
        cities = relationship("City", backref="state")
    # If storage type is not db, initialize name as an empty string
    else:
        name = ""

    def __init__(self, *args, **kwargs):
        """
        Initializes a State instance.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(*args, **kwargs)

    @property
    def cities(self):
        """
        Getter for a list of City instances related to the state.

        Returns:
            list: A list of City instances.
        """
        city_list = []
        all_cities = models.storage.all(City)
        for city in all_cities.values():
            if city.state_id == self.id:
                city_list.append(city)
        return city_list