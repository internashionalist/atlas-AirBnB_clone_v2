#!/usr/bin/python3
"""
This module contains the State class.
"""
import models
from models.base_model import BaseModel, Base
from os import getenv
from sqlalchemy import relationship
from sqlalchemy import Column, String


class State(BaseModel, Base):
    """
    State class (contains name only)
    """
    if getenv("HBNB_TYPE_STORAGE") == "db":  # database storage
        __tablename__ = "states"
        name = Column(String(128),
                      nullable=False)
        cities = relationship("City",
                              backref="state",
                              cascade="all, delete-orphan")
    else:
        name = ""

        @property
        def cities(self):  # getter for cities
            """
            returns list of City instances in state
            """
            return [city for city in models.storage.all("City").values()
                    if city.state_id == self.id]
