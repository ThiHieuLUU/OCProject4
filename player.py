"""docstring"""


class Player:
    """docstring"""

    def __init__(self, fide_id=None, first_name=None, last_name=None, date_of_birth=None, gender=None, ranking=None):
        self._fide_id = fide_id
        self._first_name = first_name
        self._last_name = last_name
        self._date_of_birth = date_of_birth
        self._gender = gender
        self._ranking = ranking

    def __hash__(self):
        return hash((self._fide_id, self._first_name, self._last_name)) # tuple hash

    def __eq__(self, other):
        return (self._fide_id, self._first_name, self._last_name) == (other.fide_id, other.first_name,
                                                                      other.last_name)

    @property
    def fide_id(self):
        return self._fide_id

    @fide_id.setter
    def fide_id(self, new_fide_id):
        self._fide_id = new_fide_id

    @fide_id.deleter
    def fide_id(self):
        del self._fide_id

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
    def ranking(self):
        return self._ranking

    @ranking.setter
    def ranking(self, new_ranking):
        self._ranking = new_ranking

    @ranking.deleter
    def ranking(self):
        del self._ranking

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
        if self._fide_id is not None:
            return self._first_name + " " + self._last_name + " - ID " + str(self._fide_id)
        else:
            return str(None)


if __name__ == '__main__':
    p = Player(123, "Maxim", "Drague")
    print(p)
