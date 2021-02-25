"""docstring"""
import basic_backend


class Player:
    """docstring"""

    def __init__(self, player_id=None, first_name=None, last_name=None, date_of_birth=None, gender=None,
                 elo_rating=None):
        self._player_id = player_id
        self._first_name = first_name
        self._last_name = last_name
        self._date_of_birth = date_of_birth
        self._gender = gender
        self._elo_rating = elo_rating
    #
    # def __init__(self):
    #     self._player_id = None
    #     self._first_name = None
    #     self._last_name = None
    #     self._date_of_birth = None
    #     self._gender = None
    #     self._elo_rating = None

    def __hash__(self):
        return hash((self._player_id, self._first_name, self._last_name))  # tuple hash

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return (self._player_id, self._first_name, self._last_name, self._date_of_birth, self._gender) \
                   == (other.player_id, other.first_name, other.last_name, other.date_of_birth, other.gender)
        return False

    @property
    def player_id(self):
        return self._player_id

    @player_id.setter
    def player_id(self, new_player_id):
        self._player_id = new_player_id

    @player_id.deleter
    def player_id(self):
        del self._player_id

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
        attributes_info = basic_backend.get_attributes(self)
        return attributes_info

    def set_attrs(self, kwargs):
        basic_backend.set_attrs(self, kwargs)

    @classmethod
    def create_player(cls, attributes_values):
        # Retrieve the class type
        obj_type = globals()[cls.__name__]
        return basic_backend.create_item(attributes_values, obj_type)

    @classmethod
    def add_player(cls, players, player):
        return basic_backend.add_item(players, player)

    @classmethod
    def find_player(cls, players, key, value):
        return basic_backend.find_item(players, key, value)

    @classmethod
    def read_player(cls, players, key, value):
        return basic_backend.read_item(players, key, value)

    @classmethod
    def update_player(cls, players, key, value, attributes_new_values):
        return basic_backend.update_item(players, key, value, attributes_new_values)

    @classmethod
    def delete_player(cls, players, key, value):
        return basic_backend.delete_item(players, key, value)

    def __str__(self):
        """Print all attributes and theirs values of an object"""
        attr_str = basic_backend.get_str(self)
        return attr_str

    def __repr__(self):
        if self._player_id is not None:
            return self._first_name + " " + self._last_name + " - ID " + str(self._player_id)
        else:
            return str(None)

if __name__ == '__main__':
    # klass = globals()["Player"]
    p = Player(123, "Maxim", "Drague")
    print(p)

    # print(klass)
    # p = klass()
    # print(p)
