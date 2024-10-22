#!/usr/bin/python3
"""
This module contains the State class.
"""
import models
from models.base_model import BaseModel
from os import getenv
from sqlalchemy import relationship
from sqlalchemy import Column, String


class State(BaseModel):
    """
    State class
    """
    if getenv('HBNB_TYPE_STORAGE') == 'db':  # database storage
        __tablename__ = 'states'
        name = Column(String(128), nullable=False)
        cities = relationship('City', backref='state')
    else:
        name = ""

    def __init__(self, *args, **kwargs):
        """
        initializes new state
        """
        super().__init__(*args, **kwargs) # call BaseModel

    if getenv('HBNB_TYPE_STORAGE') != 'db':  # file storage
        @property
        def cities(self):  # getter attribute
            """
            returns list of City instances in state
            """
            city_values = models.storage.all('City').values()
            cities_list = []
            for city in city_values:
                if city.state_id == self.id:
                    cities_list.append(city)
            return cities_list
