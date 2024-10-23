#!/usr/bin/python3
"""
This module contains the City class.
"""
import models
from models.base_model import BaseModel
from os import getenv


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

else:
    class City(BaseModel):
        """
        City class (contains state_id and name) for file storage

        Attributes:
            name (str):     name of city
            state_id (str): state id
        """
        state_id = ""
        name = ""

        def __init__(self, *args, **kwargs):
            """
            Initializes a city
            """
            super().__init__(*args, **kwargs)