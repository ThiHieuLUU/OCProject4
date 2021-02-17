"""docstring"""
# A faire : round idex pour appler fonction pair
# Générer temps pour round
import datetime
import mvc_exceptions as mvc_exc
import location as loc
import round_robin
import player
import player_list
import match

# default_number_of_rounds = 4
DEFAULT_NUMBER_OF_ROUNDS = 4

none_player = player.Player()


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
        date_format = "%d-%m-%Y"
        if datetime.datetime.strptime(str(new_date), date_format):
            print("This is the correct date string date_format.")
            self._date = new_date
        else:
            raise mvc_exc.DateError('Incorrect date date_format. It should be DD-MM-YYYY')

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
        
    def get_initial_rankings(self):
        """docstring"""
        initial_rankings = dict()
        for _player in self._players:
            initial_rankings[_player] = _player.ranking
        return initial_rankings

    def make_pairs_first_round(self):
        """docstring"""
        pairs = []
        sorted_players = sorted(self._players, key=lambda p: p.ranking, reverse=True)
        half_number = int(len(self._players) / 2)

        for index in range(half_number):
            pairs.append([sorted_players[index], sorted_players[half_number + index]])

        if len(self._players) % 2 == 1:
            pairs.append([none_player, sorted_players[-1]])
        return pairs


    def make_pairs(self, player_info_list, total_points, opponent_list):
        """docstring"""
        pairs = []
        # player_info_list = self.update_player_info_list(total_points, initial_rankings, opponent_list)
        player_info_list = self.update_player_info_list(player_info_list, total_points, opponent_list)

        # Initial ranking consist of player's Elo rating, the best player is the best Elo rating
        # Sort with decreasing order of total point and decreasing order of Elo rating
        # The best player with sorted result is in the first, the worst is in the last
        sorted_player_info_list = sorted(player_info_list, key=lambda k: (-k["total_point"], -k['initial_ranking']))

        player_number = len(sorted_player_info_list)
        if player_number % 2 == 1:
            player_number_ = player_number - 1
        else:
            player_number_ = player_number

        paired_player_number = 0

        # Each time, two players are taken.
        # If the numbers of players is odd, the treatment is only done to the numbers of players - 1
        while paired_player_number < player_number_:
            print("paired_nb = ", paired_player_number)
            print("len=", len(sorted_player_info_list))
            player_1_info = sorted_player_info_list[0]
            not_encountered_player_list = [info for info in sorted_player_info_list if info["player"] not in
                                           player_1_info["opponents"]]

            if not not_encountered_player_list:
                # Take the first element in the list which eliminates all the players encountered
                player_2_info = not_encountered_player_list[0]
            else:
                # If the player 1 encountered all other players, take the next element in the sorted list
                player_2_info = sorted_player_info_list[1]

            # Each time, remove the pair of players has been made in the sorted list
            sorted_player_info_list = [element for element in sorted_player_info_list if element not in (
                player_1_info, player_2_info)]
            # Built pair
            pairs.append([player_1_info["player"], player_2_info["player"]])
            paired_player_number += 2

        if player_number % 2 == 1:
            # Pair with none player if number of player is odd
            pairs.append([none_player, sorted_player_info_list[-1]["player"]])
        print(pairs)
        return pairs
    
    @staticmethod
    def initialize_round_with_pairs(pairs):
        """docstring"""
        _round = round_robin.Round()
        _round.matches = []
        for pair in pairs:
            m = match.Match(pair[0], 0, pair[1], 0)
            _round.matches.append(m.match)
        return _round

    def update_round_result(self, _round):
        """docstring"""
        matches = _round.matches
        match_index = 1
        while match_index <= len(matches):
            match = matches[match_index - 1]  # ([player1, score1], [player2, score2])
            print(match)
            none_player = player.Player()
            if match[0][0] != none_player and match[1][0] != none_player:
                print(f"Enter the scores of the match {match_index}")
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
                print("odd nb", match)

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

    def initialize_opponent_list(self):
        """docstring"""
        opponent_list = dict()
        for _player in self._players:
            opponent_list[_player] = []
        return opponent_list

    @staticmethod
    def update_opponent_list(_round, opponent_list):
        """docstring"""
        for match in _round.matches:
            # match structure: ([player1, score1], [player2, score2])
            if match[0][0] != none_player and match[1][0] != none_player:  # odd number of players
                opponent_list[match[0][0]].append(match[1][0])
                opponent_list[match[1][0]].append(match[0][0])
        return opponent_list
    
    def initialize_player_info_list(self, initial_rankings):
        """docstring"""
        player_info_list = []
        for _player in self._players:
            info = dict()
            info["player"] = _player
            # info["total_point"] = total_points[_player]
            info["initial_ranking"] = initial_rankings[_player]
            # info["opponents"] = opponents[_player]
            player_info_list.append(info)
        return player_info_list
    
    def update_player_info_list(self, player_info_list, total_points, opponents):
        """docstring"""
        for info in player_info_list:
            _player = info["player"]
            print(_player)
            print(total_points[_player])
            info["total_point"] = total_points[_player]
            info["opponents"] = opponents[_player]
        return player_info_list

    # def update_player_info_list(self, total_points, initial_rankings, opponents):
    #     """docstring"""
    #     player_info_list = []
    #     for _player in self._players:
    #         info = dict()
    #         info["player"] = _player
    #         info["total_point"] = total_points[_player]
    #         info["initial_ranking"] = initial_rankings[_player]
    #         info["opponents"] = opponents[_player]
    #         player_info_list.append(info)
    #     return player_info_list

    def get_attributes(self):
        """Get all attribute's names (without protected or private sign) and theirs values """
        attr_names = []

        protected_sign = "_"
        private_sign = "_" + type(self).__name__ + "__"

        for attribute_name in self.__dict__:
            # in case of protected or private attribute, retrieve only true name of attribute
            if attribute_name.startswith(private_sign):
                attribute_name = attribute_name[len(private_sign):]
            elif attribute_name.startswith(protected_sign):
                attribute_name = attribute_name[1:]

            attr_names.append(attribute_name)
        return attr_names, list(self.__dict__.values())

    def __str__(self):
        """Print all attributes and theirs values for an object"""
        attr_names, attr_values = self.get_attributes()
        attr_str = ""

        for attr_name, attr_value in zip(attr_names, attr_values):
            attr_str += str(attr_name).capitalize() + ': ' + str(attr_value) + "\n"

        return attr_str


if __name__ == '__main__':
    # input_data = b'\x00\x10' #
    t = Tournament()
    print(t)
    print("==")
    t.name = "tournament 1"
    t.location = "10 rue de Fontenay"
    t.date = "27-12-2020"
    # "bullet", "blitz", and "rapid".
    t.players = player_list.players
    t.time_control = "bullet"
    t.description = "Local tournament"
    print(t)
    first_pairs = t.make_pairs_first_round()
    print(first_pairs)
    # for p in first_pairs:
    #     print(p[0].ranking, p[1].ranking)
    _round = t.initialize_round_with_pairs(first_pairs)
    t.rounds.append(_round)
    print(t)
    t.update_round_result(_round)
    print(t)
    print(t.rounds[0].matches)
    total_points = t.initialize_total_points()
    total_points = t.update_total_points(_round, total_points)
    print("===")
    print(total_points)
    opponent_list = t.initialize_opponent_list()
    print(opponent_list)
    t.update_opponent_list(_round, opponent_list)
    print(opponent_list)
    initial_rankings = t.get_initial_rankings()
    print(initial_rankings)
    player_info =t.initialize_player_info_list(initial_rankings)
    player_info = t.update_player_info_list(player_info, total_points, opponent_list)
    print(player_info)
    from operator import itemgetter

    # The two sorts are increasing
    # sorted_player_info = sorted(player_info, key=itemgetter("total_point", "initial_ranking"))
    # sorted_player_info_list = sorted(player_info, key=lambda k: (-k["total_point"], k['initial_ranking']))
    # for item in sorted_player_info_list:
    #     print(item["total_point"], item["initial_ranking"])

    pairs = t.make_pairs(player_info, total_points, opponent_list)
    _round = t.initialize_round_with_pairs(pairs)
    t.rounds.append(_round)
    print(t)
    t.update_round_result(_round)
    print(t)
    print(t.rounds[-1].matches)
    total_points = t.update_total_points(_round, total_points)
    print(total_points)


    # t.update_opponent_list(_round, opponent_list)

    # t.make_pairs(total_points, opponent_list, initial_rankings)

    # players = player_list.players
