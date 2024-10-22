#!/usr/bin/python3
"""
This module defines the DBStorage class.
"""
import os
from models.base_model import Base
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


class DBStorage:
    """
    DBStorage class for managing the database
    """

    __engine = None
    __session = None

    def __init__(self):
        """
        initializes the database engine
        """
        user = os.getenv("HBNB_MYSQL_USER")
        password = os.getenv("HBNB_MYSQL_PWD")
        host = os.getenv("HBNB_MYSQL_HOST")
        db = os.getenv("HBNB_MYSQL_DB")
        env = os.getenv("HBNB_ENV")

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
            user, password, host, db), pool_pre_ping=True)
        if env == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        returns a dictionary of objects
        """
        if not self.__session:  # if no session, reload
            self.reload()
        obj_dict = {}
        if cls:  # if class is specified, return objects of that class
            for obj in self.__session.query(cls).all():
                key = "{}.{}".format(type(obj).__name__, obj.id)
                obj_dict[key] = obj
        else:  # otherwise, return all objects
            for cls in [State, City, Amenity, Place, Review]:
                for obj in self.__session.query(cls).all():
                    key = "{}.{}".format(type(obj).__name__, obj.id)
                    obj_dict[key] = obj
        return obj_dict

    def new(self, obj):
        """
        creates a new object
        """
        self.__session.add(obj)

    def save(self):
        """
        saves current session
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        deletes an object
        """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """
        reloads objects from database
        """
        session_create = sessionmaker(
            bind=self.__engine,
            expire_on_commit=False)
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(session_create)
