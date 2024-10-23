#!/usr/bin/python3
"""
This module contains the Review class.
"""
import models
from os import getenv
from models.base_model import BaseModel


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

else:
    class Review(BaseModel):
        """
        Reviews class (contains place_id, user_id, text) for file storage

        Attributes:
            place_id (str):     place id
            user_id (str):      user id
            text (str):         review text
        """
        place_id = ""
        user_id = ""
        text = ""

        def __init__(self, *args, **kwargs):
            """
            Initializes a review
            """
            super().__init__(*args, **kwargs)
