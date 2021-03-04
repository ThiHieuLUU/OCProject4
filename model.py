#! /usr/bin/venv python3
# coding: utf-8

"""This module takes into account all elements (players, rounds, matches) to take place a tournament."""

import tournament
import player
import chess_round
import location
import mvc_exceptions as mvc_exc

total_points = dict()
opponents = dict()
players_info = dict()


class Model:
    """The Model class is the business logic of the application.
    The Model class provides methods to access the data of the application and
    performs tournament operations. The data can be stored in the Model itself or in
    a database. Only the Model can access the database. A Model never calls
    View's methods.
    """
    tournaments = list()
    players = list()

    def __init__(self):
        """Each model instance is associated with a tournament."""

        self.tournament = tournament.Tournament()
        type(self).tournaments.append(self.tournament)
        type(self).players.append(self.tournament.players)

    @staticmethod
    def build_location(building_number, street, city, zipcode):
        """Build a location object from given values."""

        return location.Location(building_number=building_number, street=street, city=city, zipcode=zipcode)

    @staticmethod
    def build_player(first_name, last_name, date_of_birth, gender, elo_rating):
        """Build a player object from given values."""

        return player.Player(first_name=first_name, last_name=last_name, date_of_birth=date_of_birth, gender=gender,

                             elo_rating=elo_rating)

    # @staticmethod
    # def add_player(new_player):
    #     global players
    #     player.Player.add_player(players, new_player)

    def create_tournament(self, name, _location, date, number_of_rounds, players, time_control, description):
        """Build a tournament object from given values."""

        self.tournament = tournament.Tournament(name=name, location=_location, date=date,
                                                number_of_rounds=number_of_rounds, players=players,
                                                time_control=time_control, description=description)

    def initialize_info(self):
        """Initialize values for three global variable."""

        global total_points
        global opponents
        global players_info
        total_points = self.tournament.initialize_total_points()
        opponents = self.tournament.initialize_opponents()
        elo_ratings = self.tournament.get_elo_ratings()
        players_info = self.tournament.initialize_players_info(elo_ratings)

    def check_exist_players(self):
        if self.tournament.players is not None and len(self.tournament.players) > 0:
            return True
        else:
            raise mvc_exc.EmptyListError("Error: there is no player at the moment!")

    def get_first_pairs(self):
        return self.tournament.make_pairs_first_round()

    def get_pairs(self, round_index):
        global total_points
        global opponents
        global players_info

        # round index for user, shift 1 compared to the real
        if round_index <= self.tournament.number_of_rounds:
            if round_index == 1:
                pairs = self.tournament.make_pairs_first_round()
            else:
                pairs = self.tournament.make_pairs(players_info)
            return pairs
        else:
            raise mvc_exc.RoundIndexError(f"Can not get pairs for the round {round_index} because the "
                                          f"number of rounds is limited by {self.tournament.number_of_rounds}.")

    def make_new_round(self, start_time):
        # Advanced one round index
        round_index = len(self.tournament.rounds) + 1
        if round_index <= self.tournament.number_of_rounds:
            _round = chess_round.Round()
            _round.name = "Round " + str(round_index)
            _round.date = self.tournament.date

            pairs = self.get_pairs(round_index)
            _round.matches = self.tournament.initialize_matches(pairs)
            _round.start_time = start_time
            self.tournament.rounds.append(_round)
            return self.tournament.rounds[-1]
        else:
            # To change: raise ?
            raise mvc_exc.RoundIndexError("Can not start the round because the number of rounds is limited by "
                                          f"{self.tournament.number_of_rounds}.")
            # print("Impossible to create new round)

    def update_round(self, updated_matches):
        global total_points
        global opponents
        global players_info

        if len(self.tournament.rounds) == 1:
            self.initialize_info()

        self.tournament.update_round(updated_matches)
        _round = self.tournament.rounds[-1]
        total_points = self.tournament.update_total_points(_round, total_points)
        opponents = self.tournament.update_opponents(_round, opponents)
        players_info = self.tournament.update_players_info(players_info, total_points, opponents)

    def get_last_round(self):
        """Get the last round in the list of rounds of the tournament. It will not be the final round."""

        # round index for user, shift 1 compared to the real
        if len(self.tournament.rounds) == 0:
            return None
        else:
            last_round_index = len(self.tournament.rounds)
            last_round = self.tournament.rounds[-1]

        return last_round, last_round_index

    def get_last_round_index(self):
        """Get the last round index in the list of rounds of the tournament."""

        return len(self.tournament.rounds)

    def get_number_of_rounds(self):
        """Get the number of rounds which is set in the starting of the tournament."""

        return self.tournament.number_of_rounds

    def get_last_ranking(self):
        """Get the ranking of the last rounds."""

        global total_points
        global opponents
        global players_info
        if self.get_last_round_index() == 0:
            sorted_players = sorted(self.tournament.players, key=lambda p: p.elo_rating, reverse=True)
            last_ranking = [[repr(_player), _player.elo_rating] for _player in sorted_players]
            # print(last_ranking)
        else:
            sorted_players_info = sorted(players_info, key=lambda k: (-k["total_point"], -k['initial_ranking']))
            last_ranking = [[repr(item["player"]), item["total_point"], item["initial_ranking"]] for item in
                            sorted_players_info]
        return last_ranking

    @staticmethod
    def get_items(items, item_name):
        """The method is used as a pattern for get players, rounds, matches."""

        if items is not None and len(items) > 0:
            return items
        else:
            raise mvc_exc.EmptyListError(f'For the moment, there is no {item_name} in the list of'
                                         f' {item_name}s!')

    def get_players(self):
        """Get player list of the tournament."""

        return self.get_items(self.tournament.players, "player")

    def get_rounds(self):
        """Get round list of the tournament."""

        return self.get_items(self.tournament.rounds, "round")

    def get_matches(self):
        """Get match list of the tournament."""

        rounds = self.tournament.rounds
        matches = []
        if rounds is not None and len(rounds) > 0:
            matches = [match for _round in rounds for match in _round.matches]
        return self.get_items(matches, "match")

    @staticmethod
    def get_players_from_match(_match):
        """To display two players of a match."""

        return repr(_match[0][0]), repr(_match[1][0])

    @staticmethod
    def update_match(match, score1, score2):
        """Update match with input of scores."""

        match[0][1] = score1
        match[1][1] = score2
        return match

    # @staticmethod
    # def get_tournaments():
    #     # global tournaments
    #     return Model.tournaments
