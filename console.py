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

    def do_exit(self, command):
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

    def do_show(self, args):
        """
        Shows an individual object
        """
        split_args = args.split()
        if len(split_args) == 0:
            print("** class name missing **")
            return
        if len(split_args) == 1:
            print("** instance id missing **")
            return
        cls_name, obj_id = split_args[0], split_args[1]

        if cls_name not in classes:
            print("** class doesn't exist **")
            return

        obj_dict = storage.all(cls_name)
        key = f"{cls_name}.{obj_id}"

        if key not in obj_dict:
            print("** no instance found **")
        else:
            print(obj_dict[key])

    def do_destroy(self, args):
        """
        Destroys a specified object
        """
        split_args = args.split()
        if len(split_args) == 0:
            print("** class name missing **")
            return
        if len(split_args) == 1:
            print("** instance id missing **")
            return

        cls_name, obj_id = split_args[0], split_args[1]
        if cls_name not in classes:
            print("** class doesn't exist **")
            return

        obj_dict = storage.all(classes[cls_name])
        key = f"{cls_name}.{obj_id}"

        if key not in obj_dict:
            print("** no instance found **")
        else:
            storage.delete(obj_dict[key])
            storage.save()
            print(f"{obj_id} deleted")
            return

    def do_resetdb(self, args):  # for de-cluttering database while testing
        """
        Destroys all models in the database, completely emptying it.
        This cannot be undone.
        """
        if input("Are you sure you want to delete everything in the database?\
                  This cannot be undone. [y/N]: ").lower() == "y":
            size = len(storage.all())
            for model in list(storage.all().values()):
                model.delete()
            print(f"Database reset. {size} models have been deleted.")

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

        cls = classes.get(args)
        if cls is None:
            print("** class doesn't exist **")
            return

        count = len(storage.all(cls))
        print(count)

    def do_size(self, args):
        """
        Displays the size of the database, or the number of objects saved.
        """
        print(len(storage.all()))

    def do_update(self, args):
        """
        Updates an instance based on the class name and id
        """
        split_args = shlex.split(args)
        if len(split_args) == 0:
            print("** class name missing **")
            return
        if len(split_args) == 1:
            print("** instance id missing **")
            return
        if len(split_args) == 2:
            print("** attribute name missing **")
            return
        if len(split_args) == 3:
            print("** value missing **")
            return

        cls_name = split_args[0]
        obj_id = split_args[1]
        attr_name = split_args[2]
        attr_value = split_args[3]

        if cls_name not in classes:
            print("** class doesn't exist **")
            return

        obj_dict = storage.all(cls_name)
        key = f"{cls_name}.{obj_id}"

        if key not in obj_dict:
            print("** no instance found **")
            return
        else:
            obj = obj_dict[key]
            setattr(obj, attr_name, attr_value)
            storage.save()
            print("** instance updated **")


if __name__ == "__main__":
    HBNBCommand().cmdloop()
