"""docstring"""

import datetime
import mvc_exceptions as mvc_exc


#     def get_attribute_names
#     'save data in BDD
#     def update_matches
# }

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
        if isinstance(new_name, str):
            self._name = new_name
        else:
            raise mvc_exc.UnexpectedString(f'Input "{new_name}" does not meet expectations')

    @name.deleter
    def name(self):
        del self._name

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, new_date):
        date_format = "%d-%m-%Y"
        if datetime.datetime.strptime(str(new_date), date_format):
            print("This is the correct date string date_format.")
            self._date = new_date
        else:
            raise mvc_exc.DateError('Incorrect date date_format. It should be DD-MM-YYYY')

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
        attr_names = []

        protected_sign = "_"
        private_sign = "_" + type(self).__name__ + "__"

        for attribute_name in self.__dict__:
            # in case of protected or private attribute, retrieve only true name of attribute
            if attribute_name.startswith(private_sign):
                attribute_name = attribute_name[len(private_sign):]
            elif attribute_name.startswith(protected_sign):
                attribute_name = attribute_name[1:]

            attr_names.append(attribute_name)
        return attr_names, list(self.__dict__.values())

    def __str__(self):
        """Print all attributes and theirs values of an object"""
        attr_names, attr_values = self.get_attributes()
        attr_str = ""

        for attr_name, attr_value in zip(attr_names, attr_values):
            attr_str += str(attr_name).capitalize() + ': ' + str(attr_value) + "\n"

        return attr_str

    def __repr__(self):
        return f"Round {type(self).count}"


if __name__ == '__main__':
    r = Round("round 0")
    print(r)
    r.name = "round 1"
    r.start_time = "10"
    r.end_time = "10"
    r.matches = [(["a", 1], ["b", 2])]  # Problem

    n_r = r
    print(n_r.matches)
    m = r.matches

    print(r.matches)
    m[0][0][0] = "c"
    print(m)
    print(r.matches)
    dct = {r: "a"}
    print(dct.keys().__getattribute__)

    # print(r)
