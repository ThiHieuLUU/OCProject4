"""docstring"""

import basic_backend


class Round:
    """docstring"""
    count = 0

    def __init__(self, name=None, date=None, matches=None, start_time=None, end_time=None):
        self._name = name
        self._date = date
        self._matches = matches
        self._start_time = start_time
        self._end_time = end_time
        type(self).count += 1

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

    def get_attributes(self):
        """Get attribute names (without protected or private sign) and theirs values """
        attributes_info = basic_backend.get_attributes(self)
        return attributes_info

    def set_attrs(self, kwargs):
        basic_backend.set_attrs(self, kwargs)

    @staticmethod
    def get_attribute_names():
        t = Round()
        return t.get_attributes().keys()

    def __str__(self):
        """Print all attributes and theirs values of an object"""
        attr_str = basic_backend.get_str(self)
        return attr_str

    def __repr__(self):
        if self._name is not None:
            return self._name + "at " + self.start_time
        else:
            return str(None)

