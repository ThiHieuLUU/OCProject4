#! /usr/bin/venv python3
# coding: utf-8

"""This module is used to model a chess round associated with a list of matches."""

import copy

import basic_backend
import match


class Round:
    """This class represents a chess round where matches is a list of match instances."""

    def __init__(self, name=None, date=None, matches=None, start_time=None, end_time=None):
        self._name = name
        self._date = date
        self._matches = matches
        self._start_time = start_time
        self._end_time = end_time

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        self._name = new_name

    @name.deleter
    def name(self):
        del self._name

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, new_date):
        self._date = new_date

    @date.deleter
    def date(self):
        del self._date

    @property
    def matches(self):
        return self._matches

    @matches.setter
    def matches(self, new_matches):
        self._matches = new_matches

    @matches.deleter
    def matches(self):
        del self._matches

    @property
    def start_time(self):
        return self._start_time

    @start_time.setter
    def start_time(self, new_start_time):
        self._start_time = new_start_time

    @start_time.deleter
    def start_time(self):
        del self._start_time

    @property
    def end_time(self):
        return self._end_time

    @end_time.setter
    def end_time(self, new_end_time):
        self._end_time = new_end_time

    @end_time.deleter
    def end_time(self):
        del self._end_time

    def initialize_matches(self, pairs):
        """Initialize a match with score = 0 for each player."""

        matches = []
        for pair in pairs:
            _match = match.Match(pair[0], 0, pair[1], 0)
            matches.append(_match)
        self._matches = matches

    def update_round(self, updated_matches):
        """Conventions: update only the last round."""

        self._matches = updated_matches

    def get_serialized_attributes(self):
        """Serialize all attributes of a chess round instance in order to save them in a document oriented database
        (TinyDB).

        It must serialize the list of matches (list of match instances).
        """

        attributes_info = basic_backend.get_attributes(self)
        new_dict = copy.deepcopy(attributes_info)
        # This part is added used for the serialization with TinyDB
        for index, _match in enumerate(attributes_info["matches"]):
            serialized_match = _match.get_serialized_attributes()
            new_dict["matches"][index] = serialized_match
        return new_dict

    def get_attributes(self):
        """Get names of attributes (without protected or private sign) and theirs values."""

        attributes_info = basic_backend.get_attributes(self)
        return attributes_info

    @classmethod
    def get_deserialized_round(cls, serialized_attributes_values):
        """Rebuilt a chess round object from serialized attributes-values
        (e.g. from TinyDB).
        """

        # Retrieve the class type
        obj_type = globals()[cls.__name__]

        for key in serialized_attributes_values.keys():
            if key == "matches":
                matches = serialized_attributes_values["matches"]
                for index, match_info in enumerate(matches):
                    deserialized_match = match.Match.get_deserialized_match(match_info)
                    # print("deserialized_match", deserialized_match)
                    matches[index] = deserialized_match
        _round = basic_backend.create_item(serialized_attributes_values, obj_type)
        return _round

    def set_attrs(self, kwargs):
        """Set values for all attributes via a dictionary."""

        basic_backend.set_attrs(self, kwargs)

    @staticmethod
    def get_attribute_names():
        """Get only names of attributes (without protected sign or private sign)."""

        _round = Round()
        return _round.get_attributes().keys()

    def __str__(self):
        """Print all attributes and theirs values for a round."""

        attr_str = basic_backend.get_str(self)
        return attr_str

    def __repr__(self):
        """Display the string representation of a round object."""

        if self._name is not None:
            return basic_backend.get_str(self)
            # return self._name + "at " + self.start_time
        return str(None)
