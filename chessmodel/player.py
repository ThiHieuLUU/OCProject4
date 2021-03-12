# ! /usr/bin/venv python3
# coding: utf-8

"""This module is used to represent a chess player with player's individual information."""

import random

from . import basic_backend


class Player:
    """This class describes a normal person with his chess ranking (here, elo rating)."""

    def __init__(self, first_name=None, last_name=None, date_of_birth=None, gender=None,
                 elo_rating=None):
        self._first_name = first_name
        self._last_name = last_name
        self._date_of_birth = date_of_birth
        self._gender = gender
        self._elo_rating = elo_rating

    def __hash__(self):
        """To take player as a key in a dictionary."""

        return hash((self._first_name, self._last_name, self._date_of_birth))  # tuple hash

    def __eq__(self, other):
        """To compare two players."""

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

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, new_last_name):
        self._last_name = new_last_name

    @property
    def date_of_birth(self):
        return self._date_of_birth

    @date_of_birth.setter
    def date_of_birth(self, new_date_of_birth):
        self._date_of_birth = new_date_of_birth

    @property
    def gender(self):
        return self._gender

    @gender.setter
    def gender(self, new_gender):
        self._gender = new_gender

    @property
    def elo_rating(self):
        return self._elo_rating

    @elo_rating.setter
    def elo_rating(self, new_elo_rating):
        self._elo_rating = new_elo_rating

    def get_attributes(self):
        """Get names of all attributes (without protected or private sign) and theirs values."""

        attributes_info = basic_backend.get_attributes(self)
        return attributes_info

    def get_serialized_attributes(self):
        """Serialize all attributes of a player instance in order to save them in a document oriented database (TinyDB).

        In the case of the Player class, this method is the same of get_attributes method because the attributes
        are not build from other class instances.
        """

        return self.get_attributes()

    def set_attrs(self, kwargs):
        """Set values for attributes via a dictionary."""

        basic_backend.set_attrs(self, kwargs)

    @classmethod
    def create_player(cls, attributes_values):
        """Create a chess player from the given set of attribute - value."""

        return basic_backend.create_item(cls, attributes_values)

    def __str__(self):
        """Print all attributes and theirs values for a player."""

        attr_str = basic_backend.get_str(self)
        return attr_str

    def __repr__(self):
        """Display the string representation of a player object."""

        if self._first_name:
            return self._first_name + " " + self._last_name + " - " + self._date_of_birth
        return str(None)

    @classmethod
    def get_players(cls):
        """Method is used to get a random sample of players."""

        players = dict()
        players[0] = cls("Damien", "Adnet", "12/02/1980", "M", 1070)
        players[1] = cls("Lucrèce", "Besnard", "15/02/1980", "M", 1070)
        players[2] = cls("Alexis", "Marchant", "18/01/1980", "M", 670)
        players[3] = cls("Gaël", "Charpentier", "12/02/1980", "M", 470)
        players[4] = cls("Marius", "Bouhier", "09/01/1980", "M", 1250)
        players[5] = cls("Jean-François", "Duchemin", "02/01/1980", "M", 570)
        players[6] = cls("Frédéric", "Colbert", "06/01/1980", "M", 870)
        players[7] = cls("Gaëtan", "Trintignant", "27/01/1980", "M", 770)
        players[8] = cls("Abraham", "Adnet", "12/01/1980", "M", 970)
        players[9] = cls("Nicolas", "Desmarais", "05/01/1980", "M", 1170)
        players[10] = cls("Claude", "Brassard", "03/01/1980", "M", 1470)
        players[11] = cls("Louis", "Bouhier", "15/02/1980", "M", 1090)
        players[12] = cls("Augustin", "Besnard", "15/04/1980", "M", 1490)
        players[13] = cls("Alice", "Duchemin", "15/09/1980", "F", 1190)
        players[14] = cls("Camille", "Victor", "25/02/1980", "F", 990)
        players[15] = cls("Hugo", "Albert", "10/09/1980", "M", 890)
        players[16] = cls("Marie", "Colbert", "10/02/1980", "F", 690)
        players[17] = cls("Pascal", "Luc", "15/01/1980", "M", 490)
        players[18] = cls("Antoine", "Yvon", "15/01/1980", "M", 490)
        players[19] = cls("Alex", "Martin", "15/05/1980", "M", 790)
        players[20] = cls("Joël", "Desmoulins", "15/06/1980", "M", 990)
        players[21] = cls("Hervé", "Pesnard", "15/07/1980", "M", 1590)
        players[22] = cls("Ivan", "Desnard", "15/08/1980", "M", 1390)

        # Pick randomly players with a given number of players.
        # original_list = [players[i] for i in range(22)]
        # number_of_players = 8
        # list_of_players = random.sample(original_list, number_of_players)

        # For test cases to check the algorithm of constructing two players for a match.
        # The must not be encountered before.
        list_of_players = [players[i] for i in range(1, 9, 1)]

        return list_of_players
