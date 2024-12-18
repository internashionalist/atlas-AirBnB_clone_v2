#!/usr/bin/python3
"""
This module defines the DBStorage class.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
import os


class DBStorage:
    """
    DBStorage class for managing the database

    Attributes:
        __engine (sqlalchemy.engine.base.Engine):   database engine
        __session (sqlalchemy.orm.session.Session): database session

    Methods:
        __init__(self):         initializes the database engine
        all(self, cls=None):    returns a dictionary of objects
        new(self, obj):         creates a new object
        save(self):             saves current session
        delete(self, obj=None): deletes an object
        reload(self):           reloads objects from database
    """
    __engine = None
    __session = None

    classes = {
        "User": User,
        "State": State,
        "City": City,
        "Amenity": Amenity,
        "Place": Place,
        "Review": Review
    }

    def __init__(self):
        """
        Initializes the database connection
        """
        user = os.getenv("HBNB_MYSQL_USER")
        password = os.getenv("HBNB_MYSQL_PWD")
        host = os.getenv("HBNB_MYSQL_HOST")
        db = os.getenv("HBNB_MYSQL_DB")
        env = os.getenv("HBNB_ENV")

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
            user, password, host, db), pool_pre_ping=True)
        if os.getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Returns a dictionary of objects
        """
        obj_dict = {}
        objs = []
        if cls:
            if isinstance(cls, str):
                cls = self.classes.get(cls)
            if cls:
                objs = self.__session.query(cls).all()
        else:
            for cls_name in self.classes.values():
                objs.extend(self.__session.query(cls_name).all())
        for obj in objs:
            key = self.key_create(obj)
            obj_dict[key] = obj

        return obj_dict

    def new(self, obj):
        """
        Creates a new object
        """
        self.__session.add(obj)

    def save(self):
        """
        Saves current session
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        Deletes an object
        """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """
        Reloads objects from the database
        """
        Base.metadata.create_all(self.__engine)
        session_builder = sessionmaker(
            bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(session_builder)

    def close(self):
        """
        Closes the session and the connection
        """
        self.__session.remove()

    def key_create(self, obj):
        """
        Creates a key for an object
        """
        return "{}.{}".format(type(obj).__name__, obj.id)
