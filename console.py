#!/usr/bin/python3
""" Console Module """
import cmd
import sys
import shlex
import json
import models
from models.base_model import BaseModel
from models.__init__ import storage
from datetime import datetime
from models import storage
from shlex import split
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from models.engine.file_storage import FileStorage
from models.engine.db_storage import DBStorage

classes = {
    "BaseModel": BaseModel,
    "User": User,
    "Place": Place,
    "State": State,
    "City": City,
    "Amenity": Amenity,
    "Review": Review
    }


class HBNBCommand(cmd.Cmd):
    """
    Contains functionality for the HBNB console

    Attributes:
        prompt (str):       prompt for console
        dot_cmds (list):    list of commands that require dot notation
        types (dict):       dictionary of types for casting
    """
    # determines prompt for interactive/non-interactive modes
    prompt = '(hbnb) ' if sys.__stdin__.isatty() else ''

    dot_cmds = ['all', 'count', 'show', 'destroy', 'update']
    types = {
             'number_rooms': int,
             'number_bathrooms': int,
             'max_guest': int,
             'price_by_night': int,
             'latitude': float,
             'longitude': float
            }

    def parse_pairs(self, args):
        """
        Parses key-value pairs

        Args:
            args (str):         string to parse

        Returns:
            parsed_dict (dict): dictionary of key-value pairs
        """
        parsed_dict = {}  # dictionary to store key-value pairs
        for pair in args:  # iterate through pairs
            if "=" in pair:  # if the pair is key-value
                key, value = pair.split("=", 1)  # split them
                parsed_dict[key] = value.strip('"')  # add to dictionary
        return parsed_dict  # return completed dictionary

    def do_quit(self, command):
        """
        Exits the HBNB console
        """
        return True

    def do_EOF(self, arg):
        """
        Handles EOF to exit program without formatting
        """
        print()
        return True

    def do_create(self, args):
        """
        Creates an object that inherits from BaseModel
        """
        split_args = shlex.split(args)
        if len(split_args) == 0:
            print("** class name missing **")
            return
        class_name = split_args[0]
        if class_name not in classes:
            print("** class doesn't exist **")
            return

        new_obj = classes[class_name]()  # create new object
        parsed_pairs = self.parse_pairs(split_args[1:])  # helper function

        for key, value in parsed_pairs.items():  # iterate through pairs
            if hasattr(new_obj, key):  # if key is an attribute
                if key in ["name", "description"]:
                    value = value.replace('_', ' ')
                setattr(new_obj, key, value)  # set attribute to value

        new_obj.save()
        print(new_obj.id)  # print id of new object

    def do_show(self, args):
        """
        Shows an individual object
        """
        split_args = args.split()
        if len(split_args) == 0:
            print("** class name missing **")
            return
        if split_args[0] not in classes:
            print("** class doesn't exist **")
            return
        if len(split_args) == 1:
            print("** instance id missing **")
            return
        key = split_args[0] + "." + split_args[1]
        objects = storage.all()
        if key in objects:
            obj = objects[key]  # convert object to string
            print(obj)  # print entire object
        else:
            print("** no instance found **")

    def do_destroy(self, args):
        """
        Destroys a specified object
        """
        split_args = args.split()
        if len(split_args) == 0:
            print("** class name missing **")
            return
        if split_args[0] not in classes:
            print("** class doesn't exist **")
            return
        if len(split_args) == 1:
            print("** instance id missing **")
            return
        key = split_args[0] + "." + split_args[1]
        objects = storage.all()
        if key in objects:
            del objects[key]
            storage.save()
        else:
            print("** no instance found **")

    def do_all(self, args):
        """
        Shows all objects, or all objects of a class
        """
        if args:
            if args not in classes:
                print("** class doesn't exist **")
                return
            objects = storage.all(classes[args])
        else:
            objects = storage.all()

        print([str(obj) for obj in objects.values()])

    def do_count(self, args):
        """
        Counts current number of class instances
        """
        if not args:
            print("** class name missing **")
            return
        if args not in storage.classes:
            print("** class doesn't exist **")
            return
        
        count = len(storage.all(args))
        print(count)

    def do_update(self, args):
        """
        Updates an instance based on the class name and id
        """
        split_args = shlex.split(args)
        if len(split_args) == 0:
            print("** class name missing **")
            return
        if split_args[0] not in classes:
            print("** class doesn't exist **")
            return
        if len(split_args) == 1:
            print("** instance id missing **")
            return
        key = split_args[0] + "." + split_args[1]
        objects = storage.all()
        if key not in objects:
            print("** no instance found **")
            return
        if len(split_args) == 2:
            print("** attribute name missing **")
            return
        if len(split_args) == 3:
            print("** value missing **")
            return

        obj = objects[key]
        attr_name = split_args[2]
        attr_value = split_args[3]

        if attr_name in self.types:
            attr_value = self.types[attr_name](attr_value)

        setattr(obj, attr_name, attr_value)
        obj.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
