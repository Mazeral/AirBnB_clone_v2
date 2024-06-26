#!/usr/bin/python3
"""
This module initializes the models package based on the value of the
environment variable HBNB_TYPE_STORAGE.
"""

from os import getenv


# Get the value of the environment variable HBNB_TYPE_STORAGE
storage_t = getenv("HBNB_TYPE_STORAGE")

# Initialize the storage object based on the value of the environment variable
if storage_t == "db":
    # If the environment variable is set to "db", instantiate DBStorage
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    # If the environment variable is not set to "db", instantiate FileStorage
    # and reload the storage dictionary from the file
    from models.engine.file_storage import FileStorage
    storage = FileStorage()
    storage.reload()

# Reload the storage dictionary from the file
# NOTE: This is only executed when the environment variable HBNB_TYPE_STORAGE
# is not set to "db"