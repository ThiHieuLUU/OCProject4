"""docstring"""


class Player:
    """docstring"""

    def __init__(self, fide_id=None, first_name=None, last_name=None, date_of_birth=None, gender=None, elo_rating=None):
        self._fide_id = fide_id
        self._first_name = first_name
        self._last_name = last_name
        self._date_of_birth = date_of_birth
        self._gender = gender
        self._elo_rating = elo_rating

    def __hash__(self):
        return hash((self._fide_id, self._first_name, self._last_name))  # tuple hash

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return (self._fide_id, self._first_name, self._last_name, self._date_of_birth, self._gender) \
               == (other.fide_id, other.first_name, other.last_name, other.date_of_birth, other.gender)
        return False

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
    def elo_rating(self):
        return self._elo_rating

    @elo_rating.setter
    def elo_rating(self, new_elo_rating):
        self._elo_rating = new_elo_rating

    @elo_rating.deleter
    def elo_rating(self):
        del self._elo_rating

    def get_attributes(self):
        """Get attribute names (without protected or private sign) and theirs values """
        attributes_info = dict()

        protected_sign = "_"
        private_sign = "_" + type(self).__name__ + "__"

        for attribute_name, attribute_value in zip(self.__dict__, self.__dict__.values()):
            # in case of protected or private attribute, retrieve only true name of attribute
            if attribute_name.startswith(private_sign):
                attribute_name = attribute_name[len(private_sign):]
            elif attribute_name.startswith(protected_sign):
                attribute_name = attribute_name[1:]

            attributes_info[attribute_name] = attribute_value
        return attributes_info

    def set_attrs(self, kwargs):
        for k, v in kwargs.items():
            # print(f"k = {k}, v = {v}")
            setattr(self, k, v)

    def __str__(self):
        """Print all attributes and theirs values of an object"""
        attr_info = self.get_attributes()
        attr_str = ""

        for attr_name, attr_value in attr_info.items():
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
