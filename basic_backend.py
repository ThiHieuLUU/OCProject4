import mvc_exceptions as mvc_exc


# import player
#
# # from player import Player as obj_type
# obj_type = player.Player

# items = list()


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
    # global items
    items_info = [item.get_attributes() for item in items]
    # print(items_info)
    my_item_indexes = next((i for i, item in enumerate(items_info) if item[key] == value), None)
    if my_item_indexes is not None:
        # print(items[my_item_indexes])
        return items[my_item_indexes]
    else:
        print("Not found")
    return None


def read_item(items, key, value):
    item = find_item(items, key, value)
    if item is not None:
        return item
    else:
        print(f"Can not read because {item} does not exist")
        raise mvc_exc.ItemNotExisted(f'Can\'t read {key} = {value} because it\'s not existed')


def read_items(items):
    return [item for item in items]


def update_item(items, key, value, attributes_new_values):
    item = find_item(items, key, value)
    if item is not None:
        item.set_attrs(attributes_new_values)
    else:
        print("Can not update")


def delete_item(items, key, value):
    item = find_item(items, key, value)
    if item is not None:
        items.remove(item)
    else:
        print("Can not delete")
    # del item


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


if __name__ == '__main__':
    p1 = obj_type(234, "Lucrèce", "Besnard", "12/02/2021", "M", 1070)
    p2 = obj_type(172, "Alexis", "Marchant", "18/01/2021", "M", 670)
    p3 = obj_type(896, "Gaël", "Charpentier", "12/02/2021", "M", 470)
    p4 = obj_type(742, "Marius", "Bouhier", "09/01/2021", "M", 1250)
    p5 = obj_type(666, "Jean-François", "Duchemin", "02/01/2021", "M", 570)
    p6 = obj_type(957, "Frédéric", "Colbert", "06/01/2021", "M", 870)
    p7 = obj_type(482, "Gaëtan", "Trintignant", "27/01/2021", "M", 770)
    p8 = obj_type(976, "Abraham", "Adnet", "12/01/2021", "M", 970)
    p9 = obj_type(348, "Nicolas", "Desmarais", "05/01/2021", "M", 1170)
    p10 = obj_type(523, " Claude", "Brassard", "03/01/2021", "M", 1470)

    attributes_values = {"fide_id": 234,
                         "first_name": "a",
                         "last_name": "b",
                         "date_of_birth": "12/02/2021",
                         "gender": "F",
                         "elo_rating": 2020}

    create_item(attributes_values, obj_type)
    print(items)
    find_item("first_name", "a")

    attributes_values = {"fide_id": 244,
                         "first_name": "c",
                         "last_name": "d",
                         "date_of_birth": "12/02/2021",
                         "gender": "F",
                         "elo_rating": 2020}

    create_item(attributes_values, obj_type)
    update_item("first_name", "c", attributes_values)
    print(items)

    print("before deleting")
    print(items)
    delete_item("first_name", "a")
    print("after deleting")
    print(items)
