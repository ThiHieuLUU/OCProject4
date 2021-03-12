#! /usr/bin/venv python3
# coding: utf-8

"""This module is used to model a location, e.g. location for a tournament."""

from . import basic_backend


class Location:
    """This class represents a normal address."""

    def __init__(self, building_number=None, street=None, city=None, zipcode=None):
        self._building_number = building_number
        self._street = street
        self._city = city
        self._zipcode = zipcode

    @property
    def building_number(self):
        return self._building_number

    @building_number.setter
    def building_number(self, building_number):
        self._building_number = building_number

    @property
    def street(self):
        return self._street

    @street.setter
    def street(self, street):
        self._street = street

    @property
    def city(self):
        return self._city

    @city.setter
    def city(self, city):
        self._city = city

    @property
    def zipcode(self):
        return self._zipcode

    @zipcode.setter
    def zipcode(self, zipcode):
        self._zipcode = zipcode

    @classmethod
    def create_location(cls, attributes_values):
        """Create a location from a dictionary."""

        return basic_backend.create_item(cls, attributes_values)

    def get_attributes(self):
        """Get names of all attributes (without protected or private sign) and theirs values."""

        attributes_info = basic_backend.get_attributes(self)
        return attributes_info

    def get_serialized_attributes(self):
        """Serialize all attributes of a location instance in order to save them in a document oriented database
        (TinyDB here).

        In the case of the Location class, this method is the same of get_attributes method because the attributes
        are not other class instances.
        """

        return self.get_attributes()

    def set_attrs(self, kwargs):
        """Set values for attributes via a dictionary."""

        basic_backend.set_attrs(self, kwargs)

    def __str__(self):
        """Print all attributes and theirs values for a location."""

        attr_str = basic_backend.get_str(self)
        return "\n" + attr_str

    def __repr__(self):
        """Display the string representation of a location object."""

        attr_names, attr_values = self.get_attributes()
        attr_str = ""

        for attr_name, attr_value in zip(attr_names, attr_values):
            attr_str += str(attr_name).capitalize() + ': ' + str(attr_value) + "\n"

        return attr_str
