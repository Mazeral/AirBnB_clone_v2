#!/usr/bin/python3
"""
State Module for HBNB project
"""
from models.base_model import BaseModel
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()


class State(BaseModel, Base):
    """
    State class

    This class represents a state in the database.
    """
    __tablename__ = "states"

    # Define the columns of the state table
    name = Column(String(128), nullable=False)

    # Define a relationship with the City model
    # This allows us to access the cities of a state
    cities = relationship("City",
                          backref="state",
                          cascade="all, delete",
                          passive_deletes=True)

    if BaseModel.storage_t == "db":
        @property
        def city(self):
            """
            Returns a list of cities belonging to this state.

            This property is only available when the storage type is 'db'.
            """
            city_list = []
            # Iterate over all cities in the storage
            for city in BaseModel.storage.all(City).values():
                # If the city's state_id matches this state's id,
                # add it to the city list
                if city.state_id == self.id:
                    city_list.append(city)
            return city_list
