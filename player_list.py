import player
p1 = player.Player(234, "Lucrèce", "Besnard", "12/02/2021", "M", 1070)
p2 = player.Player(172, "Alexis", "Marchant", "18/01/2021", "M", 670)
p3 = player.Player(896, "Gaël", "Charpentier", "12/02/2021", "M", 470)
p4 = player.Player(742, "Marius", "Bouhier", "09/01/2021", "M", 1250)
p5 = player.Player(666, "Jean-François", "Duchemin", "02/01/2021", "M", 570)
p6 = player.Player(957, "Frédéric", "Colbert", "06/01/2021", "M", 870)
p7 = player.Player(482, "Gaëtan", "Trintignant", "27/01/2021", "M", 770)
p8 = player.Player(976, "Abraham", "Adnet", "12/01/2021", "M", 970)
p9 = player.Player(348, "Nicolas", "Desmarais", "05/01/2021", "M", 1170)
p10 = player.Player(523, " Claude", "Brassard", "03/01/2021", "M", 1470)
p11 = player.Player(234, "Lucrèce", "Besnard", "12/02/2021", "M", 1090)

# players = [p1, p2, p3, p4, p5, p6, p7, p8, p9]
players = [p1, p2, p3, p4, p5, p6, p7, p8]

# p = player.Player(976, "Abraham", "Adnet", "12/01/2021", "M", 970)
#
# attributes_values = {"fide_id": 234,
# "first_name": "a",
# "last_name": "b",
# "date_of_birth": None,
# "gender": None,
# "elo_rating": None}
#
#
# print("*"*10)
# print(p)
# print(players)
# print(p.get_attributes())
# print(p.set_attrs(attributes_values))
# print(p)
# new_p = player.Player.create_player(attributes_values)
# print(new_p)
# # players.append(new_p)
# print(players)
# new_players = player.Player.add_player(players, new_p)
# # print(new_players)
# res = player.Player.find_player(players, key="first_name", value="a")
# print("response of finding", res)
# res = player.Player.read_player(players, key="last_name", value="Besnard")
# print("response of finding", res)
#
# attributes_values = {"fide_id": 234,
# "first_name": "a",
# "last_name": "b",
# "date_of_birth": "22/09/2018",
# "gender": "F",
# "elo_rating": 1890}
#
# player.Player.update_player(players, "first_name", "a", attributes_values)
# print(players)
# res = player.Player.delete_player(players, key="first_name", value="a")
# print("after of deleting \n ", players)
# print("*"*10)
