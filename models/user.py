#!/usr/bin/python3
"""
This module contains the User class for both file and database storage.
"""
from os import getenv
from models.base_model import BaseModel


if getenv("HBNB_TYPE_STORAGE") == "db":
    from models.base_model import Base
    from sqlalchemy import Column, String
    from sqlalchemy.orm import relationship

    class User(BaseModel, Base):
        """
        Defines a user by various attributes (for database storage)

        Attributes:
            email (str):        email
            password (str):     password
            first_name (str):   first name (optional)
            last_name (str):    last name (optional)
            places (list):      Place instances of User
        """
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
        reviews = relationship("Review",
                               backref="user",
                               cascade="all, delete, delete-orphan")

        def __init__(self, *args, **kwargs):
            """
            initializes a user
            """
            super().__init__(*args, **kwargs)

        def save(self):
            """
            checks if the email & password attributes were provided
            before saving normally if both are provided.
            """
            # check if email is given
            if self.email is None:
                print("** email not provided **")
                return
            # check if password is given
            if self.password is None:
                print("** password not provided **")
                return

            super().save()

else:
    class User(BaseModel):
        """
        Defines a user by various attributes (for file storage)

        Attributes:
            email (str):        email
            password (str):     password
            first_name (str):   first name (optional)
            last_name (str):    last name (optional)
        """
        email = None
        password = None
        first_name = None
        last_name = None

        def __init__(self, *args, **kwargs):
            """
            initializes a user
            """
            super().__init__(*args, **kwargs)

        def save(self):
            """
            checks if the email & password attributes were provided
            before saving normally if both are provided.
            """
            # check if email is given
            if self.email is None:
                print("** email not provided **")
                return
            # check if password is given
            if self.password is None:
                print("** password not provided **")
                return

            super().save()
