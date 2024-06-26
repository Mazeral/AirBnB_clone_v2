#!/usr/bin/python3
"""
City module for HBNB project.

This module defines the City class which inherits from the BaseModel class
and the declarative_base class from SQLAlchemy. It represents a city in the
database.
"""

from models.base_model import BaseModel
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey


Base = declarative_base()


class City(BaseModel, Base):
    """
    The City class represents a city in the database.

    Attributes:
        __tablename__ (str): The name of the table in the database.
        name (str): The name of the city.
        state_id (str): The foreign key referencing the state id in the states
                         table.
    """

    # Table name
    __tablename__ = 'cities'

    # Columns
    name = Column(String(128), nullable=False)
    state_id = Column(String(60), ForeignKey('states.id'), nullable=False)