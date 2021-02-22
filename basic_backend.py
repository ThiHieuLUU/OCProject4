import mvc_exceptions as mvc_exc


def create_item(attributes_values, obj_type):
    # create a new object
    item = obj_type()
    item.set_attrs(attributes_values)
    return item


def add_item(items, item):
    if item in items:
        raise mvc_exc.ItemAlreadyExisted(f'{item} already existed!')
    else:
        items.append(item)
    return items


def find_item(items, key, value):
    items_info = [item.get_attributes() for item in items]
    my_item_indexes = next((i for i, item in enumerate(items_info) if item[key] == value), None)
    if my_item_indexes is not None:
        return items[my_item_indexes]
    else:
        raise mvc_exc.ItemNotFound(f'{item} not found!')
    return None


def read_item(items, key, value):
    item = find_item(items, key, value)
    if item is not None:
        return item
    else:
        raise mvc_exc.ItemNotExisted(f'Can not read item with {key} = {value} because it\'s not existed')


def read_items(items):
    return [item for item in items]


def update_item(items, key, value, attributes_new_values):
    item = find_item(items, key, value)
    if item is not None:
        item.set_attrs(attributes_new_values)
    else:
        raise mvc_exc.ItemNotExisted(f'Can not update item with {key} = {value} because it\'s not existed')


def delete_item(items, key, value):
    item = find_item(items, key, value)
    if item is not None:
        items.remove(item)
    else:
        raise mvc_exc.ItemNotExisted(f'Can not delete item with {key} = {value} because it\'s not existed')


def get_attributes(obj):
    """Get attribute names (without protected or private sign) and theirs values """
    attributes_info = dict()

    protected_sign = "_"
    private_sign = "_" + type(obj).__name__ + "__"

    for attribute_name, attribute_value in zip(obj.__dict__, obj.__dict__.values()):
        # in case of protected or private attribute, retrieve only true name of attribute
        if attribute_name.startswith(private_sign):
            attribute_name = attribute_name[len(private_sign):]
        elif attribute_name.startswith(protected_sign):
            attribute_name = attribute_name[1:]

        attributes_info[attribute_name] = attribute_value
    return attributes_info


def set_attrs(obj, kwargs):
    for k, v in kwargs.items():
        setattr(obj, k, v)


def get_str(obj):
    """Print all attributes and theirs values of an obj"""
    attr_info = obj.get_attributes()
    attr_str = ""

    for attr_name, attr_value in attr_info.items():
        attr_str += str(attr_name).capitalize() + ': ' + str(attr_value) + "\n"

    return attr_str
