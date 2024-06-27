#!/usr/bin/python3
"""
Module containing FileStorage class used for file storage
"""
import json
import models


class FileStorage:
    """
    FileStorage class is used to serialize and deserialize instances
    to and from a JSON file.

    Attributes:
        __file_path (str): The path to the JSON file.
        __objects (dict): A dictionary that stores the serialized objects.
    """

    # Initialize the path to the JSON file and the objects dictionary
    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """
        Returns a dictionary containing every object in storage.

        Args:
            cls (class, optional): If specified, returns a dictionary
            containing only objects of the given class.

        Returns:
            dict: A dictionary containing the objects.
        """
        if not cls:
            return self.__objects

        result = {}
        for key in self.__objects.keys():
            if key.split(".")[0] == cls.__name__:
                result.update({key: self.__objects[key]})
        return result

    def new(self, obj):
        """
        Creates a new object and saves it to the storage.

        Args:
            obj (object): The object to be saved.
        """
        key = "{}.{}".format(type(obj).__name__, obj.id)
        self.__objects[key] = obj

    def save(self):
        """
        Updates the JSON file to reflect any changes in the objects.
        """
        temp = {}
        for id, obj in self.__objects.items():
            temp[id] = obj.to_dict()
        with open(self.__file_path, "w") as json_file:
            json.dump(temp, json_file)

    def reload(self):
        """
        Updates the objects dictionary to restore previously created objects.
        """
        try:
            with open(self.__file_path, "r") as json_file:
                temp = json.load(json_file)
            for id, dict in temp.items():
                temp_instance = models.dummy_classes[dict["__class__"]](**dict)
                self.__objects[id] = temp_instance
        except:
            pass

    def close(self):
        """
        Displays the HBNB data by reloading the objects from the storage.
        """
        self.reload()

    def delete(self, obj=None):
        """
        Deletes an object from the storage if it exists.

        Args:
            obj (object, optional): The object to be deleted. If not specified,
            the method does nothing.
        """
        if obj:
            self.__objects.pop("{}.{}".format(type(obj).__name__, obj.id))