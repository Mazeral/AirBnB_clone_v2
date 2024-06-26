#!/usr/bin/python3
"""
This module defines a class User that inherits from BaseModel and Base.
"""

from models.base_model import BaseModel
from os import environ
from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

# Get the storage engine type from the environment variable
storage_engine = environ.get("HBNB_TYPE_STORAGE")

# If the storage engine is set to 'db', use SQLAlchemy's declarative base
if storage_engine == "db":
    Base = declarative_base()


class User(BaseModel, Base):
    """
    This class defines a User by various attributes.

    Attributes:
        email (str): The email of the user.
        password (str): The password of the user.
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
    """

    # Define the columns for the User table if the storage engine is 'db'
    if storage_engine == "db":
        __tablename__ = "users"
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
    else:
        # Define the attributes for the User class if
        # the storage engine is not 'db'
        # These attributes are used for in-memory storage
        email = ''
        password = ''
        first_name = ''
        last_name = ''
