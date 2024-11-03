#!/usr/bin/python3
"""
This module contains the FileStorage class.
"""
import models
import json
import importlib
from datetime import datetime
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review

classes = {
    "BaseModel": BaseModel,
    "User": User,
    "State": State,
    "City": City,
    "Place": Place,
    "Amenity": Amenity,
    "Review": Review,
}


class FileStorage:
    """
    Serializes/deserializes objects to/from JSON file

    Attributes:
        __file_path (str):      path to JSON file
        __objects (dict):       dictionary to store objects

    Methods:
        all(self, cls=None):    returns list of objects
        new(self, obj):         adds object to storage dictionary
        save(self):             serializes __objects to JSON file
        reload(self):           deserializes JSON file to __objects
        delete(self, obj=None): deletes object from storage
        key_create(self, obj):  creates key
    """
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """
        Returns list of objects
        """
        if cls is not None:
            if isinstance(cls, str):
                if cls in classes:
                    cls = classes[cls]
            class_objects = {}
            for key, value in self.__objects.items():
                if key.find(cls.__name__) == 0:
                    class_objects.update({key: value})
            return class_objects
        return self.__objects

    def new(self, obj):
        """
        Adds object to storage dictionary (<class name>.id)
        """
        key = obj.__class__.__name__ + "." + obj.id
        self.__objects[key] = obj

    def save(self):
        """
        Serializes __objects to JSON file

        Attributes:
            obj_dict (dict):  dictionary to store objects
        """
        obj_dict = {}
        for key, value in self.__objects.items():
            obj_dict[key] = value.to_dict()
        with open(self.__file_path, "w", encoding="utf-8") as file:
            json.dump(obj_dict, file)

    def reload(self):
        """
        Deserializes JSON file to __objects

        Attributes:
            obj_dict (dict):  dictionary to store objects
            obj_class (dict): dictionary of classes
        """
        try:
            with open(self.__file_path, "r") as file:
                obj_dict = json.load(file)
            classes = {
                "BaseModel": BaseModel,
                "User": User,
                "State": State,
                "City": City,
                "Place": Place,
                "Amenity": Amenity,
                "Review": Review,
            }
            for key, value in obj_dict.items():
                class_name = value.pop("__class__", None)
                if class_name in classes:
                    if "created_at" in value:
                        value["created_at"] = datetime.strptime(
                            value["created_at"], "%Y-%m-%dT%H:%M:%S.%f")
                    if "updated_at" in value:
                        value["updated_at"] = datetime.strptime(
                            value["updated_at"], "%Y-%m-%dT%H:%M:%S.%f")
                    self.__objects[key] = classes[class_name](**value)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """
        Deletes object from __objects

        Attributes:
            key (str):  key for object
        """
        if obj is not None:
            key = self.key_create(obj)
            del self.__objects[key]
        else:
            return

    def close(self):
        """
        Calls reload method for deserialization
        """
        self.reload()

    def key_create(self, obj):
        """
        Helper function to create key
        """
        return obj.__class__.__name__ + "." + obj.id
