"""docstring"""

import tournament
import player
import chess_round
import location

tournaments = list()
players = list()

total_points = dict()
opponents = dict()
players_info = dict()


class Model:

    def __init__(self):
        self.tournament = tournament.Tournament()

    @staticmethod
    def build_location(building_number, street, city, zipcode):
        attributes_values = dict()
        attributes_values["building_number"] = building_number
        attributes_values["street"] = street
        attributes_values["city"] = city
        attributes_values["zipcode"] = zipcode
        return location.Location.create_location(attributes_values)

    @staticmethod
    def build_player(player_id, first_name, last_name, date_of_birth, gender, elo_rating):
        attributes_values = dict()
        attributes_values["player_id"] = player_id
        attributes_values["first_name"] = first_name
        attributes_values["last_name"] = last_name
        attributes_values["date_of_birth"] = date_of_birth
        attributes_values["gender"] = gender
        attributes_values["elo_rating"] = elo_rating
        return player.Player.create_player(attributes_values)

    @staticmethod
    def add_player(new_player):
        global players
        player.Player.add_player(players, new_player)

    def create_tournament(self, name, _location, date, number_of_rounds, player_list, time_control, description):
        attributes_values = dict()
        attributes_values["name"] = name
        attributes_values["location"] = _location
        attributes_values["date"] = date
        attributes_values["number_of_rounds"] = number_of_rounds
        attributes_values["players"] = player_list
        attributes_values["time_control"] = time_control
        attributes_values["description"] = description
        self.tournament = tournament.Tournament.create_tournament(attributes_values)

    def initialize_info(self):
        global total_points
        global opponents
        global players_info
        total_points = self.tournament.initialize_total_points()
        opponents = self.tournament.initialize_opponents()
        elo_ratings = self.tournament.get_elo_ratings()
        players_info = self.tournament.initialize_players_info(elo_ratings)

    def get_first_pairs(self):
        return self.tournament.make_pairs_first_round()

    def get_pairs(self, round_index):
        global total_points
        global opponents
        global players_info

        if round_index == 1:
            pairs = self.tournament.make_pairs_first_round()
        else:
            pairs = self.tournament.make_pairs(players_info)
        return pairs

    def make_new_round(self):
        round_index = len(self.tournament.rounds) + 1
        if round_index <= self.tournament.number_of_rounds:
            _round = chess_round.Round()
            _round.name = "Round " + str(round_index)
            _round.date = self.tournament.date

            pairs = self.get_pairs(round_index)
            _round.matches = self.tournament.initialize_matches(pairs)

            self.tournament.rounds.append(_round)
            return self.tournament.rounds[-1]
        else:
            # To change: raise ?
            print("Impossible to create new round")

    def update_round(self, updated_matches):
        global total_points
        global opponents
        global players_info

        if len(self.tournament.rounds) == 1:
            print(self.tournament.players)
            self.initialize_info()

        self.tournament.update_round(updated_matches)
        _round = self.tournament.rounds[-1]
        total_points = self.tournament.update_total_points(_round, total_points)
        opponents = self.tournament.update_opponents(_round, opponents)
        players_info = self.tournament.update_players_info(players_info, total_points, opponents)

    def get_last_round(self):
        if len(self.tournament.rounds) == 0:
            return None
        else:
            last_round_index = len(self.tournament.rounds)
            last_round = self.tournament.rounds[-1]

        return last_round, last_round_index

    def get_number_of_rounds(self):
        return self.tournament.number_of_rounds

    @staticmethod
    def get_players_from_match(_match):
        return repr(_match[0][0]), repr(_match[1][0])

    @staticmethod
    def update_match(match, score1, score2):
        match[0][1] = score1
        match[1][1] = score2
        return match

    @staticmethod
    def add_player(new_tournament):
        global tournaments
        tournament.Tournament.add_tournament(tournaments, new_tournament)

    @staticmethod
    def get_players():
        global players
        return players

    @staticmethod
    def get_tournaments():
        global tournaments
        return tournaments
