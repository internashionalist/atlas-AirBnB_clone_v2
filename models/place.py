#!/usr/bin/python3
"""
This module contains the Place class.
"""
import models
from os import getenv
from models.base_model import BaseModel

if getenv("HBNB_TYPE_STORAGE") == "db":
    from sqlalchemy import Column, String, Integer, Float, Table, ForeignKey
    from sqlalchemy.orm import relationship
    from models.review import Review
    from models.amenity import Amenity
    from models.base_model import Base

    amenity_place = Table("place_amenity", Base.metadata,
                          Column("place_id", String(60),
                                 ForeignKey("places.id"),
                                 primary_key=True,
                                 nullable=False),
                          Column("amenity_id", String(60),
                                 ForeignKey("amenities.id"),
                                 primary_key=True,
                                 nullable=False),
                          extend_existing=True)

    class Place(BaseModel, Base):
        """
        Defines a place by various attributes (for database storage)

        Attributes:
            city_id (str):          city id
            user_id (str):          user id
            name (str):             name
            description (str):      description
            number_rooms (int):     number of rooms
            number_bathrooms (int): number of bathrooms
            max_guest (int):        maximum number of guests
            price_by_night (int):   price per night
            latitude (float):       latitude
            longitude (float):      longitude
            reviews (list):         Review instances of Place
            amenities (list):       Amenity instances of Place
        """
        __tablename__ = "places"
        city_id = Column(String(60),
                         ForeignKey("cities.id"),
                         nullable=False)
        user_id = Column(String(60),
                         ForeignKey("users.id"),
                         nullable=False)
        name = Column(String(128),
                      nullable=False)
        description = Column(String(1024),
                             nullable=True)
        number_rooms = Column(Integer,
                              default=0,
                              nullable=False)
        number_bathrooms = Column(Integer,
                                  default=0,
                                  nullable=False)
        max_guest = Column(Integer,
                           default=0,
                           nullable=False)
        price_by_night = Column(Integer,
                                default=0,
                                nullable=False)
        latitude = Column(Float,
                          nullable=True)
        longitude = Column(Float,
                           nullable=True)
        reviews = relationship("Review",
                               backref="places",
                               cascade="all, delete, delete-orphan")
        amenities = relationship("Amenity",
                                 secondary=amenity_place,
                                 back_populates="places",
                                 viewonly=False)

        def __init__(self, *args, **kwargs):
            """
            Initializes a place
            """
            super().__init__(*args, **kwargs)

else:
    class Place(BaseModel):
        """
        Defines a place by various attributes (for file storage)

        Attributes:
            city_id (str):          city id
            user_id (str):          user id
            name (str):             name
            description (str):      description
            number_rooms (int):     number of rooms
            number_bathrooms (int): number of bathrooms
            max_guest (int):        maximum number of guests
            price_by_night (int):   price per night
            latitude (float):       latitude
            longitude (float):      longitude
            reviews (list):         Review instances of Place
            amenity_ids (list):     Amenity instances of Place
        """
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

        @property
        def reviews(self):
            """
            Returns list of Review instances linked to Place
            """
            return [review for review
                    in models.storage.all("Review").values()
                    if review.place_id == self.id]

        @property
        def amenities(self):
            """
            Returns list of Amenity instances linked to Place
            """
            return [amenity for amenity
                    in models.storage.all("Amenity").values()
                    if amenity.id in self.amenity_ids]

        @amenities.setter
        def amenities(self, obj):
            """
            Sets amenity_ids when adding an Amenity to Place
            """
            if isinstance(obj, models.Amenity):
                self.amenity_ids.append(obj.id)

        def __init__(self, *args, **kwargs):
            """
            Initializes a place
            """
            super().__init__(*args, **kwargs)
