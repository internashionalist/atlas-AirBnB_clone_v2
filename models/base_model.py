#!/usr/bin/python3
"""
This module contains the BaseModel class.
"""
from datetime import datetime
import uuid
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from os import getenv

Base = declarative_base()

time_format = "%Y-%m-%dT%H:%M:%S.%f"


class BaseModel:
    """
    BaseModel class from which all other classes inherit

    Attributes:
        id (str):               id of instance
        created_at (datetime):  time of instance creation
        updated_at (datetime):  time of instance update

    Methods:
        __init__(self,  *args, **kwargs): initializes a new BaseModel instance
        __str__(self):  returns a string representation of the instance
        save(self):     changes updated_at attribute to current time
        to_dict(self):  returns dictionary for instance
        delete(self):   deletes current instance
    """
    id = Column(String(60),
                nullable=False,
                primary_key=True)
    created_at = Column(DateTime,
                        default=datetime.utcnow,
                        nullable=False)
    updated_at = Column(DateTime,
                        default=datetime.utcnow,
                        nullable=False)

    def __init__(self, *args, **kwargs):
        """
        Initializes a new BaseModel instance
        """
        self.id = kwargs.get("id", str(uuid.uuid4()))
        self.created_at = kwargs.get("created_at", datetime.utcnow())
        self.updated_at = kwargs.get("updated_at", datetime.utcnow())

        for key, value in kwargs.items():
            if key != "__class__":
                setattr(self, key, value)

    def __str__(self):
        """
        Returns a string representation of the instance
        """
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """
        Changes updated_at attribute to current time
        """
        from models import storage
        self.updated_at = datetime.utcnow()
        storage.new(self)
        storage.save()
        print(self.id)  # print id of new object

    def to_dict(self):
        """
        Converts instance to dictionary
        """
        time_format = "%Y-%m-%dT%H:%M:%S.%f"
        inst_dict = self.__dict__.copy()
        inst_dict["__class__"] = self.__class__.__name__
        inst_dict["created_at"] = self.created_at.strftime(
            time_format) if isinstance(self.created_at,
                                       datetime) else self.created_at
        inst_dict["updated_at"] = self.updated_at.strftime(
            time_format) if isinstance(self.updated_at,
                                       datetime) else self.updated_at
        if "_sa_instance_state" in inst_dict:
            del inst_dict["_sa_instance_state"]
        return inst_dict

    def delete(self):
        """
        Deletes current instance
        """
        from models import storage
        storage.delete(self)
        storage.save()
