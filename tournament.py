"""docstring"""


from datetime import datetime, date
import mvc_exceptions as mvc_exc
import round_robin
import player
import player_list
import match
import location

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
            
        print("*"*10)    
        print("First pairs")
        for pair in pairs:
            print(pair[0].elo_rating, pair[1].elo_rating)
        print("*" * 10)
        
        return pairs

    def make_pair(self, pair_index, player_1, not_yet_encountered_players):
        if len(not_yet_encountered_players) >= 1:
            player_2 = not_yet_encountered_players[0]
            # Eliminate the taken player_2 for the next time if it has to re-find player_2
            not_yet_encountered_players = not_yet_encountered_players[1:]
            pair = [player_1, player_2]
            return pair, not_yet_encountered_players
        else:
            return None, not_yet_encountered_players

    def make_pairs(self, players_info):
        """docstring"""
        pairs = []
        sorted_players_info = sorted(players_info, key=lambda k: (-k["total_point"], -k['initial_ranking']))

        player_number = len(sorted_players_info)
        if player_number % 2 == 1:
            player_number_ = player_number - 1
        else:
            player_number_ = player_number

        paired_player_number = 0

        pair_index = 1
        pair_number = int(player_number/2)

        # Each time, two players are taken.
        # If the numbers of players is odd, the treatment is only done to the numbers of players - 1

        # Each pair has its own player, built player_1 as dictionary in order to mark the player of which pair
        player_1_info = dict()
        player_1 = dict()
        sorted_players_info_dict = dict()
        sorted_players_info_dict[pair_index] = sorted_players_info
        while pair_index <= pair_number:
            player_1_info[pair_index] = sorted_players_info_dict[pair_index][0]
            player_1[pair_index] = player_1_info[pair_index]["player"]

            not_yet_encountered_players = [info for info in sorted_players_info_dict[pair_index] if info["player"]
                                           not in player_1_info[pair_index]["opponents"]] # stop at here
            # eliminate the player_1 in the list
            not_yet_encountered_players = not_yet_encountered_players[1:]
            pair, not_yet_encountered_players = self.make_pair(pair_index, player_1, not_yet_encountered_players)
            if pair is None:
                # return in the previous pair and re-make
                pair_index -= 1
            else:
                # pass to next pair
                pair_index += 1


            if len(not_yet_encountered_players) > 1:
                print("len =", len(not_yet_encountered_players))
                # Take the first element in the list which eliminates all the players encountered
                player_2_info = not_yet_encountered_players[0]
            else:
                raise("Player encountered all other players")
                # print(f"not_yet_encountered_players {not_yet_encountered_players}")
                # # If the player 1 encountered all other players, take the next element in the sorted list
                # player_2_info = sorted_players_info[1]

            # Each time, remove the pair of players has been made in the sorted list
            sorted_players_info = [element for element in sorted_players_info if element not in (
                player_1_info, player_2_info)]
            # Built pair
            pairs.append([player_1_info["player"], player_2_info["player"]])
            paired_player_number += 2

            print(f'{player_1_info["total_point"]} vs {player_2_info["total_point"]}; '
                  f'{player_1_info["player"].elo_rating} vs {player_2_info["player"].elo_rating}; '
                  f'{player_1_info["player"] in player_2_info["opponents"]} vs '
                  f'{player_2_info["player"] in player_1_info["opponents"]}')

        if player_number % 2 == 1:
            # Pair with none player if number of player is odd
            pairs.append([none_player, sorted_players_info[-1]["player"]])
            print(sorted_players_info[-1]["total_point"], sorted_players_info[-1]["player"].elo_rating)

        return pairs



    # def make_pairs(self, players_info):
    #     """docstring"""
    #     pairs = []
    #     # players_info = self.update_players_info(total_points, elo_ratings, opponents)
    #     # players_info = self.update_players_info(players_info, total_points, opponents)
    #
    #     # Initial ranking consist of player's Elo rating, the best player is the best Elo rating
    #     # Sort with decreasing order of total point and decreasing order of Elo rating
    #     # The best player with sorted result is in the first, the worst is in the last
    #     sorted_players_info = sorted(players_info, key=lambda k: (-k["total_point"], -k['initial_ranking']))
    #
    #     player_number = len(sorted_players_info)
    #     if player_number % 2 == 1:
    #         player_number_ = player_number - 1
    #     else:
    #         player_number_ = player_number
    #
    #     paired_player_number = 0
    #
    #     # Each time, two players are taken.
    #     # If the numbers of players is odd, the treatment is only done to the numbers of players - 1
    #     while paired_player_number < player_number_:
    #         player_1_info = sorted_players_info[0]
    #         not_yet_encountered_players = [info for info in sorted_players_info if info["player"] not in
    #                                        player_1_info["opponents"]]
    #         # eliminate the player_1 in the list
    #         not_yet_encountered_players = not_yet_encountered_players[1:]
    #
    #         if len(not_yet_encountered_players) > 1:
    #             print("len =", len(not_yet_encountered_players))
    #             # Take the first element in the list which eliminates all the players encountered
    #             player_2_info = not_yet_encountered_players[0]
    #         else:
    #             raise("Player encountered all other players")
    #             # print(f"not_yet_encountered_players {not_yet_encountered_players}")
    #             # # If the player 1 encountered all other players, take the next element in the sorted list
    #             # player_2_info = sorted_players_info[1]
    #
    #         # Each time, remove the pair of players has been made in the sorted list
    #         sorted_players_info = [element for element in sorted_players_info if element not in (
    #             player_1_info, player_2_info)]
    #         # Built pair
    #         pairs.append([player_1_info["player"], player_2_info["player"]])
    #         paired_player_number += 2
    #
    #         print(f'{player_1_info["total_point"]} vs {player_2_info["total_point"]}; '
    #               f'{player_1_info["player"].elo_rating} vs {player_2_info["player"].elo_rating}; '
    #               f'{player_1_info["player"] in player_2_info["opponents"]} vs '
    #               f'{player_2_info["player"] in player_1_info["opponents"]}')
    #
    #     if player_number % 2 == 1:
    #         # Pair with none player if number of player is odd
    #         pairs.append([none_player, sorted_players_info[-1]["player"]])
    #         print(sorted_players_info[-1]["total_point"], sorted_players_info[-1]["player"].elo_rating)
    #
    #     return pairs

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

    t = Tournament()
    t.name = input("Enter the name of the tournament: ")
    print("Enter the location with the following information: ")
    building_number = input("Building number: ")
    street = input("Street: ")
    city = input("City: ")
    zipcode = input("Zipcode: ")
    location = location.Location(building_number, street, city, zipcode)

    t.location = location
    t.date = input("Date of the tournament (dd/mm/yyyy): ")
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
    while True:
        time_control = input("Enter time control (bullet/blitz/rapid): ")
        if time_control not in ["bullet", "blitz", "rapid"]:
            print("Re-enter")
            time_control = input("Enter time control (bullet/blitz/rapid): ")
        else:
            t.time_control = time_control
            break

    t.description = input("Enter your description :")
    print(t)

    # ranking = ranking
    pairs = t.make_pairs_first_round()
    # _round = t.initialize_matches(pairs)
    total_points = t.initialize_total_points()
    opponents = t.initialize_opponents()
    elo_ratings = t.get_elo_ratings()
    players_info = t.initialize_players_info(elo_ratings)

    print("*" * 10)
    print("First pairs :")
    # print(_round.matches)
    for pair in pairs:
        print(pair[0].elo_rating, pair[1].elo_rating)
    print("*" * 10)
    print("At the initialisation: ")
    print(f"total_points: {total_points}")
    print(f"opponents: {opponents}")
    print(f"elo_ratings: {elo_ratings}")
    print(f"players_info: {players_info}")
    #
    round_index = 1
    while round_index <= DEFAULT_NUMBER_OF_ROUNDS:
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
        print("*"*10)
        print(f'{round_index}. Round {round_index}')
        print(_round)
        print(f"total_points: {total_points}")
        print(f"opponents: {opponents}")
        print(f"players_info: {players_info}")
        print("*" * 10)
        round_index += 1

