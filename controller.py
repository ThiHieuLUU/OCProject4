import model
import view
import player_list


class Controller(object):

    def __init__(self, _model, _view):
        self.model = _model
        self.view = _view

    def input_time_control(self):
        # time_control = None
        while True:
            time_control = input("Enter time control (bullet/blitz/rapid): ")
            while time_control not in ["bullet", "blitz", "rapid"]:
                self.view.show_error("time control", "bullet/blitz/rapid")
                time_control = input("Re-enter time control (bullet/blitz/rapid): ")
            break
        return time_control

    # def input_players(self):
    #     self.view.show_request("players")
    #     players = []
    #     nb_player = 1
    #     while True:
    #         self.view.show_request(f"player {nb_player}")
    #         # print(f"{nb_player}. Enter the players {nb_player}: ")
    #         # _player_id = int(input("Fide id :"))
    #         first_name = input("First name: ")
    #         last_name = input("Last name: ")
    #         date_of_birth = input("Date of birth (dd/mm/yyyy): ")
    #         gender = input("Gender (male/female): ")
    #         ranking = input("Ranking (Elo rating): ")
    #         # assert ranking is int, 'Ranking must be integer'
    #         player_id = len(self.model.get_players()) + 1
    #         player = self.model.build_player(player_id, first_name, last_name, date_of_birth, gender, ranking)
    #         players.append(player)
    #         # Add to BDD
    #         self.model.add_player(player)
    #         self.view.show_question("add more player")
    #         res = input()
    #         if res.lower() == "y":
    #             nb_player += 1
    #         else:
    #             break
    #     return players

    def input_players(self):
        return player_list.players

    def input_location(self):
        self.view.show_request("location")
        building_number = input("Location: \nBuilding number: ")
        street = input("Street: ")
        city = input("City: ")
        zipcode = input("Zipcode: ")
        location = self.model.build_location(building_number, street, city, zipcode)
        return location

    def create_tournament(self):
        self.view.start_view()
        res = input()
        if res == 'y':
            name = input("Enter the name of the tournament: ")
            # print("Enter the location with the following information: ")
            date = input("Enter the date of the tournament (dd/mm/yyyy): ")
            number_of_rounds = int(input("Enter the number of rounds: "))
            description = input("Enter your description :")
            location = self.input_location()
            players = self.input_players()
            time_control = self.input_time_control()

            self.model.create_tournament(name, location, date, number_of_rounds, players, time_control, description)
            # self.model.tournament = tournament
            # return tournament
        else:
            return view.end_view()

    # def get_pairs_first_round(self):
    #     pairs = self.model.get_first_pairs()
    #     self.view.show_pairs(pairs, round_index=1)

    def get_pairs(self, round_index):
        pairs = self.model.get_pairs(round_index)
        self.view.show_pairs(pairs, round_index)

    def make_new_round(self):
        self.model.make_new_round()
        # the added round is the last round in the list of rounds
        last_round, last_round_index = self.model.get_last_round()
        self.view.show_round(last_round, last_round_index)

    def update_matches(self):
        # convention: always update the last round
        last_round, last_round_index = self.model.get_last_round()
        matches = last_round.matches
        self.view.show_updating_round(last_round_index)
        match_index = 1
        while match_index <= len(matches):
            match = matches[match_index - 1]  # ([player_1, score1], [player_2, score2])
            player1, player2 = self.model.get_players_from_match(match)

            self.view.show_updating_match(last_round_index, match_index)
            score1 = float(input(f'{player1}, score = '))
            score2 = float(input(f'{player2}, score = '))

            score_list = [0, 0.5, 1]
            if score1 in score_list and score2 in score_list and score1 + score2 == 1.0:
                # match[0][1] = score1  # update also to _round.matches
                # match[1][1] = score2
                self.model.update_match(match, score1, score2)
                match_index += 1
            else:
                self.view.show_error("score", "[0/0.5/1], sum of scores must be 1")
        print(matches)
        self.model.update_round(matches)
        last_round, last_round_index = self.model.get_last_round()
        self.view.show_round(last_round, last_round_index)

if __name__ == "__main__":
    # running controller function
    _model = model.Model()
    _view = view.View()
    controller = Controller(_model, _view)
    controller.create_tournament()
    controller.view.show_tournament_info(controller.model.tournament)
    round_index = 1
    controller.get_pairs(round_index)
    controller.make_new_round()
    controller.update_matches()
    round_index = 2
    controller.get_pairs(round_index)
    controller.make_new_round()
    controller.update_matches()
    round_index = 3
    controller.get_pairs(round_index)
    controller.make_new_round()
    controller.update_matches()
    round_index = 4
    controller.get_pairs(round_index)
    controller.make_new_round()
    controller.update_matches()
    # print(controller.model.tournament)
