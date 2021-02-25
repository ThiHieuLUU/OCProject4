import basic_backend


class Location:
    def __init__(self):
        self._building_number = None
        self._street = None
        self._city = None
        self._zipcode = None

    @property
    def building_number(self):
        return self._building_number

    @building_number.setter
    def building_number(self, building_number):
        self._building_number = building_number

    @building_number.deleter
    def building_number(self):
        del self._building_number

    @property
    def street(self):
        return self._street

    @street.setter
    def street(self, street):
        self._street = street

    @street.deleter
    def street(self):
        del self._street

    @property
    def city(self):
        return self._city

    @city.setter
    def city(self, city):
        self._city = city

    @city.deleter
    def city(self):
        del self._city

    @property
    def zipcode(self):
        return self._zipcode

    @zipcode.setter
    def zipcode(self, zipcode):
        self._zipcode = zipcode

    @zipcode.deleter
    def zipcode(self):
        del self._zipcode

    def get_attributes(self):
        """Get attribute names (without protected or private sign) and theirs values """
        attributes_info = basic_backend.get_attributes(self)
        return attributes_info

    def set_attrs(self, kwargs):
        basic_backend.set_attrs(self, kwargs)

    @classmethod
    def create_location(cls, attributes_values):
        # Retrieve the class type
        obj_type = globals()[cls.__name__]
        return basic_backend.create_item(attributes_values, obj_type)

    @classmethod
    def add_location(cls, locations, location):
        return basic_backend.add_item(locations, location)

    @classmethod
    def find_location(cls, locations, key, value):
        return basic_backend.find_item(locations, key, value)

    @classmethod
    def read_location(cls, locations, key, value):
        return basic_backend.read_item(locations, key, value)

    @classmethod
    def update_location(cls, locations, key, value, attributes_new_values):
        return basic_backend.update_item(locations, key, value, attributes_new_values)

    @classmethod
    def delete_location(cls, locations, key, value):
        return basic_backend.delete_item(locations, key, value)

    def __str__(self):
        """Print all attributes and theirs values of an object"""
        attr_str = basic_backend.get_str(self)
        return "\n" + attr_str

    def __repr__(self):
        """Print all attributes and theirs values of an object"""
        attr_names, attr_values = self.get_attributes()
        attr_str = ""

        for attr_name, attr_value in zip(attr_names, attr_values):
            attr_str += str(attr_name).capitalize() + ': ' + str(attr_value) + "\n"

        return attr_str
