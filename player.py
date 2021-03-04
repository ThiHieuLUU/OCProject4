#! /usr/bin/venv python3
# coding: utf-8

"""This module is used to model a chess player with his individual information."""

import basic_backend


class Player:
    """This class describes a normal person with his chess rating (here, elo rating)"""

    def __init__(self, first_name=None, last_name=None, date_of_birth=None, gender=None,
                 elo_rating=None):
        self._first_name = first_name
        self._last_name = last_name
        self._date_of_birth = date_of_birth
        self._gender = gender
        self._elo_rating = elo_rating

    def __hash__(self):
        return hash((self._first_name, self._last_name, self._date_of_birth))  # tuple hash

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return (self._first_name, self._last_name, self._date_of_birth, self._gender) \
                   == (other.first_name, other.last_name, other.date_of_birth, other.gender)
        return False

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, new_first_name):
        self._first_name = new_first_name

    @first_name.deleter
    def first_name(self):
        del self._first_name

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, new_last_name):
        self._last_name = new_last_name

    @last_name.deleter
    def last_name(self):
        del self._last_name

    @property
    def date_of_birth(self):
        return self._date_of_birth

    @date_of_birth.setter
    def date_of_birth(self, new_date_of_birth):
        self._date_of_birth = new_date_of_birth

    @date_of_birth.deleter
    def date_of_birth(self):
        del self._date_of_birth

    @property
    def gender(self):
        return self._gender

    @gender.setter
    def gender(self, new_gender):
        self._gender = new_gender

    @gender.deleter
    def gender(self):
        del self._gender

    @property
    def elo_rating(self):
        return self._elo_rating

    @elo_rating.setter
    def elo_rating(self, new_elo_rating):
        self._elo_rating = new_elo_rating

    @elo_rating.deleter
    def elo_rating(self):
        del self._elo_rating

    def get_attributes(self):
        """Get attribute names (without protected or private sign) and theirs values."""
        attributes_info = basic_backend.get_attributes(self)
        return attributes_info

    def set_attrs(self, kwargs):
        """Set attributes' values via a dictionary."""

        basic_backend.set_attrs(self, kwargs)

    @classmethod
    def create_player(cls, attributes_values):
        """Create a chess player from the given set of attribute - value (under dictionary format)."""

        # Retrieve the class type
        obj_type = globals()[cls.__name__]
        return basic_backend.create_item(attributes_values, obj_type)

    def __str__(self):
        """Print all attributes and theirs values for a chess player"""

        attr_str = basic_backend.get_str(self)
        return attr_str

    def __repr__(self):
        """Display the string representation of a chess player object."""

        if self._first_name is not None:
            return self._first_name + " " + self._last_name + " - " + self._date_of_birth
        return str(None)


p1 = Player("Lucrèce", "Besnard", "12/02/2021", "M", 1070)
p2 = Player("Alexis", "Marchant", "18/01/2021", "M", 670)
p3 = Player("Gaël", "Charpentier", "12/02/2021", "M", 470)
p4 = Player("Marius", "Bouhier", "09/01/2021", "M", 1250)
p5 = Player("Jean-François", "Duchemin", "02/01/2021", "M", 570)
p6 = Player("Frédéric", "Colbert", "06/01/2021", "M", 870)
p7 = Player("Gaëtan", "Trintignant", "27/01/2021", "M", 770)
p8 = Player("Abraham", "Adnet", "12/01/2021", "M", 970)
p9 = Player("Nicolas", "Desmarais", "05/01/2021", "M", 1170)
p10 = Player(" Claude", "Brassard", "03/01/2021", "M", 1470)
p11 = Player("Lucas", "Besnard", "15/02/2021", "M", 1090)

# players = [p1, p2, p3, p4, p5, p6, p7, p8, p9]
# players = [p1, p2, p3, p4, p5, p6, p7, p8]
players = [p4, p5, p6, p7, p8, p9, p10, p11]
