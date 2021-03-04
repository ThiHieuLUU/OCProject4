from tinydb import TinyDB, Query
import player
import tournament
import match
import chess_round
import location

db = TinyDB('db.json', encoding="utf-8", ensure_ascii=False)
actors_table = db.table('actors', cache_size=30)
tournaments_table = db.table('tournaments', cache_size=30)

# players_table = db.table('players', cache_size=30)
# matches_table = db.table('matches', cache_size=30)
# rounds_table = db.table('rounds', cache_size=30)

# actors_table.truncate()
# tournaments_table.truncate()  # clear the table first

# players_table.truncate()  # clear the table first
# matches_table.truncate()
# rounds_table.truncate()

cdn = Query()
# Deserialization function
player_fct = player.Player.create_player
match_fct = match.Match.get_deserialized_match
round_fct = chess_round.Round.get_deserialized_round
tournament_fct = tournament.Tournament.get_deserialized_tournament

def serialize_item(_item):
    # Player is not composed class
    if _item.__class__.__name__ in ["Match", "Round", "Tournament"]:
        return _item.get_serialized_attributes()
    else:
        return _item.get_attributes()


def serialize_items(_items):
    serialized_items = [serialize_item(_item) for _item in _items]
    return serialized_items


def deserialize_item(serialized_item, fct):
    # return player.Player.create_item(serialized_item)
    return fct(serialized_item)


def deserialize_items(serialized_items, fct):
    deserialized_items = [deserialize_item(_item, fct) for _item in serialized_items]
    return deserialized_items


def insert(table, item):
    table.insert(item)


def insert_multiple(table, items):
    table.insert_multiple(items)


def upsert_player(table, item):
    global cdn
    table.upsert(item, cdn.first_name == item["first_name"]
                 and cdn.last_name == item["last_name"]
                 and cdn.date_of_birth == item["date_of_birth"])


def upsert_tournament(table, item):
    global cdn
    table.upsert(item, cdn.name == item["name"]
                 and cdn.date == item["date"])
    # and cdn.time_control == item["time_control"])

def upsert_round(table, item):
    global cdn
    table.upsert(item, cdn.name == item["name"]
                 and cdn.date == item["date"])

def upsert_match(table, item):
    global cdn
    # compare players in a match
    table.upsert(item, cdn.match[0][0] == item["match"][0][0]
                 and cdn.match[1][0] == item["match"][1][0])


def upsert_multiple(table, items, upsert_fct):
    # global cdn
    for item in items:
        upsert_fct(table, item)
"""
 STEPS:
 For a item
 1. Serialize item (call serialize_item(item)
 2. Define function de deserialize
  (player : create_player, location: create_location, others: get_deserialized_round/match/tournament)
  
  For many items:
  1. serialize_items(items)
  2. Save in TinyDB
  - upsert_fct : fct = upsert_player
  - call : upsert_multiple(players_table, serialized_items, cdn, fct)
  3. Deserialization:
  - db_serialized_items = players_table.all()
  - deserialized_items = deserialize_items(db_serialized_items, deserialize_fct)
  
"""

