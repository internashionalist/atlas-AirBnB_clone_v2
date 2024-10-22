#!/usr/bin/python3
"""
This module contains the City class.
"""
import models
from models.base_model import BaseModel
from os import getenv
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class City(BaseModel):
    """
    City class (contains state_id and name)
    """
    if getenv('HBNB_TYPE_STORAGE') == 'db':  # database storage
        __tablename__ = 'cities'
        name = Column(String(128),
                      nullable=False)
        state_id = Column(String(60),
                          ForeignKey('states.id'),
                          nullable=False)
        state = relationship('State',
                             backref='cities',
                             cascade='all, delete-orphan')
    else: # for file storage
        state_id = ""
        name = ""

    def __init__(self, *args, **kwargs):
        """
        initializes new city
        """
        super().__init__(*args, **kwargs)  # call BaseModel
