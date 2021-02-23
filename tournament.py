"""docstring"""

from datetime import datetime, date
import basic_backend
import mvc_exceptions as mvc_exc
import round_robin
import player
import player_list
import match
import location

# default_number_of_rounds = 4
DEFAULT_NUMBER_OF_ROUNDS = 4

none_player = player.Player()

tournaments = dict()

class Tournament:
    """docstring"""
    count_round = 0

    def __init__(self):
        self._name = None
        self._location = None
        self._date = None
        self._number_of_rounds = DEFAULT_NUMBER_OF_ROUNDS
        self._rounds = []
        self._players = None
        self._time_control = None
        self._description = None
        self.item_type = type(self)

    def __hash__(self):
        return hash((self._name, self._location, self._date))  # tuple hash

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return (self._name, self._location, self._date) \
               == (other.name, other.location, other.date)
        return False

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        if isinstance(new_name, str):
            self._name = new_name
        else:
            raise mvc_exc.UnexpectedString(f'Input "{new_name}" does not meet expectations')

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
        date_format = "%d/%m/%Y"
        if datetime.strptime(str(new_date), date_format):
            self._date = new_date
        else:
            raise mvc_exc.DateError('Incorrect date date_format. It should be DD/MM/YYYY')

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

    def get_elo_ratings(self):
        """docstring"""
        elo_ratings = dict()
        for _player in self._players:
            elo_ratings[_player] = _player.elo_rating
        return elo_ratings

    def make_pairs_first_round(self):
        """docstring"""
        pairs = []
        sorted_players = sorted(self._players, key=lambda p: p.elo_rating, reverse=True)
        half_number = int(len(self._players) / 2)

        for index in range(half_number):
            pairs.append([sorted_players[index], sorted_players[half_number + index]])

        if len(self._players) % 2 == 1:
            pairs.append([none_player, sorted_players[-1]])

        print("*" * 10)
        print("First pairs by elo rating")
        for pair in pairs:
            print(pair[0].elo_rating, pair[1].elo_rating)
        print("*" * 10)

        return pairs

    def make_pair(self, player_1, not_yet_encountered_players):
        if len(not_yet_encountered_players) >= 1:
            player_2_info = not_yet_encountered_players[0]
            player_2 = player_2_info["player"]
            # Eliminate the taken player_2 for the next time if it has to re-find player_2
            not_yet_encountered_players = not_yet_encountered_players[1:]
            pair = [player_1, player_2]
            return pair, player_2_info, not_yet_encountered_players
        else:
            return None

    def make_pairs(self, players_info):
        """docstring"""
        pairs = []
        sorted_players_info = sorted(players_info, key=lambda k: (-k["total_point"], -k['initial_ranking']))

        player_number = len(sorted_players_info)
        pair_index = 1
        # If the numbers of players is odd, the treatment is only done to the numbers of players - 1
        pair_number = int(player_number / 2)

        # Each pair has its own player, built player_1 as dictionary in order to mark the player of which pair
        sorted_players_info_dict = dict()
        sorted_players_info_dict[pair_index] = sorted_players_info
        not_yet_encountered_players = dict()
        called_time = dict()
        called_time[pair_index] = 1
        while pair_index <= pair_number:
            print("pair_index", pair_index)
            player_1_info = sorted_players_info_dict[pair_index][0]
            player_1 = player_1_info["player"]
            if called_time[pair_index] == 1:
                # This list has always the player_1
                not_yet_encountered_players[pair_index] = [info for info in sorted_players_info_dict[pair_index]
                                                       if info["player"] not in player_1_info["opponents"]]
                # eliminate the player_1 in the list, player_1 is the first element of the list
                not_yet_encountered_players[pair_index] = not_yet_encountered_players[pair_index][1:]
                called_time[pair_index] += 1

            pair_result = self.make_pair(player_1, not_yet_encountered_players[pair_index])
            if pair_result is None:
                # return in the previous pair and re-make
                pair_index -= 1 # CHANGE HERE : -=1 to re-make the previous pair, pair_index = 1: re-begin all
                print("It has to return to make the previous pair")
                # remove the previous pair to re-make it
                pairs.pop()

            else:
                pair, player_2_info, new_not_yet_encountered_players = pair_result
                # update the list of not yet encountered players after selecting one of its elements, the remove this
                # element  the list. The goal is the next time, the other element will be selected
                not_yet_encountered_players[pair_index] = new_not_yet_encountered_players
                # pass to next pair
                pair_index += 1
                # Each time, remove the pair of players has been made in the sorted list
                sorted_players_info_dict[pair_index] = [element for element
                                                        in sorted_players_info_dict[pair_index - 1]
                                                        if element["player"] not in pair]
                called_time[pair_index] = 1

                # print("after\n ", sorted_players_info_dict[pair_index])
                # Built pair
                pairs.append(pair)
                # paired_player_number += 2

                print(f'{player_1_info["total_point"]} vs {player_2_info["total_point"]}; '
                      f'{player_1_info["player"].elo_rating} vs {player_2_info["player"].elo_rating}; '
                      f'{player_1_info["player"] in player_2_info["opponents"]} vs '
                      f'{player_2_info["player"] in player_1_info["opponents"]}')

        if player_number % 2 == 1:
            # Pair with none player if number of player is odd
            pairs.append([sorted_players_info_dict[pair_index][-1]["player"], none_player])
            print(sorted_players_info_dict[pair_index][-1]["player"]["total_point"],
                  sorted_players_info_dict[pair_index][-1]["player"].elo_rating)

        return pairs

    @staticmethod
    def initialize_matches(pairs):
        """docstring"""
        matches = []
        for pair in pairs:
            m = match.Match(pair[0], 0, pair[1], 0)
            matches.append(m.match)
        return matches

    def update_round(self, _round):
        """docstring"""
        matches = _round.matches
        match_index = 1
        while match_index <= len(matches):
            match = matches[match_index - 1]  # ([player_1, score1], [player_2, score2])
            none_player = player.Player()
            if match[0][0] != none_player and match[1][0] != none_player:
                print("\n")
                print(f"{_round.name}, match {match_index}, enter the scores:")
                score1 = float(
                    input(f'FIDE ID = {match[0][0].fide_id}, Name = '
                          f'{match[0][0].first_name + " " + match[0][0].last_name}, '
                          f'score = '))
                score2 = float(
                    input(f'FIDE ID = {match[1][0].fide_id}, Name = '
                          f'{match[1][0].first_name + " " + match[1][0].last_name}, '
                          f'score = '))
                score_list = [0, 0.5, 1]
                if score1 in score_list and score2 in score_list and score1 + score2 == 1.0:
                    match_index += 1
                    match[0][1] = score1  # update also to _round.matches
                    match[1][1] = score2
                else:
                    print('Typing error. Score must be: 0, 0.5 or 1. The sum of scores must be equal to 1. Re-enter:'
                          '1.')
                    # raise mvc_exc.ScoreError('Re-enter scores. The sum of scores must be equal to 1')

            else:
                # Odd number of players, the worst ranking player has one free point.
                if match[0][0] == none_player:
                    match[1][1] = 1
                elif match[1][0] == none_player:
                    match[0][1] = 1
                match_index += 1

    def initialize_total_points(self):
        """docstring"""
        total_points = dict()
        for player in self._players:
            total_points[player] = 0
        return total_points

    # @staticmethod
    def update_total_points(self, _round, total_points):
        """docstring"""
        for match in _round.matches:
            if match[0][0] != none_player:  # odd number of players
                total_points[match[0][0]] += match[0][1]

            if match[1][0] != none_player:  # odd number of players
                total_points[match[1][0]] += match[1][1]
        return total_points

    def initialize_opponents(self):
        """docstring"""
        opponents = dict()
        for _player in self._players:
            opponents[_player] = []
        return opponents

    @staticmethod
    def update_opponents(_round, opponents):
        """docstring"""
        for match in _round.matches:
            # match structure: ([player_1, score1], [player_2, score2])
            if match[0][0] != none_player and match[1][0] != none_player:  # odd number of players
                opponents[match[0][0]].append(match[1][0])
                opponents[match[1][0]].append(match[0][0])
        return opponents

    def initialize_players_info(self, elo_ratings):
        """docstring"""
        players_info = []
        for _player in self._players:
            info = dict()
            info["player"] = _player
            info["total_point"] = []
            info["initial_ranking"] = elo_ratings[_player]
            info["opponents"] = []
            players_info.append(info)
        return players_info

    def update_players_info(self, players_info, total_points, opponents):
        """docstring"""
        for info in players_info:
            _player = info["player"]
            print(_player)
            print(total_points[_player])
            info["total_point"] = total_points[_player]
            info["opponents"] = opponents[_player]
        return players_info

    def get_attributes(self):
        """Get attribute names (without protected or private sign) and theirs values """
        attributes_info = basic_backend.get_attributes(self)
        return attributes_info

    def set_attrs(self, kwargs):
        basic_backend.set_attrs(self, kwargs)

    @classmethod
    def create_tournament(cls, attributes_values):
        # Retrieve the class type
        obj_type = globals()[cls.__name__]
        return basic_backend.create_item(attributes_values, obj_type)

    @classmethod
    def add_tournament(cls, tournaments, tournament):
        return basic_backend.add_item(tournaments, tournament)

    @classmethod
    def find_tournament(cls, tournaments, key, value):
        return basic_backend.find_item(tournaments, key, value)

    @classmethod
    def read_tournament(cls, tournaments, key, value):
        return basic_backend.read_item(tournaments, key, value)

    @classmethod
    def update_tournament(cls, tournaments, key, value, attributes_new_values):
        return basic_backend.update_item(tournaments, key, value, attributes_new_values)

    @classmethod
    def delete_tournament(cls, tournaments, key, value):
        return basic_backend.delete_item(tournaments, key, value)

    @staticmethod
    def get_attribute_names():
        t = Tournament()
        return t.get_attributes().keys()

    def __str__(self):
        """Print all attributes and theirs values of an object"""
        attr_str = basic_backend.get_str(self)
        return attr_str

    def __repr__(self):
        if self._name is not None:
            return self._name + " - date: " + str(self._date)
        else:
            return str(None)

if __name__ == '__main__':

    t = Tournament()
    # t.name = input("Enter the name of the tournament: ")
    # print("Enter the location with the following information: ")
    # building_number = input("Building number: ")
    # street = input("Street: ")
    # city = input("City: ")
    # zipcode = input("Zipcode: ")
    # location = location.Location(building_number, street, city, zipcode)
    #
    # t.location = location
    # t.date = input("Date of the tournament (dd/mm/yyyy): ")
    t.number_of_rounds = DEFAULT_NUMBER_OF_ROUNDS
    t.rounds = []
    # players = []
    # nb_player = 1
    # while True:
    #     print(f"{nb_player}. Enter the players {nb_player}: ")
    #     _fide_id = int(input("Fide id :"))
    #     first_name = input("First name: ")
    #     last_name = input("Last name: ")
    #     date_of_birth = input("Date of birth (dd/mm/yyyy): ")
    #     gender = input("Gender (male/female): ")
    #     ranking = input("Ranking (Elo rating): ")
    #     _player = player.Player(_fide_id, first_name, last_name, date_of_birth, gender, ranking)
    #     players.append(_player)
    #     print("Do you want to continue?")
    #     answer = input("yes/no :")
    #     if answer.lower() == "yes":
    #         nb_player += 1
    #     else:
    #         break
    # t.players = players
    t.players = player_list.players
    # while True:
    #     time_control = input("Enter time control (bullet/blitz/rapid): ")
    #     if time_control not in ["bullet", "blitz", "rapid"]:
    #         print("Re-enter")
    #         time_control = input("Enter time control (bullet/blitz/rapid): ")
    #     else:
    #         t.time_control = time_control
    #         break
    #
    # t.description = input("Enter your description :")
    # print(t)

    # ranking = ranking
    pairs = t.make_pairs_first_round()
    # _round = t.initialize_matches(pairs)
    total_points = t.initialize_total_points()
    opponents = t.initialize_opponents()
    elo_ratings = t.get_elo_ratings()
    players_info = t.initialize_players_info(elo_ratings)

    # print("*" * 10)
    # print("First pairs :")
    # # print(_round.matches)
    # for pair in pairs:
    #     print(pair[0].elo_rating, pair[1].elo_rating)
    # print("*" * 10)
    # print("At the initialisation: ")
    # print(f"total_points: {total_points}")
    # print(f"opponents: {opponents}")
    # print(f"elo_ratings: {elo_ratings}")
    # print(f"players_info: {players_info}")
    #
    round_index = 1
    while round_index <= DEFAULT_NUMBER_OF_ROUNDS:
        print(f"Make pairs for round {round_index}")
        if round_index == 1:
            pairs = t.make_pairs_first_round()
        else:
            pairs = t.make_pairs(players_info)

        _round = round_robin.Round()
        _round.name = "Round " + str(round_index)
        _round.date = date.today().strftime("%d/%m/%Y")
        matches = t.initialize_matches(pairs)
        _round.matches = matches
        _round.start_time = datetime.now().strftime("%H:%M:%S")
        t.update_round(_round)
        _round.end_time = datetime.now().strftime("%H:%M:%S")
        total_points = t.update_total_points(_round, total_points)
        opponents = t.update_opponents(_round, opponents)
        players_info = t.update_players_info(players_info, total_points, opponents)
        print("*" * 10)
        print(f'{round_index}. Round {round_index}')
        print(_round)
        print(f"total_points: {total_points}")
        print(f"opponents: {opponents}")
        print(f"players_info: {players_info}")
        print("*" * 10)
        round_index += 1
