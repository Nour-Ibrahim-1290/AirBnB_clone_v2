#!/usr/bin/python3
""" Place Module for HBNB project """

from models.base_model import BaseModel, Base

# new imports for phase 2
from sqlalchemy import Column, String, Integer,
from sqlalchemy import Float, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from os import getenv

association_table = Table(
        'place_amenity', Base.metadata,
        Column(
            'place_id', String(60),
            ForeignKey('places.id'), primary_key=True,
            nullable=False
            ),
        Column(
            'amenity_id', String(60),
            ForeignKey('amenities.id'), primary_key=True,
            nullable=False
            )
        )


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = "places"

    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(128), nullable=False)
    number_rooms = Column(Integer, default=0, nullable=False)
    number_bathrooms = Column(Integer, default=0, nullable=False)
    max_guest = Column(Integer, default=0, nullable=False)
    price_by_night = Column(Integer, default=0, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    reviews = relationship("Review", backref="place", cascade="all, delete")
    amenities = relationship(
            "Amenity", secondary='place_amenity',
            viewonly=False, backref="amenities"
            )

    if getenv("HBNB_TYPE_STORAGE") != "db":
        @property
        def reviews(self):
            """Returns the list of Review instances"""
            return [review for review in self.reviews]

        @property
        def amenities(self):
            """Returns a list of Amenity instances"""
            return [amenity for amenity in self.amenities]

        @amenities.setter
        def amenities(self, obj):
            """Appends an amenity id to the attribute
            amenity_id
            """
            if type(obj) == Amenity:
                self.amenity_ids.append(obj.id)
