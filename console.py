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

    def preloop(self):
        """
        Prints if isatty is false
        """
        if not sys.__stdin__.isatty():
            print('(hbnb)')

    def precmd(self, line):
        """
        Reformats command line for advanced command syntax
        
        Usage: <class name>.<command>([<id> [<*args> or <**kwargs>]])
        (Brackets denote optional fields in usage example.)
        """
        _cmd = _cls = _id = _args = ''  # initialize line elements

        # scan for general formating - i.e '.', '(', ')'
        if not ('.' in line and '(' in line and ')' in line):
            return line

        try:  # parse line left to right
            pline = line[:]  # parsed line

            # isolate <class name>
            _cls = pline[:pline.find('.')]

            # isolate and validate <command>
            _cmd = pline[pline.find('.') + 1:pline.find('(')]
            if _cmd not in HBNBCommand.dot_cmds:
                raise Exception

            # if parantheses contain arguments, parse them
            pline = pline[pline.find('(') + 1:pline.find(')')]
            if pline:
                # partition args: (<id>, [<delim>], [<*args>])
                pline = pline.partition(', ')  # pline convert to tuple

                # isolate _id, stripping quotes
                _id = pline[0].replace('\"', '')
                # possible bug here:
                # empty quotes register as empty _id when replaced

                # if arguments exist beyond _id
                pline = pline[2].strip()  # pline is now str
                if pline:
                    # check for *args or **kwargs
                    if pline[0] == '{' and pline[-1] =='}'\
                            and type(eval(pline)) is dict:
                        _args = pline
                    else:
                        _args = pline.replace(',', '')
                        # _args = _args.replace('\"', '')
            line = ' '.join([_cmd, _cls, _id, _args])

        except Exception as mess:
            pass
        finally:
            return line

    def postcmd(self, stop, line):
        """
        Prints if isatty is false
        """
        if not sys.__stdin__.isatty():
            print('(hbnb) ', end='')
        return stop

    def do_quit(self, command):
        """
        Exits the HBNB console
        """
        return True

    def help_quit(self):
        """
        Prints help documentation for "quit" command
        """
        print("Exits the program with formatting\n")

    def do_EOF(self, arg):
        """
        Handles EOF to exit program without formatting
        """
        print()
        return True

    def help_EOF(self):
        """
        Prints help documentation for EOF command
        """
        print("Exits the program without formatting\n")

    def emptyline(self):
        """
        Overrides the emptyline method of CMD
        """
        pass

    def do_create(self, args):
        """
        Creates an object that inherits from BaseModel
        """
        split_args = args.split()
        if len(split_args) == 0:
            print("** class name missing **")
            return
        if split_args[0] in classes:
            new_instance = classes[split_args[0]]()
            new_instance.save()
            print(new_instance.id)
        else:
            print("** class doesn't exist **")

    def help_create(self):
        """
        Help information for create command
        """
        print("Creates a class of any type")
        print("[Usage]: create <className>\n")

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

    def help_show(self):
        """
        Help information for show command """
        print("Shows an individual instance of a class")
        print("[Usage]: show <className> <objectId>\n")

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

    def help_destroy(self):
        """
        Help information for destroy command
        """
        print("Destroys an individual instance of a class")
        print("[Usage]: destroy <className> <objectId>\n")

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

    def help_all(self):
        """
        Help information for all command
        """
        print("Shows all objects, or all of a class")
        print("[Usage]: all <className>\n")

    def do_count(self, args):
        """
        Counts current number of class instances
        """
        count = 0
        for k, v in storage._FileStorage__objects.items():
            if args == k.split('.')[0]:
                count += 1
        print(count)

    def help_count(self):
        """
        Help information for count command
        """
        print("Usage: count <class_name>")

    def do_update(self, args):
        """
        Updates an instance based on the class name and id
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
        attr = split_args[2], split_args[3]
        obj.save()

    def help_update(self):
        """
        Help information for update command
        """
        print("Updates an object with new information")
        print("Usage: update <className> <id> <attName> <attVal>\n")

if __name__ == "__main__":
    HBNBCommand().cmdloop()
