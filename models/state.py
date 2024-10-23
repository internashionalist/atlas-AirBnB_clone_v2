#!/usr/bin/python3
"""
This module contains the State class.
"""
import models
from models.base_model import BaseModel, Base
from models.city import City
from os import getenv
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String


class State(BaseModel, Base):
    """
    State class (contains name only)

    Attributes:
        name (str):     name of state
        cities (list):  City instances in state

    Methods:
        cities(self):   returns list of City instances in state
    """
    if getenv("HBNB_TYPE_STORAGE") == "db":  # database storage
        __tablename__ = "states"
        name = Column(String(128),
                      nullable=False)
        cities = relationship("City",
                              backref="state",
                              cascade="all, delete, delete-orphan")
    else:
        name = ""

        @property
        def cities(self):  # getter for cities
            """
            returns list of City instances in state
            """
            return [city for city in models.storage.all(City).values()
                    if city.state_id == self.id]
