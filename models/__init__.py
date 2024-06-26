#!/usr/bin/python3
"""
    This module initializes the storage system and defines dummy classes
    for further use.
"""

from models.engine.file_storage import FileStorage
from models.engine.db_storage import DBStorage
from os import environ

# Get the storage engine type from the environment variable
storage_engine = environ.get("HBNB_TYPE_STORAGE")

# Instantiate the storage system based on the storage engine type
if storage_engine == "db":
    # If the storage engine is set to 'db', use the DBStorage class
    storage = DBStorage()
    storage.reload()
else:
    # Otherwise, use the FileStorage class
    storage = FileStorage()
    storage.reload()

# The storage variable is used to interact with the selected storage system

# The FileStorage class is used to manage storage in JSON format
# The DBStorage class is used to manage storage in a MySQL database