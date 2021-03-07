"""This module is used to do the general tasks for a class:
- create an object from a given dictionary.
- get all attributes and theirs values to put in a dictionary.
- set attributes from a given dictionary.
- print /repr an object of the class.
(the dictionary's keys are attribute names of the class).
"""


def create_item(attributes_values, cls):
    """Create an object of class 'cls' from a dictionary with its keys are attribute names of the class cls."""

    # create a new object
    item = cls()
    item.set_attrs(attributes_values)
    return item


def get_attributes(obj):
    """Get names of attributes (without protected or private sign) and theirs values."""

    attributes_info = dict()

    protected_sign = "_"
    private_sign = "_" + type(obj).__name__ + "__"

    for attribute_name, attribute_value in zip(obj.__dict__, obj.__dict__.values()):
        # In case of protected or private attribute, retrieve only name without underscore at the beginning of name.
        if attribute_name.startswith(private_sign):
            attribute_name = attribute_name[len(private_sign):]
        elif attribute_name.startswith(protected_sign):
            attribute_name = attribute_name[1:]

        attributes_info[attribute_name] = attribute_value
    return attributes_info


def set_attrs(obj, kwargs):
    """Set value for attributes of an object via a dictionary."""

    for key, value in kwargs.items():
        setattr(obj, key, value)


def get_str(obj):
    """Print all attributes and theirs values of an object."""

    attr_info = obj.get_attributes()
    attr_str = ""

    for attr_name, attr_value in attr_info.items():
        attr_str += str(attr_name).capitalize() + ': ' + str(attr_value) + "\n"

    return attr_str
