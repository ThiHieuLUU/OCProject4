class Location:
    def __init__(self, building_number=None, street=None, city=None, zipcode=None):
        self._building_number = building_number
        self._street = street
        self._city = city
        self._zipcode = zipcode

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

        return "\n" + attr_str

    def __repr__(self):
        """Print all attributes and theirs values of an object"""
        attr_names, attr_values = self.get_attributes()
        attr_str = ""

        for attr_name, attr_value in zip(attr_names, attr_values):
            attr_str += str(attr_name).capitalize() + ': ' + str(attr_value) + "\n"

        return attr_str


if __name__ == '__main__':
    l = Location(10)
    del l.building_number
    print(l)
