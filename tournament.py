#! /usr/bin/venv python3
# coding: utf-8

"""This module is used to model a chess tournament with all information about the location, the date, the players."""

import copy

import basic_backend
import mvc_exceptions as mvc_exc
import player
import location
import chess_round
import constants

DEFAULT_NUMBER_OF_ROUNDS = constants.default_number_of_rounds

none_player = player.Player()


class Tournament:
    """This class represents a tournament with some attributes where:
     - location is an instance of the Location class.
     - players is a list of instances of the Player class.
     - rounds is a list of instances of the Round class (a round contains Match instances).
     """

    def __init__(self, name=None, _location=None, date=None, number_of_rounds=DEFAULT_NUMBER_OF_ROUNDS, players=None,
                 time_control=None, description=None):

        self._name = name
        self._location = _location
        self._date = date
        self._number_of_rounds = number_of_rounds
        self._rounds = []
        self._players = players
        self._time_control = time_control
        self._description = description
        # Last ranking is a list of ranking after the last round.
        # Each element of the list is a list associated to a player: [repr(player), total point, elo rating]
        self._last_ranking = None

    def __hash__(self):
        return hash((self._name, self._location, self._date))  # tuple hash

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return (self._name, self._location, self._date) == (other.name, other.location, other.date)
        return False

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        self._name = new_name

    @name.deleter
    def name(self):
        del self._name

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, new_location):
        self._location = new_location

    @location.deleter
    def location(self):
        del self._location

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, new_date):
        self._date = new_date

    @date.deleter
    def date(self):
        del self._date

    @property
    def number_of_rounds(self):
        return self._number_of_rounds

    @number_of_rounds.setter
    def number_of_rounds(self, new_number_of_rounds):
        self._number_of_rounds = new_number_of_rounds

    @number_of_rounds.deleter
    def number_of_rounds(self):
        del self._number_of_rounds

    @property
    def rounds(self):
        return self._rounds

    @rounds.setter
    def rounds(self, new_rounds):
        self._rounds = new_rounds

    @rounds.deleter
    def rounds(self):
        del self._rounds

    @property
    def players(self):
        return self._players

    @players.setter
    def players(self, new_players):
        self._players = new_players

    @players.deleter
    def players(self):
        del self._players

    @property
    def time_control(self):
        return self._time_control

    @time_control.setter
    def time_control(self, new_time_control):
        self._time_control = new_time_control

    @time_control.deleter
    def time_control(self):
        del self._time_control

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, new_description):
        self._description = new_description

    @description.deleter
    def description(self):
        del self._description

    @property
    def last_ranking(self):
        return self._last_ranking

    @last_ranking.setter
    def last_ranking(self, new_last_ranking):
        self._last_ranking = new_last_ranking

    @last_ranking.deleter
    def last_ranking(self):
        del self._last_ranking

    def get_elo_ratings(self):
        """Build a dictionary where each key is a player in the list of players of the tournament
        and value is his elo rating.
        """

        elo_ratings = dict()
        for _player in self._players:
            elo_ratings[_player] = _player.elo_rating
        return elo_ratings

    def make_pairs_first_round(self):
        """Build the pairs for the first round based on the ranking of players (sort by elo rating)."""

        if self._players is not None and len(self._players) > 0:
            pairs = []
            sorted_players = sorted(self._players, key=lambda p: p.elo_rating, reverse=True)
            half_number = len(self._players) // 2

            for index in range(half_number):
                pairs.append([sorted_players[index], sorted_players[half_number + index]])

            if len(self._players) % 2 == 1:
                pairs.append([none_player, sorted_players[-1]])
        else:
            raise mvc_exc.EmptyListError('There is no player at the moment!')
        return pairs

    @staticmethod
    def make_pair(player_1, not_yet_encountered_players):
        """Given the player 1, find the player 2 such that they mustn't be encountered before."""

        if not not_yet_encountered_players:
            raise mvc_exc.EmptyListError(f"List of not yet encountered players for player {repr(player_1)} is empty!")

        player_2_info = not_yet_encountered_players[0]
        player_2 = player_2_info["player"]
        # Eliminate the taken player_2 for the next time if it has to re-find player_2
        not_yet_encountered_players = not_yet_encountered_players[1:]
        pair = [player_1, player_2]

        return pair, player_2_info, not_yet_encountered_players

    def make_pairs(self, players_info):
        """Build the pairs from the second round.

        The rule is that two players will be encountered if theirs order's ranking is near and
        they must not be encountered before.
        """

        pairs = []
        sorted_players_info = sorted(players_info, key=lambda k: (-k["total_point"], -k['initial_ranking']))

        player_number = len(sorted_players_info)
        pair_index = 1
        # If the numbers of players is odd, the treatment is only done for the numbers of players - 1
        pair_number = player_number // 2

        # Each pair has two players, build player_1 as a dictionary in order to mark the player of which pair
        sorted_players_info_dict = dict()
        sorted_players_info_dict[pair_index] = sorted_players_info
        not_yet_encountered_players = dict()
        called_time = dict()
        called_time[pair_index] = 1
        while pair_index <= pair_number:
            player_1_info = sorted_players_info_dict[pair_index][0]
            player_1 = player_1_info["player"]
            if called_time[pair_index] == 1:
                # This list has always the player_1
                not_yet_encountered_players[pair_index] = [info for info in sorted_players_info_dict[pair_index]
                                                           if info["player"] not in player_1_info["opponents"]]
                # Eliminate the player_1 in the list, player_1 is the first element of the list.
                not_yet_encountered_players[pair_index] = not_yet_encountered_players[pair_index][1:]
                called_time[pair_index] += 1
            try:
                pair_result = self.make_pair(player_1, not_yet_encountered_players[pair_index])
            except mvc_exc.EmptyListError:
                # Return in the previous pair and re-make previous pair
                pair_index -= 1  # CHANGE HERE : -=1 to re-make the previous pair, pair_index = 1: re-begin all
                # Remove the previous pair to re-make it.
                pairs.pop()
            else:
                pair, player_2_info, new_not_yet_encountered_players = pair_result
                # Update the list of not yet encountered players after selecting one of its elements, then remove the
                # selected element from the list. The goal is that the next time, another player will be selected.
                not_yet_encountered_players[pair_index] = new_not_yet_encountered_players
                # pass to next pair
                pair_index += 1
                # Each time, remove the pair of players has been made in the sorted list
                sorted_players_info_dict[pair_index] = [element for element
                                                        in sorted_players_info_dict[pair_index - 1]
                                                        if element["player"] not in pair]
                called_time[pair_index] = 1

                # Build pair
                pairs.append(pair)

        if player_number % 2 == 1:
            # Pair with none player if number of players is odd
            pairs.append([sorted_players_info_dict[pair_index][-1]["player"], none_player])

        return pairs

    def update_round(self, updated_matches):
        """Conventions: update only the last round."""

        last_round = self._rounds[-1]
        last_round.update_round(updated_matches)

    def initialize_total_points(self):
        """Build a dictionary of total points where each key is a player, its value is the total point of this player.

        It is updated after each round.
        """

        total_points = dict()
        for _player in self._players:
            total_points[_player] = 0
        return total_points

    @staticmethod
    def update_total_points(_round, total_points):
        """After each round, the total-point dictionary is updated by the scores of the matches."""

        for _match in _round.matches:
            # match is an object of class Match with attribute "match"
            if _match.match[0][0] != none_player:  # odd number of players
                total_points[_match.match[0][0]] += _match.match[0][1]

            if _match.match[1][0] != none_player:  # odd number of players
                total_points[_match.match[1][0]] += _match.match[1][1]
        return total_points

    def initialize_opponents(self):
        """Build a dictionary of opponents where each key is a player, its value is a list of all encountered players
        of this player.

        It is updated after each round.
        """

        opponents = dict()
        for _player in self._players:
            opponents[_player] = []
        return opponents

    @staticmethod
    def update_opponents(_round, opponents):
        """After each round, the opponent dictionary is updated by adding the encountered player in the list of
        opponents of each player.
        """

        for _match in _round.matches:
            # _match is an objet of class Match with attribute match = ([player_1, score1], [player_2, score2])
            # if _match.match[0][0] != none_player and _match.match[1][0] != none_player:  # odd number of players
            if none_player not in (_match.match[0][0], _match.match[1][0]):  # odd number of players
                opponents[_match.match[0][0]].append(_match.match[1][0])
                opponents[_match.match[1][0]].append(_match.match[0][0])
        return opponents

    def initialize_players_info(self, elo_ratings):
        """Initialize the a list of dictionaries. Each dictionary contains information for each player: player
        himself, his total point, his elo ranking and his list of opponents after each round."""

        players_info = []
        for _player in self._players:
            info = dict()
            info["player"] = _player
            info["total_point"] = []
            info["initial_ranking"] = elo_ratings[_player]
            info["opponents"] = []
            players_info.append(info)
        return players_info

    @staticmethod
    def update_players_info(players_info, total_points, opponents):
        """After each round, the list of players' information is updated (total point, opponents)."""

        for info in players_info:
            _player = info["player"]
            info["total_point"] = total_points[_player]
            info["opponents"] = opponents[_player]
        return players_info

    def get_serialized_attributes(self):
        """Serialize all attributes of a tournament instance in order to save them in a document oriented database
        (here, TinyDB).

        It must serialize player list (list of player instances), round list (list of round instances) and location.
        """

        attributes_info = basic_backend.get_attributes(self)
        new_dict = copy.deepcopy(attributes_info)

        for index, _player in enumerate(new_dict["players"]):
            serialized_player = _player.get_attributes()
            new_dict["players"][index] = serialized_player

        for index, _round in enumerate(new_dict["rounds"]):
            serialized_round = _round.get_serialized_attributes()
            new_dict["rounds"][index] = serialized_round

        new_dict["location"] = new_dict["location"].get_serialized_attributes()
        return new_dict

    @classmethod
    def get_deserialized_tournament(cls, serialized_attributes_values):
        """Rebuild a tournament object from serialized attributes-values
        (e.g. from TinyDB).
        """

        for key in serialized_attributes_values.keys():
            if key == "rounds":
                rounds = serialized_attributes_values["rounds"]
                for index, round_info in enumerate(rounds):
                    deserialized_round = chess_round.Round.get_deserialized_round(round_info)
                    rounds[index] = deserialized_round

            if key == "players":
                players = serialized_attributes_values["players"]
                for index, player_info in enumerate(players):
                    deserialized_player = player.Player.create_player(player_info)
                    players[index] = deserialized_player

            if key == "location":
                location_info = serialized_attributes_values["location"]
                deserialized_location = location.Location.create_location(location_info)
                serialized_attributes_values["location"] = deserialized_location

        _tournament = basic_backend.create_item(serialized_attributes_values, cls)
        return _tournament

    def get_attributes(self):
        """Get names of attributes (without protected or private sign) and theirs values."""

        attributes_info = basic_backend.get_attributes(self)
        return attributes_info

    def set_attrs(self, kwargs):
        """Set values for all attributes via a dictionary."""

        basic_backend.set_attrs(self, kwargs)

    @classmethod
    def create_tournament(cls, attributes_values):
        """Create a tournament from a dictionary of attributes - values."""

        return basic_backend.create_item(attributes_values, cls)

    def __str__(self):
        """Print all attributes and theirs values for a tournament."""

        attr_str = basic_backend.get_str(self)
        return attr_str

    def __repr__(self):
        """Display the string representation of a tournament object."""

        if self._name is not None:
            return ", ".join([self._name, self._date])
            # return self._name + "\n -date: " + str(self._date) + "\n -location: " + str(self._location)
        return str(None)
