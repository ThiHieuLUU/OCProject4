import mvc_exceptions as mvc_exc
import player
from player import Player as ClassType

items = list()


def create_item(attributes_values):
    global items
    item = ClassType()
    item.set_attrs(attributes_values)
    result = item in items
    if result:
        raise mvc_exc.ItemAlreadyExisted(f'{item} already existed!')
    else:
        items.append(item)


# def create_items(app_items):
#     global items
#     items = app_items

def find_item(key, value):
    global items
    items_info = [item.get_attributes() for item in items]
    print(items_info)
    my_item_indexes = next((i for i, item in enumerate(items_info) if item[key] == value), None)
    if my_item_indexes is not None:
        print(items[my_item_indexes])
        return items[my_item_indexes]
    else:
        print("Not found")
    return None


def read_item(key, value):
    global items
    items_info = [item.get_attributes() for item in items]
    my_item_indexes = next((i for i, item in enumerate(items_info) if item[key] == value), None)
    if my_item_indexes:
        return items[my_item_indexes[0]]
    else:
        raise mvc_exc.ItemNotExisted(f"Can't read {key}={value} because it's not existed")


def read_items():
    global items
    return [item for item in items]


def update_item(key, value, attributes_new_values):
    item = find_item(key, value)
    if item is not None:
        item.set_attrs(attributes_new_values)
    else:
        print("Can not update")


def delete_item(key, value):
    item = find_item(key, value)
    if item is not None:
        items.remove(item)
    else:
        print("Can not delete")
    # del item


if __name__ == '__main__':
    p1 = ClassType(234, "Lucrèce", "Besnard", "12/02/2021", "M", 1070)
    p2 = ClassType(172, "Alexis", "Marchant", "18/01/2021", "M", 670)
    p3 = ClassType(896, "Gaël", "Charpentier", "12/02/2021", "M", 470)
    p4 = ClassType(742, "Marius", "Bouhier", "09/01/2021", "M", 1250)
    p5 = ClassType(666, "Jean-François", "Duchemin", "02/01/2021", "M", 570)
    p6 = ClassType(957, "Frédéric", "Colbert", "06/01/2021", "M", 870)
    p7 = ClassType(482, "Gaëtan", "Trintignant", "27/01/2021", "M", 770)
    p8 = ClassType(976, "Abraham", "Adnet", "12/01/2021", "M", 970)
    p9 = ClassType(348, "Nicolas", "Desmarais", "05/01/2021", "M", 1170)
    p10 = ClassType(523, " Claude", "Brassard", "03/01/2021", "M", 1470)

    attributes_values = {"fide_id": 234,
                         "first_name": "a",
                         "last_name": "b",
                         "date_of_birth": "12/02/2021",
                         "gender": "F",
                         "elo_rating": 2020}

    create_item(attributes_values)
    print(items)
    find_item("first_name", "a")

    attributes_values = {"fide_id": 244,
                         "first_name": "c",
                         "last_name": "d",
                         "date_of_birth": "12/02/2021",
                         "gender": "F",
                         "elo_rating": 2020}

    create_item(attributes_values)
    update_item("first_name", "c", attributes_values)
    print(items)

    print("before deleting")
    print(items)
    delete_item("first_name", "a")
    print("after deleting")
    print(items)
