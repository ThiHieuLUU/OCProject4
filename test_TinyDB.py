# from tinydb import TinyDB
from tinydb import TinyDB, Query
import player
# import player_list
import tournament
import match
import chess_round
import location

db = TinyDB('db.json', encoding="utf-8", ensure_ascii=False)
players_table = db.table('players')
tournaments_table = db.table('tournaments', cache_size=30)
matches_table = db.table('matches', cache_size=30)
rounds_table = db.table('rounds', cache_size=30)


p8 = player.Player("Abraham", "Adnet", "12/01/2021", "M", 970)
p1 = player.Player("Lucrèce", "Besnard", "12/02/2021", "M", 1070)
p3 = player.Player("Frédéric", "Colbert", "06/01/2021", "M", 870)
p = [p1, p3, p8]

m = match.Match(player1=p1, score1=1, player2=p8, score2=0)
m1 = match.Match(player1=p3, score1=1, player2=p8, score2=0)
m2 = match.Match(player1=p1, score1=0.5, player2=p3, score2=0.5)

r1 = chess_round.Round(name="Round 1", date="01/02/2018", matches=[m, m1])
r2 = chess_round.Round(name="Round 2", date="01/03/2018", matches=[m, m2])
r3 = chess_round.Round(name="Round 3", date="01/04/2018", matches=[m1, m2])
r = [r1, r2, r3]
# print(r)


_location = location.Location(building_number=10, street="Rue de Fontenay", city="Paris", zipcode=75015)
t1 = tournament.Tournament(name="T1", location=_location, date="01/02/2021", players=p)
t2 = tournament.Tournament(name="T2", location=_location, date="02/02/2021", number_of_rounds=5, players=p)
t3 = tournament.Tournament(name="T3", location=_location, date="06/02/2021", players=p)
t4 = tournament.Tournament(name="T4", location=_location, date="08/02/2021", players=p)
t5 = tournament.Tournament(name="T5", location=_location, date="28/02/2021", players=p)
t5.rounds = r

t = [t1, t2, t3, t4, t5]

# input()
# m = (1, 2)

players_table.truncate()  # clear the table first
matches_table.truncate()
rounds_table.truncate()
tournaments_table.truncate()  # clear the table first

p8 = player.Player("Abraham", "Adnet", "12/01/2021", "M", 970)

players = player.players


def serialize_item(_item):
    if _item.__class__.__name__ in ["Match", "Round", "Tournament"]:
    # if _item.__class__.__name__ in ["Match"]:
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


def upsert_player(table, item, cdn):
    table.upsert(item, cdn.first_name == item["first_name"]
                 and cdn.last_name == item["last_name"]
                 and cdn.date_of_birth == item["date_of_birth"])


def upsert_tournament(table, item, cdn):
    # print(cdn.date)
    # print(item["date"])
    table.upsert(item, cdn.name == item["name"]
                 and cdn.date == item["date"])
    # and cdn.time_control == item["time_control"])

def upsert_round(table, item, cdn):
    table.upsert(item, cdn.name == item["name"]
                 and cdn.date == item["date"])

def upsert_match(table, item, cdn):
    # compare players in a match
    table.upsert(item, cdn.match[0][0] == item["match"][0][0]
                 and cdn.match[1][0] == item["match"][1][0])


def upsert_multiple(table, items, cdn, upsert_fct):
    for item in items:
        upsert_fct(table, item, cdn)


p8_info = serialize_item(p8)
print(p8_info)

fct = player.Player.create_player
p8_bis = deserialize_item(p8_info, fct)
print(type(p8_bis))
print(p8_bis)

serialized_items = serialize_items(players)
# players_table.insert_multiple(serialized_items)
cdn = Query()
# cdn.first_name == item["first_name"] and cdn.last_name == item["last_name"] and and cdn.date_of_birth == item["date_of_birth"]

fct = upsert_player
upsert_multiple(players_table, serialized_items, cdn, fct)
for row in players_table:
    print(row)

print("=" * 10)

db_serialized_items = players_table.all()
print(db_serialized_items)
fct = player.Player.create_player
deserialized_items = deserialize_items(db_serialized_items, fct)
for _item in deserialized_items:
    print("*" * 5)
    print(_item)
    print("*" * 5)

# insert(players_table, p8_info)
cdn = Query()
upsert_player(players_table, p8_info, cdn)
upsert_player(players_table, p8_info, cdn)
p8_bis.elo_rating = 500
print(p8_bis)
p8_info = serialize_item(p8_bis)
print(p8_info)
upsert_player(players_table, p8_info, cdn)


serialized_m = serialize_item(m)
print(serialized_m)
fct = upsert_match
upsert_match(matches_table, serialized_m, cdn)

serialized_m = serialize_item(m2)
print(serialized_m)
# input("Stop at serialized_m")
fct = upsert_match
upsert_match(matches_table, serialized_m, cdn)

# insert(matches_table, serialized_m)
print("In db")
for row in matches_table:
    print(row)
# input("Stop at matches")

db_serialized_items = matches_table.all()
print(db_serialized_items)
# input()

# fct = match.Match.create_match
fct = match.Match.get_deserialized_match
deserialized_items = deserialize_items(db_serialized_items, fct)
print(deserialized_items)
print("="*10)
for _item in deserialized_items:
    # print("*" * 5)
    print(_item)
    # print("*" * 5)

# print(m)

# serialized_r = serialize_item(r1)
# print("==============")
# print(serialized_r)
# upsert_round(rounds_table, serialized_r, cdn)
#
#
serialized_r = serialize_items(r)
fct = upsert_match
fct = upsert_round
upsert_multiple(rounds_table, serialized_r, cdn, fct)
db_serialized_items = rounds_table.all()
for item in db_serialized_items:
    for _match in item['matches']:
        print(_match)


# fct = chess_round.Round.create_round
fct = chess_round.Round.get_deserialized_round
deserialized_items = deserialize_items(db_serialized_items, fct)
print(deserialized_items)
print("="*10)
for _item in deserialized_items:
    # print("*" * 5)
    print(_item)
    # print("*" * 5)

# input()

cdn = Query()
serialized_tournament = serialize_item(t5)
# print(serialized_tournament)

serialized_tournaments = serialize_items(t)
print(serialized_tournaments)
for t in serialized_tournaments:
    print(t)

fct = upsert_tournament
upsert_multiple(tournaments_table, serialized_tournaments, cdn, fct)
# insert_multiple(tournaments_table, serialized_tournaments)
#
db_serialized_items = tournaments_table.all()
for item in db_serialized_items:
    print("*" * 10)
    print(item)
    print("*" * 10)
fct = tournament.Tournament.get_deserialized_tournament
deserialized_items = deserialize_items(db_serialized_items, fct)
for t in deserialized_items:
    print("*" * 5)
    # print("t.rounds", t.rounds)
    print(type(t.location))
    # input()
    # print(t.rounds[0])
    if (len(t.players)) > 0:
        print(type(t.players[0]))
    if (len(t.rounds)) > 0:
        print(type(t.rounds[0]))
    print("*" * 5)
