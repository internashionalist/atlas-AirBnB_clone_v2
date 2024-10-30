#!/usr/bin/python3
"""
This module contains the Place class.
"""
import models
from os import getenv
from models.base_model import BaseModel
from models.city import City
from models.user import User


if getenv("HBNB_TYPE_STORAGE") == "db":
    from sqlalchemy import Column, String, Integer, Float, Table, ForeignKey
    from sqlalchemy.orm import relationship
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
            description (str):      description (optional)
            number_rooms (int):     number of rooms
            number_bathrooms (int): number of bathrooms
            max_guest (int):        maximum number of guests
            price_by_night (int):   price per night
            latitude (float):       latitude (optional)
            longitude (float):      longitude (optional)
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
            
        def save(self):
            """
            checks if the city_id, user_id, and name attribute were
            provided before saving normally if they both were given.
            """
            # check if city_id was specified
            if self.city_id is None:
                print("** city_id not provided **")
                return

            # Check if given city id exists in database
            city_exists = False
            for city in models.storage.all(City).values():
                if city.id == self.city_id:
                    city_exists = True
                    break
            if not city_exists:
                print("** city with that id does not exist **")
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

            # check if name was specified
            if self.name is None:
                print("** name not provided **")
                return

            super().save()

else:
    class Place(BaseModel):
        """
        Defines a place by various attributes (for file storage)

        Attributes:
            city_id (str):          city id
            user_id (str):          user id
            name (str):             name
            description (str):      description (optional)
            number_rooms (int):     number of rooms
            number_bathrooms (int): number of bathrooms
            max_guest (int):        maximum number of guests
            price_by_night (int):   price per night
            latitude (float):       latitude (optional)
            longitude (float):      longitude (optional)
            reviews (list):         Review instances of Place
            amenity_ids (list):     Amenity instances of Place
        """
        city_id = None
        user_id = None
        name = None
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = None
        longitude = None
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

        def save(self):
            """
            checks if the city_id, user_id, and name attribute were
            provided before saving normally if they both were given.
            """
            # check if city_id was specified
            if self.city_id is None:
                print("** city_id not provided **")
                return

            # Check if given city id exists in database
            city_exists = False
            for city in models.storage.all(City).values():
                if city.id == self.city_id:
                    city_exists = True
                    break
            if not city_exists:
                print("** city with that id does not exist **")
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

            # check if name was specified
            if self.name is None:
                print("** name not provided **")
                return

            super().save()
