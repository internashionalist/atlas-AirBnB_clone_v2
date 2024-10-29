#!/usr/bin/python3
"""
This module contains the City class.
"""
import models
from models.base_model import BaseModel
from os import getenv
from models.state import State


if getenv("HBNB_TYPE_STORAGE") == "db":  # database storage
    from sqlalchemy import Column, String, ForeignKey
    from sqlalchemy.orm import relationship
    from models.base_model import Base

    class City(BaseModel, Base):
        """
        City class (contains state_id and name) for database storage

        Attributes:
            name (str):     name of city
            state_id (str): state id
        """
        __tablename__ = "cities"
        state_id = Column(String(60),
                          ForeignKey("states.id"),
                          nullable=False)
        name = Column(String(128),
                      nullable=False)
        places = relationship("Place",
                              backref="cities",
                              cascade="all, delete, delete-orphan")

        def __init__(self, *args, **kwargs):
            """
            Initializes a city
            """
            super().__init__(*args, **kwargs)
            
        def save(self):
            """
            checks if the name and state_id attribute were provided
            before saving normally if they both were given.
            """
            # check if state_id was specified
            if self.state_id is None:
                print("** state_id not provided **")
                return

            # Check if given state id exists in database
            state_exists = False
            for state in models.storage.all(State).values():
                if state.id == self.state_id:
                    state_exists = True
                    break
            if not state_exists:
                print("** state with that id does not exist **")
                return

            # check if name was specified
            if self.name is None:
                print("** name not provided **")
                return

            super().save()

else:
    class City(BaseModel):
        """
        City class (contains state_id and name) for file storage

        Attributes:
            name (str):     name of city
            state_id (str): state id
        """
        state_id = None
        name = None

        def __init__(self, *args, **kwargs):
            """
            Initializes a city
            """
            super().__init__(*args, **kwargs)

        def save(self):
            """
            checks if the name and state_id attribute were provided
            before saving normally if they both were given.
            """
            # check if state_id was specified
            if self.state_id is None:
                print("** state_id not provided **")
                return

            # Check if given state id exists in database
            state_exists = False
            for state in models.storage.all(State).values():
                if state.id == self.state_id:
                    state_exists = True
                    break
            if not state_exists:
                print("** state with that id does not exist **")
                return

            # check if name was specified
            if self.name is None:
                print("** name not provided **")
                return

            super().save()
