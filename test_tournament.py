import tournament
tournaments = []
t1 = tournament.Tournament()
t2 = tournament.Tournament()
tournaments.append((t1))
tournaments.append((t2))
t1.name = "T1"
t2.name = "T2"
print(tournaments)
attributes_values = {"name": "T3",
"location": "a",
"date": "25/07/2015",
"description": "qrezt"}

t = tournament.Tournament.create_tournament(attributes_values)
print(t)
print(t.get_attributes())

attributes_values = {"name": "T3",
"location": "b",
"date": "26/07/2015",
"description": "qrezt"}

print(t.set_attrs(attributes_values))
print(t)
tournament.Tournament.add_tournament(tournaments, t)
print(tournaments)
res = tournament.Tournament.find_tournament(tournaments, key="name", value="T2")
print("response of finding\n", res)
res = tournament.Tournament.read_tournament(tournaments, key="name", value="T3")
print("response of finding\n", res)
# res = tournament.Tournament.read_tournament(tournaments, key="name", value="T0")
# print("response of finding\n", res)

attributes_values = {"name": "T1",
"location": "bqsdg",
"date": "20/07/2015",
"description": "qrezt"}
print("before updating \n", tournaments)

tournament.Tournament.update_tournament(tournaments, "name", "T1", attributes_values)
print(tournaments)
res = tournament.Tournament.delete_tournament(tournaments, key="name", value="T1")
print("after of deleting \n ", tournaments)
print("*"*10)



# print("*"*10)
# print(p)
# print(tournaments)
# print(p.set_attrs(attributes_values))
# print(p)