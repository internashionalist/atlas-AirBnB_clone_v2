#!/usr/bin/python3
"""
This module contains the State class.
"""
import models
from models.base_model import BaseModel
from os import getenv


if getenv("HBNB_TYPE_STORAGE") == "db":  # database storage
    from sqlalchemy import Column, String
    from sqlalchemy.orm import relationship
    from models.base_model import Base

    class State(BaseModel, Base):
        """
        State class (contains name only) for database storage

        Attributes:
            name (str):     name of state
            cities (list):  City instances in state

        Methods:
            cities(self):   returns list of City instances in state
        """
        __tablename__ = "states"
        name = Column(String(128),
                      nullable=False)
        cities = relationship("City",
                              backref="state",
                              cascade="all, delete, delete-orphan")

        def __init__(self, *args, **kwargs):
            """
            Initializes a state
            """
            super().__init__(*args, **kwargs)

        def save(self):
            """
            checks if the name attribute was provided
            before saving normally if it was.
            """
            if self.name is None:
                print("** name not provided **")
                return

            super().save()

else:
    class State(BaseModel):
        """
        State class (contains name only) for file storage

        Attributes:
            name (str):     name of state
        """
        name = None

        @property
        def cities(self):  # getter for cities
            """
            returns list of City instances in state
            """
            return [city for city in models.storage.all("City").values()
                    if city.state_id == self.id]

        def __init__(self, *args, **kwargs):
            """
            Initializes a state
            """
            super().__init__(*args, **kwargs)

        def save(self):
            """
            checks if the name attribute was provided
            before saving normally if it was.
            """
            if self.name is None:
                print("** name not provided **")
                return

            super().save()
