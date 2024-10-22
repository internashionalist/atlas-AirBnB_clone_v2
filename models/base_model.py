#!/usr/bin/python3
"""
This module contains the BaseModel class.
"""
from os import getenv
import models
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

if getenv("HBNB_TYPE_STORAGE") == "db":
    Base = declarative_base()
else:
    Base = object

time_format = "%Y-%m-%dT%H:%M:%S.%f"


class BaseModel:
    """
    A base class for all hbnb models
    """

    if getenv('HBNB_TYPE_STORAGE') == 'db':  # database storage
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
        initializes a new BaseModel instance
        """
        self.id = kwargs.get('id', str(uuid.uuid4()))
        self.created_at = datetime.strptime(
            kwargs.get('created_at',
                    datetime.utcnow().strftime(time_format)),
                    time_format)
        self.updated_at = datetime.strptime(
            kwargs.get('updated_at',
                    datetime.utcnow().strftime(time_format)),
                    time_format)
        for key, value in kwargs.items():
            if key != '__class__':
                setattr(self, key, value)

    def __str__(self):
        """
        returns a string representation of the instance
        """
        return "[{}] ({}) {}".format(type(self).__name__, self.id,
                                    self.__dict__)

    def save(self):
        """
        changes updated_at attribute to current time
        """
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """
        returns dictionary for instance
        """
        inst_dict = self.__dict__.copy()
        inst_dict['__class__'] = self.__class__.__name__
        inst_dict['created_at'] = self.created_at.strftime(time_format)
        inst_dict['updated_at'] = self.updated_at.strftime(time_format)
        if '_sa_instance_state' in inst_dict:
            del inst_dict['_sa_instance_state']
        return inst_dict
    
    def delete(self):
        """
        deletes current instance
        """
        models.storage.delete(self)
        models.storage.save()
