import player

p1 = player.Player(234, "Lucrèce", "Besnard", "12/02/2021", "M", 17)
p2 = player.Player(172, "Alexis", "Marchant", "18/01/2021", "M", 37)
p3 = player.Player(896, "Gaël", "Charpentier", "12/02/2021", "M", 27)
p4 = player.Player(742, "Marius", "Bouhier", "09/01/2021", "M", 47)
p5 = player.Player(666, "Jean-François", "Duchemin", "02/01/2021", "M", 57)
p6 = player.Player(957, "Frédéric", "Colbert", "06/01/2021", "M", 87)
p7 = player.Player(482, "Gaëtan", "Trintignant", "27/01/2021", "M", 67)
p8 = player.Player(976, "Abraham", "Adnet", "12/01/2021", "M", 97)
p9 = player.Player(348, "Nicolas", "Desmarais", "05/01/2021", "M", 117)
p10 = player.Player(523, " Claude", "Brassard", "03/01/2021", "M", 107)

players = [p1, p2, p3, p4, p5, p6, p7, p8, p9]
# sorted_players = sorted(players, key=lambda p : p.ranking)
# for player in sorted_players:
#     print(player.ranking)
#
# score1 = input(f'Player: ID = {p1.fide_id}, Name = {p1.first_name + " " + p1.last_name}, score = ')
