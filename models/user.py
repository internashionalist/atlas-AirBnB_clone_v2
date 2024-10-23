#!/usr/bin/python3
"""
This module contains the User class.
"""
from os import getenv
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """
    defines a user by various attributes
    """
    if getenv("HBNB_TYPE_STORAGE") == "db":
        __tablename__ = "users"
        email = Column(String(128),
                    nullable=False)
        password = Column(String(128),
                        nullable=False)
        first_name = Column(String(128),
                            nullable=True)
        last_name = Column(String(128),
                        nullable=True)
        places = relationship("Place",
                                backref="user",
                                cascade="all, delete, delete-orphan")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        """
        initializes a user
        """
        super().__init__(*args, **kwargs)
