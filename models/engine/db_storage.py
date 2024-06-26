#!/usr/bin/python3
"""
This module defines a class to manage the data of a MySQL database.
"""

from models.base_model import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from os import getenv


class DBStorage:
    """
    This class manages the data of a MySQL database.
    """

    __engine = None
    __session = None

    def __init__(self):
        """
        Initializes the database connection and session.
        """
        # Get environment variables
        HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')
        HBNB_ENV = getenv('HBNB_ENV')

        # Create database engine
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(HBNB_MYSQL_USER,
                                             HBNB_MYSQL_PWD,
                                             HBNB_MYSQL_HOST,
                                             HBNB_MYSQL_DB))

        # Drop all tables if in test environment
        if HBNB_ENV == "test":
            Base.metadata.drop_all(self.__engine)

        # Create session factory and session
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session()

    def all(self, cls=None):
        """
        Query on the current database session.

        :param cls: The class to query on. If None, query all classes.
        :type cls: class
        :return: A dictionary of all objects in storage matching\
        the given class name.
        :rtype: dict
        """
        new_dict = {}

        # Query all classes if cls is None
        if cls is None:
            for clss in Base.classes.values():
                objs = self.__session.query(clss).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        else:
            # Query specified class
            objs = self.__session.query(cls).all()
            for obj in objs:
                key = obj.__class__.__name__ + '.' + obj.id
                new_dict[key] = obj

        return new_dict

    def new(self, obj):
        """
        Add the object to the current database session.

        :param obj: The object to add.
        :type obj: object
        """
        self.__session.add(obj)

    def save(self):
        """
        Commit all changes of the current database session.
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        Delete from the current database session obj if not None.

        :param obj: The object to delete. If None, do nothing.
        :type obj: object
        """
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """
        Reloads data from the database.
        """
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session()

    def close(self):
        """
        Call remove() method on the private session attribute.
        """
        self.__session.remove()

    def get(self, cls, id):
        """
        Returns the object based on the class and its ID, or None if not found.

        :param cls: The class to query on.
        :type cls: class
        :param id: The ID of the object.
        :type id: int
        :return: The object or None if not found.
        :rtype: object or None
        """
        if cls is None or id is None:
            return None

        for obj in self.all(cls):
            if obj.id == id:
                return obj
        return None

    def count(self, cls=None):
        """
        Returns the number of objects in storage matching the given class name.

        :param cls: The class to query on. If None, query all classes.
        :type cls: class
        :return: The number of objects in storage\
        matching the given class name.
        :rtype: int
        """
        if cls is None:
            return len(self.all())
        else:
            return len(self.all(cls))
