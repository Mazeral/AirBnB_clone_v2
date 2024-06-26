#!/usr/bin/python3
"""
This module instantiates an object of class FileStorage or DBStorage
depending on the value of the environment variable HBNB_ENV.
"""

# Import necessary modules
from os import environ as env

# Check the value of the environment variable HBNB_ENV
if env.get('HBNB_ENV') == "db":
    # If the environment variable is set to "db", instantiate DBStorage
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    # If the environment variable is not set to "db", instantiate FileStorage
    # and reload the storage dictionary from the file
    from models.engine.file_storage import FileStorage
    storage = FileStorage()
    storage.reload()