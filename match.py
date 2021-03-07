#! /usr/bin/venv python3
# coding: utf-8

"""This module is used to model a chess match with two players and theirs scores."""

import copy

import basic_backend
import player


class Match:
    """This class describes a chess match using a tuple which contains two lists.

    Each list contains a player and his score for the match.
    """

    def __init__(self, player1=None, score1=None, player2=None, score2=None):
        self._match = ([player1, score1], [player2, score2])

    @property
    def match(self):
        return self._match

    @match.setter
    def match(self, new_match):
        self._match = new_match

    @match.deleter
    def match(self):
        del self._match

    def get_serialized_attributes(self):
        """Serialize all attributes of a match instance in order to save them in a document oriented database
        (TinyDB).
        """

        attributes_info = basic_backend.get_attributes(self)
        # Do not use new_dict = attributes_info or attributes_info.copy()
        # because the change of new_dict will lead to the change of attributes_info
        # (e.g. containing others class instances).
        new_dict = copy.deepcopy(attributes_info)
        for key, value in new_dict.items():
            if key == "match":
                # Change from a player instance to its serialization (a dictionary of attributes and serialized values)
                player1_attr_str = value[0][0].get_attributes()
                player2_attr_str = value[1][0].get_attributes()
                new_dict["match"][0][0] = player1_attr_str
                new_dict["match"][1][0] = player2_attr_str
        return new_dict

    def get_attributes(self):
        """Get names of attributes (without protected or private sign) and theirs values."""

        attributes_info = basic_backend.get_attributes(self)
        return attributes_info

    def set_attrs(self, kwargs):
        """Set values for all attributes via a dictionary."""

        basic_backend.set_attrs(self, kwargs)

    def update_match(self, score1, score2):
        """Update match when the scores of two players are known."""

        self._match[0][1] = score1
        self._match[1][1] = score2

    def get_players_from_match(self):
        """To display two players of a match."""

        return repr(self._match[0][0]), repr(self._match[1][0])

    @classmethod
    def get_deserialized_match(cls, serialized_attributes_values):
        """Rebuilt a match object from serialized attributes-values
        (e.g. from TinyDB).
        """

        for key in serialized_attributes_values.keys():
            if key == "match":
                serialized_attributes_values["match"] = tuple(
                    serialized_attributes_values["match"]
                )
                deserialized_player1 = player.Player.create_player(
                    serialized_attributes_values[key][0][0]
                )
                deserialized_player2 = player.Player.create_player(
                    serialized_attributes_values[key][1][0]
                )
                serialized_attributes_values["match"][0][0] = deserialized_player1
                serialized_attributes_values["match"][1][0] = deserialized_player2

        return basic_backend.create_item(serialized_attributes_values, cls)

    def __str__(self):
        """Set values for attributes via a dictionary."""

        attr_str = basic_backend.get_str(self)
        return attr_str

    def __repr__(self):
        """Display the string representation of a chess match object."""

        if self._match[0][0] is not None:
            return basic_backend.get_str(self)
        return str(None)
