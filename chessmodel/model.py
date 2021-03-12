#! /usr/bin/venv python3
# coding: utf-8

"""This module takes into account all elements (players, rounds, matches) to take place a new tournament.

It also accesses and handles the database (here for tournaments and actors).
"""
from tinydb import TinyDB

from . import tournament
from . import player
from . import chess_round
from . import location
import mvc_exceptions as mvc_exc
from . import db_tinydb as tiny

# 'db.json' is created and updated where model module is called, e.g. in the directory containing controller.
db = TinyDB('db.json', encoding="utf-8", ensure_ascii=False)
actors_table = db.table('actors')
tournaments_table = db.table('tournaments', cache_size=30)

# clear the table if necessary
# actors_table.truncate()
# tournaments_table.truncate()


class Model:
    """The Model class is the business logic of the application.
    The Model class provides methods to access the data of the application and
    performs tournament operations. The data can be stored in the Model itself or in
    a database. Only the Model can access the database.
    """

    def __init__(self):
        """Each instance of the Model class is associated with a new tournament.
        The table of actors in the database is updated here.
        The table of tournament in the database is updated here.
        """

        self.tournament = tournament.Tournament()

        # Dictionaries represent some information for each player (his total point, his list of opponents)
        # These dictionaries are updated after each round.
        self.total_points = dict()
        self.opponents = dict()
        self.players_info = dict()

        # For the table of actors and the table of tournaments in the database.
        self.actors_table = actors_table
        self.tournaments_table = tournaments_table

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

        self.tournament = tournament.Tournament(name=name, _location=_location, date=date,
                                                number_of_rounds=number_of_rounds, players=players,
                                                time_control=time_control, description=description)
        # For Tiny_DB:
        self.upsert_players()  # Insert each player if this player is not in the table of actors or update if else.
        self.upsert_tournament()  # Insert new tournament in the table of tournaments.

    def initialize_info(self):
        """Initialize values for: total_points, opponents and players_info"""

        self.total_points = self.tournament.initialize_total_points()  # all palyers have 0 point
        self.opponents = self.tournament.initialize_opponents()  # all players have an empty list of opponents
        elo_ratings = self.tournament.get_elo_ratings()

        # First, insert total_points, opponents, and elo_ratings for each player
        self.players_info = self.tournament.initialize_players_info(elo_ratings)

    def check_exist_players(self):
        """Check if there are players in the tournament."""

        if not self.tournament.players:
            raise mvc_exc.EmptyListError("Error: there is no player at the moment!")
        return True

    def check_if_new_round(self):
        """Check if the index of new round is over the number of rounds."""

        last_round_index = self.get_last_round_index()
        nbr_rounds = self.get_number_of_rounds()

        if last_round_index > nbr_rounds - 1:
            raise mvc_exc.RoundIndexError(f"Can not do your request because the "
                                          f"number of rounds is limited by {nbr_rounds}.")
        return True

    def get_first_pairs(self):
        """Get the first pairs for the first round, based on the initial ranking (e.g. elo rating)."""

        return self.tournament.make_pairs_first_round()

    def get_pairs(self, round_index):
        """Get pairs for a round in the limite of number of rounds which is set before."""

        nb_rounds = self.tournament.number_of_rounds
        # Here, round index is seen by user (that is added by 1 compared to the index in the system).
        if round_index <= nb_rounds:
            if round_index == 1:
                pairs = self.tournament.make_pairs_first_round()
            else:
                pairs = self.tournament.make_pairs(self.players_info)
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
            _round.initialize_matches(pairs)
            _round.start_time = start_time
            self.tournament.rounds.append(_round)

            # For Tiny_DB
            self.get_last_ranking_new_tournament()
            self.upsert_tournament()

            return self.tournament.rounds[-1]
        else:
            raise mvc_exc.RoundIndexError("Can not start the round because the number of rounds is limited by "
                                          f"{self.tournament.number_of_rounds}.")

    @staticmethod
    def get_players_from_match(match):
        """To display two player objects of a match."""

        return match.get_players_from_match()

    @staticmethod
    def update_match(match, score1, score2):
        """Update match when the scores of two players are known."""

        return match.update_match(score1, score2)

    def update_round(self, updated_matches):
        """Update a round after the scores of matches are known."""

        if len(self.tournament.rounds) == 1:
            self.initialize_info()

        self.tournament.update_round(updated_matches)
        _round = self.tournament.rounds[-1]
        self.total_points = self.tournament.update_total_points(_round, self.total_points)
        self.opponents = self.tournament.update_opponents(_round, self.opponents)
        self.players_info = self.tournament.update_players_info(self.players_info, self.total_points, self.opponents)

        # For Tiny_DB
        self.get_last_ranking_new_tournament()
        self.upsert_tournament()

    def get_last_round(self):
        """Get the last round in the list of rounds. It may not be the final round."""

        # For user, the index of a round in a list is shifted by 1, compared to the index in system.
        if self.tournament.rounds is not None and len(self.tournament.rounds) > 0:
            last_round_index = len(self.tournament.rounds)
            last_round = self.tournament.rounds[-1]

            # For Tiny_DB
            self.get_last_ranking_new_tournament()
            self.upsert_tournament()
        else:
            raise mvc_exc.RoundIndexError('Error: There is no round now!')

        return last_round, last_round_index

    def get_last_round_index(self):
        """Get the last round index in the list of rounds. It may not be the final round."""

        return len(self.tournament.rounds)

    def get_number_of_rounds(self):
        """Get the number of rounds which is set in the starting of the tournament."""

        return self.tournament.number_of_rounds

    def get_last_ranking_new_tournament(self):
        """Get the ranking of the last finished round. It may not be the final round."""

        if self.get_last_round_index() == 0:
            sorted_players = sorted(self.tournament.players, key=lambda p: p.elo_rating, reverse=True)
            last_ranking = [[repr(_player), _player.elo_rating] for _player in sorted_players]
        else:
            sorted_players_info = sorted(self.players_info, key=lambda k: (-k["total_point"], -k['initial_ranking']))
            last_ranking = [[repr(item["player"]), item["total_point"], item["initial_ranking"]] for item in
                            sorted_players_info]

        # For Tiny_DB:
        self.tournament.last_ranking = last_ranking
        self.upsert_tournament()
        return last_ranking

    def get_players_new_tournament(self):
        """Get the list of players of the current tournament (which is the self.tournament)."""

        return Model.get_players(self.tournament)

    def get_rounds_new_tournament(self):
        """Get the list of rounds of the current tournament (which is the self.tournament)."""

        return Model.get_rounds(self.tournament)

    def get_matches_new_tournament(self):
        """Get the list of matches of the current tournament (which is the self.tournament)."""

        return Model.get_matches(self.tournament)

    @staticmethod
    def get_items(items, item_name):
        """The method is used as a pattern for get players, rounds, matches."""

        if not items:
            raise mvc_exc.EmptyListError(f'Error: there is no {item_name} in the list of'
                                         f' {item_name}s!')
        return items

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
        if rounds is not None and len(rounds) > 0:
            matches = [match for _round in rounds for match in _round.matches]
        else:
            raise mvc_exc.EmptyListError("Error: there is no match in the list of matches!")
        return Model.get_items(matches, "matche")

    @staticmethod
    def get_last_ranking(_tournament):
        """Get the ranking of the last round. It may not be the final round."""

        last_ranking = _tournament.last_ranking
        try:
            Model.get_items(_tournament.last_ranking, "last ranking")
        except mvc_exc.EmptyListError as error:
            raise mvc_exc.EmptyListError(error)

        last_round_index = len(_tournament.rounds)
        return last_ranking, last_round_index

    @staticmethod
    def get_player_sample():
        """Get a random sample of players from the Player class."""

        return player.Player.get_players()

    def get_tournaments(self):
        """Retrieve the data of tournaments from the database and rebuild them to a list of tournaments."""

        # Upsert when the tournament is created with full information.
        if self.tournament != tournament.Tournament():
            self.upsert_tournament()

        db_serialized_items = self.tournaments_table.all()
        fct = self.tournament.get_deserialized_tournament
        deserialized_tournaments = tiny.deserialize_items(db_serialized_items, fct)
        return deserialized_tournaments

    def get_actors(self):
        """Retrieve the data of players from the database and rebuild them to a list of players."""

        db_serialized_items = self.actors_table.all()
        fct = player.Player.create_player
        deserialized_actors = tiny.deserialize_items(db_serialized_items, fct)
        return deserialized_actors

    def get_actors_alphabetical_order(self):
        """Retrieve all players from the database and sort these players by theirs names in the alphabetical order.
        """

        actors = self.get_actors()
        return sorted(actors, key=lambda actor: actor.first_name)

    def get_actors_ranking_order(self):
        """Retrieve all players from the database and sort these players by theirs ranking (elo rating)."""

        actors = self.get_actors()
        return sorted(actors, key=lambda actor: actor.elo_rating, reverse=True)

    def upsert_tournament(self):
        """Update and insert the current tournament in the database (the table of tournaments)."""

        serialized_tournament = tiny.serialize_item(self.tournament)
        tiny.upsert_tournament(self.tournaments_table, serialized_tournament)

    def upsert_players(self):
        """Update and insert the list of players of the current tournament into the database
        (the table of actors).
        """

        serialized_players = tiny.serialize_items(self.tournament.players)
        tiny.upsert_multiple(self.actors_table, serialized_players, tiny.upsert_player)
