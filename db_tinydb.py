"""
This module is used to serialize or deserialize an object/item.

 STEPS:
 For an item:
    1. Serialize item (call serialize_item(item)
    2. Define the function for deserializing:
    (player : create_player, location: create_location, others: get_deserialized_round/match/tournament)

 For many items:
    1. Serialize items: serialize_items(items)
    2. Save in TinyDB
    - upsert_fct : call corresponding function, e.g. for player, call 'upsert_player'
    - call : upsert_multiple(table, serialized_items, cdn, upsert_fct)
    3. Deserialization:
    Example for players:
    - db_serialized_items = players_table.all()
    - deserialized_items = deserialize_items(db_serialized_items, deserialize_fct)

"""

from tinydb import Query
import player
import tournament
import match
import chess_round

# Deserialization functions which will be called in deserialize_item or deserialize_items methods.
player_fct = player.Player.create_player
match_fct = match.Match.get_deserialized_match
round_fct = chess_round.Round.get_deserialized_round
tournament_fct = tournament.Tournament.get_deserialized_tournament


def serialize_item(_item):
    """Serialize an object/item."""

    return _item.get_serialized_attributes()


def serialize_items(_items):
    """Serialize many objects/items."""

    serialized_items = [serialize_item(_item) for _item in _items]
    return serialized_items


def deserialize_item(serialized_item, fct):
    """Deserialize an object/item."""

    return fct(serialized_item)


def deserialize_items(serialized_items, fct):
    """Deserialize many objects/items."""

    deserialized_items = [deserialize_item(_item, fct) for _item in serialized_items]
    return deserialized_items


def upsert_player(table, item):
    """Insert (if not exist) or update (if exist) a player in a selected table of the database."""

    condition = Query()
    table.upsert(item, condition.first_name == item["first_name"]
                 and condition.last_name == item["last_name"]
                 and condition.date_of_birth == item["date_of_birth"])


def upsert_tournament(table, item):
    """Insert (if not exist) or update (if exist) a tournament in a selected table of the database."""

    condition = Query()
    table.upsert(item, condition.name == item["name"]
                 and condition.date == item["date"])


def upsert_round(table, item):
    """Insert (if not exist) or update (if exist) a round in a selected table of the database."""

    condition = Query()
    table.upsert(item, condition.name == item["name"]
                 and condition.date == item["date"])


def upsert_match(table, item):
    """Insert (if not exist) or update (if exist) a match in a selected table of the database."""

    condition = Query()
    # compare players in a match
    table.upsert(item, condition.match[0][0] == item["match"][0][0]
                 and condition.match[1][0] == item["match"][1][0])


def upsert_multiple(table, items, upsert_fct):
    """Insert (if not exist) or update (if exist) many objects/items in a selected table of the database."""

    for item in items:
        upsert_fct(table, item)
