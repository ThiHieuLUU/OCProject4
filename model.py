#! /usr/bin/venv python3
# coding: utf-8

"""This module takes into account all elements (players, rounds, matches) to take place a new tournament."""

from tinydb import TinyDB, Query

import tournament
import player
import chess_round
import location
import mvc_exceptions as mvc_exc
import db_TinyDB as tiny

total_points = dict()
opponents = dict()
players_info = dict()

db = TinyDB('db.json', encoding="utf-8", ensure_ascii=False)
actors_table = db.table('actors')
players_table = db.table('players')
tournaments_table = db.table('tournaments', cache_size=30)
matches_table = db.table('matches', cache_size=30)
rounds_table = db.table('rounds', cache_size=30)


class Model:
    """The Model class is the business logic of the application.
    The Model class provides methods to access the data of the application and
    performs tournament operations. The data can be stored in the Model itself or in
    a database. Only the Model can access the database. A Model never calls
    View's methods.
    """

    def __init__(self):
        """Each instance of the class Medel is associated with a new tournament."""

        self.tournament = tournament.Tournament()
        self.actors_table = tiny.actors_table
        self.tournaments_table = tiny.tournaments_table

    @staticmethod
    def build_location(building_number, street, city, zipcode):
        """Build a location object from given values."""

        return location.Location(building_number=building_number, street=street, city=city, zipcode=zipcode)

    @staticmethod
    def build_player(first_name, last_name, date_of_birth, gender, elo_rating):
        """Build a player object from given values."""

        return player.Player(first_name=first_name, last_name=last_name, date_of_birth=date_of_birth, gender=gender,

                             elo_rating=elo_rating)

    def create_tournament(self, name, _location, date, number_of_rounds, players, time_control, description):
        """Build a tournament object from given values."""

        self.tournament = tournament.Tournament(name=name, location=_location, date=date,
                                                number_of_rounds=number_of_rounds, players=players,
                                                time_control=time_control, description=description)
        # For Tiny_DB:
        self.upsert_players()  # Insert each player if player is not in the table of actors and update if else.
        self.upsert_tournament()  # Insert new tournament in the table of tournaments.

    def initialize_info(self):
        """Initialize values for three global variables."""

        global total_points
        global opponents
        global players_info
        total_points = self.tournament.initialize_total_points()
        opponents = self.tournament.initialize_opponents()
        elo_ratings = self.tournament.get_elo_ratings()
        players_info = self.tournament.initialize_players_info(elo_ratings)

    def check_exist_players(self):
        """Check if there are players in the tournament."""

        if not self.tournament.players:
            return True
        else:
            raise mvc_exc.EmptyListError("Error: there is no player at the moment!")

    def check_if_new_round(self):
        """Check if the index of new round is over the number of rounds."""

        last_round_index = self.get_last_round_index()
        nbr_rounds = self.get_number_of_rounds()
        if last_round_index <= nbr_rounds - 1:
            return True
        else:
            raise mvc_exc.RoundIndexError(f"Can not do your request because the "
                                          f"number of rounds is limited by {nbr_rounds}.")

    def get_first_pairs(self):
        """Get the first pairs for the first round, based on the initial ranking (e.g. elo rating)."""

        return self.tournament.make_pairs_first_round()

    def get_pairs(self, round_index):
        """Get pairs from the second round."""

        global total_points
        global opponents
        global players_info

        # For user, the index of a round is shifted by 1 (in python, index begins by 0).
        nb_rounds = self.tournament.number_of_rounds
        if round_index <= nb_rounds:
            if round_index == 1:
                pairs = self.tournament.make_pairs_first_round()
            else:
                pairs = self.tournament.make_pairs(players_info)
            return pairs
        else:
            raise mvc_exc.RoundIndexError(f"Can not get pairs for the round {round_index} because the "
                                          f"number of rounds is limited by {nb_rounds}.")

    def make_new_round(self, start_time):
        """Build the pairs for a new round and start the round."""

        # For user, the index of a round in a list is shifted by 1, compared to the index in system.
        round_index = len(self.tournament.rounds) + 1
        if round_index <= self.tournament.number_of_rounds:
            _round = chess_round.Round()
            _round.name = " ".join(["Round", str(round_index)])
            _round.date = self.tournament.date

            pairs = self.get_pairs(round_index)
            _round.matches = self.tournament.initialize_matches(pairs)
            _round.start_time = start_time
            self.tournament.rounds.append(_round)

            # For Tiny_DB:
            self.upsert_tournament()

            return self.tournament.rounds[-1]
        else:
            raise mvc_exc.RoundIndexError("Can not start the round because the number of rounds is limited by "
                                          f"{self.tournament.number_of_rounds}.")

    def update_round(self, updated_matches):
        """Update a round after the scores of all matches are known."""

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

        # For Tiny_DB:
        self.upsert_tournament()

    def get_last_round(self):
        """Get the last round in the list of rounds of the tournament. It may be not the final round."""

        # For user, the index of a round in a list is shifted by 1, compared to the index in system.
        if not self.tournament.rounds:
            last_round_index = len(self.tournament.rounds)
            last_round = self.tournament.rounds[-1]
        else:
            raise mvc_exc.RoundIndexError('Error: There is no round now!')

        return last_round, last_round_index

    def get_last_round_index(self):
        """Get the last round index in the list of rounds of the tournament."""

        return len(self.tournament.rounds)

    def get_number_of_rounds(self):
        """Get the number of rounds which is set in the starting of the tournament."""

        return self.tournament.number_of_rounds

    def get_last_ranking(self):
        """Get the ranking of the last finished round. It may be not the final round."""

        global total_points
        global opponents
        global players_info
        if self.get_last_round_index() == 0:
            sorted_players = sorted(self.tournament.players, key=lambda p: p.elo_rating, reverse=True)
            last_ranking = [[repr(_player), _player.elo_rating] for _player in sorted_players]
        else:
            sorted_players_info = sorted(players_info, key=lambda k: (-k["total_point"], -k['initial_ranking']))
            last_ranking = [[repr(item["player"]), item["total_point"], item["initial_ranking"]] for item in
                            sorted_players_info]
        return last_ranking

    @staticmethod
    def get_items(items, item_name):
        """The method is used as a pattern for get players, rounds, matches."""

        if not items:
            return items
        else:
            raise mvc_exc.EmptyListError(f'For the moment, there is no {item_name} in the list of'
                                         f' {item_name}s!')

    @staticmethod
    def get_players(_tournament):
        """Get the list of players of the tournament."""

        return Model.get_items(_tournament.players, "player")

    @staticmethod
    def get_rounds(_tournament):
        """Get the list of rounds of the tournament."""

        rounds = _tournament.rounds
        return Model.get_items(rounds, "round")

    @staticmethod
    def get_matches(_tournament):
        """Get the list of matches of the tournament."""

        rounds = _tournament.rounds
        if not rounds:
            matches = [match for _round in rounds for match in _round.matches]
        else:
            raise mvc_exc.EmptyListError("There is no round now!")
        return Model.get_items(matches, "matche")

    def get_players_new_tournament(self):
        """Get the list of players of the actual tournament (which is the self.tournament)."""
        return Model.get_players(self.model.tournament)

    def get_rounds_new_tournament(self):
        """Get the list of rounds of the actual tournament (which is the self.tournament)."""

        return Model.get_rounds(self.model.tournament)

    def get_matches_new_tournament(self):
        """Get the list of matches of the actual tournament (which is the self.tournament)."""

        return Model.get_matches(self.model.tournament)

    @staticmethod
    def get_players_from_match(_match):
        """To display two players of a match."""

        return repr(_match[0][0]), repr(_match[1][0])

    @staticmethod
    def update_match(match, score1, score2):
        """Update match when the scores of two players are known."""

        match[0][1] = score1
        match[1][1] = score2
        return match

    def upsert_tournament(self):
        """Update and insert the actual tournament in the data base (the table of tournaments)."""
        
        serialized_tournament = tiny.serialize_item(self.tournament)
        tiny.upsert_tournament(self.tournaments_table, serialized_tournament)

    def upsert_players(self):
        """Update and insert the list of players of the actual tournament in the data base (the table of 
        actors)."""

        serialized_players = tiny.serialize_items(self.tournament.players)
        tiny.upsert_multiple(self.actors_table, serialized_players, tiny.upsert_player)

    def get_tournaments(self):
        """Retrieve the data of tournaments from the data base and rebuild them to a list of tournaments."""

        db_serialized_items = self.tournaments_table.all()
        fct = tournament.Tournament.get_deserialized_tournament
        deserialized_tournaments = tiny.deserialize_items(db_serialized_items, fct)
        return deserialized_tournaments

    def get_actors(self):
        """Retrieve the data of players from the data base and rebuild them to a list of players."""

        db_serialized_items = self.actors_table.all()
        fct = player.Player.create_player
        deserialized_actors = tiny.deserialize_items(db_serialized_items, fct)
        return deserialized_actors

    def get_actors_alphabetical_order(self):
        """Retrieve all players from the data base and sort these players by theirs names in the alphabetical order.
        """

        actors = self.get_actors()
        return sorted(actors, key=lambda actor: actor.first_name)

    def get_actors_ranking_order(self):
        """Retrieve all players from the data base and sort these players by theirs ranking (elo rating)."""

        actors = self.get_actors()
        return sorted(actors, key=lambda actor: actor.elo_rating, reverse=True)
