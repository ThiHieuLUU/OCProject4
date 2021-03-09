"""This module is used to do some general tasks for a class:

- create an object from a given dictionary (it's useful and automatically when deserialization process is called).

- get all attributes and theirs values to put in a dictionary (all attributes' names are automatically retrieved. It
is not the same as the __getattribute__ (built-in method) where the attribute's name must be known and given and this
gives only one attribute's value.).

- set attributes from a given dictionary (each attribute's name is automatically compared with the keys of the
dictionary. If this comparison is true, value of the corresponding key will be set to one of attributes. It's useful for
deserialization of an object. It is not the same as the __setattr__ (built-in method) where the attribute's name must be
known and this sets value for only one attribute).

- print an object of the class: concatenating all attributes and theirs' values by an given string pattern.
(otherwise, repr method is not implemented here, it is customised in each class).
"""


def create_item(cls, attributes_values):
    """Create an object of class 'cls' from a dictionary with its keys are attribute names of the class cls."""

    # create a new class
    item = cls()
    item.set_attrs(attributes_values)
    return item


def get_attributes(cls):
    """Get names of attributes (without protected or private sign) and theirs values."""

    attributes_info = dict()

    protected_sign = "_"
    private_sign = "_" + type(cls).__name__ + "__"

    for attribute_name, attribute_value in zip(cls.__dict__, cls.__dict__.values()):
        # In case of protected or private attribute, retrieve only name without underscore at the beginning of name.
        if attribute_name.startswith(private_sign):
            attribute_name = attribute_name[len(private_sign):]
        elif attribute_name.startswith(protected_sign):
            attribute_name = attribute_name[1:]

        attributes_info[attribute_name] = attribute_value
    return attributes_info


def set_attrs(cls, kwargs):
    """Set value for attributes of an object via a dictionary."""

    for key, value in kwargs.items():
        setattr(cls, key, value)


def get_str(cls):
    """Print all attributes and theirs values of an object."""

    attr_info = cls.get_attributes()
    attr_str = ""

    for attr_name, attr_value in attr_info.items():
        attr_str += str(attr_name).capitalize() + ': ' + str(attr_value) + "\n"

    return attr_str
