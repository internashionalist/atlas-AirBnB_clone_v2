#!/usr/bin/python3
"""
This module contains the Amenity class.
"""
import models
from models.base_model import BaseModel
from os import getenv


if getenv("HBNB_TYPE_STORAGE") == "db":  # database storage
    from sqlalchemy import Column, String, Table, ForeignKey
    from sqlalchemy.orm import relationship
    from models.base_model import Base

    place_amenity = Table("place_amenity", Base.metadata,
                          Column("place_id", String(60),
                                 ForeignKey("places.id"),
                                 primary_key=True, nullable=False),
                          Column("amenity_id", String(60),
                                 ForeignKey("amenities.id"),
                                 primary_key=True, nullable=False),
                          extend_existing=True)

    class Amenity(BaseModel, Base):
        """
        Amenity class (contains name only) for database storage

        Attributes:
            name (str):             name of amenity
            place_amenities (list): Place instances with amenity
        """
        __tablename__ = "amenities"
        name = Column(String(128),
                      nullable=False)
        places = relationship("Place",
                              secondary=place_amenity,
                              back_populates="amenities",
                              viewonly=False)

        def __init__(self, *args, **kwargs):
            """
            Initializes an amenity
            """
            super().__init__(*args, **kwargs)

        def save(self):
            """
            checks if the name attribute was provided
            before saving normally if it was.
            """
            # check if name is given
            if self.name is None:
                print("** name not provided **")
                return

            super().save()

else:
    class Amenity(BaseModel):
        """
        Amenity class (contains name only) for file storage

        Attributes:
            name (str):     name of amenity
        """
        name = None

        @property
        def place_amenities(self):
            """
            returns list of Place instances with amenity
            """
            return [place for place in models.storage.all("Place").values()
                    if place.amenity_ids == self.id]

        def __init__(self, *args, **kwargs):
            """
            Initializes an amenity
            """
            super().__init__(*args, **kwargs)

        def save(self):
            """
            checks if the name attribute was provided
            before saving normally if it was.
            """
            # check if name is given
            if self.name is None:
                print("** name not provided **")
                return

            super().save()


