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
        if cls is not None:  # if class is specified
            class_objects = {}  # dictionary to store objects
            for key, value in self.__objects.items():  # iterate
                if key.find(cls.__name__) == 0:  # if class name matches
                    class_objects.update({key: value})  # add to dict
            return class_objects  # return dictionary
        return self.__objects  # return all objects

    def new(self, obj):
        """
        Adds object to storage dictionary (<class name>.id)
        """
        key = obj.__class__.__name__ + "." + obj.id  # create key
        self.__objects[key] = obj  # add object to dictionary

    def save(self):
        """
        Serializes __objects to JSON file

        Attributes:
            obj_dict (dict):  dictionary to store objects
        """
        obj_dict = {}  # dictionary to store objects
        for key, value in self.__objects.items():  # iterate through __objects
            obj_dict[key] = value.to_dict()  # add object to dictionary
        with open(self.__file_path, "w", encoding="utf-8") as file:  # open
            json.dump(obj_dict, file)  # write to file

    def reload(self):
        """
        Deserializes JSON file to __objects

        Attributes:
            obj_dict (dict):  dictionary to store objects
            obj_class (dict): dictionary of classes
        """
        try:
            with open(self.__file_path, "r") as file:  # open file
                obj_dict = json.load(file)  # load file
            classes = {
                "BaseModel": BaseModel,
                "User": User,
                "State": State,
                "City": City,
                "Place": Place,
                "Amenity": Amenity,
                "Review": Review,
            }  # dictionary of classes
            for key, value in obj_dict.items():  # iterate through obj_dict
                class_name = value.get("__class__")  # get class name
                if class_name in classes:
                    self.__objects[key] = classes[class_name](**value)  # creat
        except FileNotFoundError:  # if file not found
            pass  # do nothing

    def delete(self, obj=None):
        """
        Deletes object from __objects

        Attributes:
            key (str):  key for object
        """
        if obj is not None:  # if object exists
            key = self.key_create(obj)  # create key
            del self.__objects[key]  # delete object
        else:  # if object does not exist
            return  # do nothing

    def key_create(self, obj):
        """
        Helper function to create key
        """
        return obj.__class__.__name__ + "." + obj.id
