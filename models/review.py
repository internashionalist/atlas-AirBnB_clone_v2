#!/usr/bin/python3
"""
This module contains the Review class.
"""
import models
from os import getenv
from models.base_model import BaseModel
from models.place import Place
from models.user import User


if getenv("HBNB_TYPE_STORAGE") == "db":  # database storage
    from sqlalchemy import Column, String, ForeignKey
    from models.base_model import Base

    class Review(BaseModel, Base):
        """
        Review class (contains place_id, user_id, text) for database storage

        Attributes:
            place_id (str):     place id
            user_id (str):      user id
            text (str):         review text
        """
        __tablename__ = "reviews"
        place_id = Column(String(60),
                          ForeignKey("places.id"),
                          nullable=False)
        user_id = Column(String(60),
                         ForeignKey("users.id"),
                         nullable=False)
        text = Column(String(1024),
                      nullable=False)

        def __init__(self, *args, **kwargs):
            """
            Initializes a review
            """
            super().__init__(*args, **kwargs)

        def save(self):
            """
            checks if the place_id, user_id, and text attribute were
            provided before saving normally if they both were given.
            """
            # check if place_id was specified
            if self.place_id is None:
                print("** place_id not provided **")
                return

            # Check if given place id exists in database
            place_exists = False
            for city in models.storage.all(Place).values():
                if city.id == self.place_id:
                    place_exists = True
                    break
            if not place_exists:
                print("** place with that id does not exist **")
                return

            # check if user_id was specified
            if self.user_id is None:
                print("** user_id not provided **")
                return

            # Check if given user id exists in database
            user_exists = False
            for user in models.storage.all(User).values():
                if user.id == self.user_id:
                    user_exists = True
                    break
            if not user_exists:
                print("** user with that id does not exist **")
                return

            # check if text was specified
            if self.text is None:
                print("** text not provided **")
                return

            super().save()

else:
    class Review(BaseModel):
        """
        Reviews class (contains place_id, user_id, text) for file storage

        Attributes:
            place_id (str):     place id
            user_id (str):      user id
            text (str):         review text
        """
        place_id = None
        user_id = None
        text = None

        def __init__(self, *args, **kwargs):
            """
            Initializes a review
            """
            super().__init__(*args, **kwargs)

        def save(self):
            """
            checks if the place_id, user_id, and text attribute were
            provided before saving normally if they both were given.
            """
            # check if place_id was specified
            if self.place_id is None:
                print("** place_id not provided **")
                return

            # Check if given place id exists in database
            place_exists = False
            for place in models.storage.all(Place).values():
                if place.id == self.place_id:
                    place_exists = True
                    break
            if not place_exists:
                print("** place with that id does not exist **")
                return

            # check if user_id was specified
            if self.user_id is None:
                print("** user_id not provided **")
                return

            # Check if given user id exists in database
            user_exists = False
            for user in models.storage.all(User).values():
                if user.id == self.user_id:
                    user_exists = True
                    break
            if not user_exists:
                print("** user with that id does not exist **")
                return

            # check if text was specified
            if self.text is None:
                print("** text not provided **")
                return

            super().save()
