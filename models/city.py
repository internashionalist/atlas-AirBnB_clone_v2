#!/usr/bin/python3
"""
This module contains the City class.
"""
import models
from models.base_model import BaseModel, Base
from os import getenv
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class City(BaseModel, Base):
    """
    City class (contains state_id and name)

    Attributes:
        name (str):     name of city
        state_id (str): state id
        places (list):  Place instances in city

    Methods:
        places(self):   returns list of Place instances in city
    """
    __tablename__ = "cities"
    name = Column(String(128),
                  nullable=False)
    state_id = Column(String(60),
                      ForeignKey("states.id"),
                      nullable=False)
    places = relationship("Place",
                            backref="cities",
                            cascade="all, delete, delete-orphan")
