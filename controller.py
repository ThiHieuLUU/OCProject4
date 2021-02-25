from datetime import datetime, date

import model
import view
import player_list


class Controller(object):

    def __init__(self):
        self.model = model.Model()
        self.view = view.View()

    def input_time_control(self):
        while True:
            time_control = input("Enter time control (bullet/blitz/rapid): ")
            while time_control not in ["bullet", "blitz", "rapid"]:
                self.view.show_error("time control", "bullet/blitz/rapid")
                time_control = input("Re-enter time control (bullet/blitz/rapid): ")
            break
        return time_control

    def input_int(self, msg):
        while True:
            try:
                int_entry = int(input(msg))
                break
            except ValueError as e:
                self.view.show_error("input", "integer")
        return int_entry

    # def input_players(self):
    #     self.view.show_request("players")
    #     players = []
    #     player_index = 1
    #     while True:
    #         self.view.show_request(f"player {player_index}")
    #         first_name = input("First name: ")
    #         last_name = input("Last name: ")
    #         date_of_birth = self.input_date("Date of birth: ")
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
    #             player_index += 1
    #         else:
    #             break
    #     return players

    @staticmethod
    def input_players():
        return player_list.players

    def input_location(self):
        self.view.show_request("location")
        building_number = input("Location: \nBuilding number: ")
        street = input("Street: ")
        city = input("City: ")
        zipcode = input("Zipcode: ")
        location = self.model.build_location(building_number, street, city, zipcode)
        return location

    def input_date(self, msg):
        # self.view.show_message(f"{msg}")
        date_format = "%d/%m/%Y"
        while True:
            try:
                date_entry = input(msg)
                datetime.strptime(str(date_entry), date_format)
                break
            except ValueError as e:
                self.view.show_error("date", "dd/mm/yyyy")
        return date_entry

    def create_tournament(self):
        self.view.show_question("create a tournament")
        res = input()
        if res == 'y':
            name = str(input("Enter the name of the tournament: "))
            date_ = self.input_date("Enter the date of the tournament: ")
            number_of_rounds = self.input_int("Enter the number of rounds: ")
            description = input("Enter your description: ")
            location = self.input_location()
            players = self.input_players()
            time_control = self.input_time_control()

            self.model.create_tournament(name, location, date_, number_of_rounds, players, time_control, description)
        else:
            return self.view.end_view()

    def get_pairs(self, round_index):
        pairs = self.model.get_pairs(round_index)
        self.view.show_question(f"see the pairs of the round {round_index}")
        res = input()
        if res.lower() in ["y", "Yes"]:
            self.view.show_pairs(pairs, round_index)
        else:
            self.view.next_view()

    def make_new_round(self):
        # The new round becomes the last round in the list of rounds
        self.model.make_new_round()
        last_round, last_round_index = self.model.get_last_round()
        self.view.show_round(last_round, last_round_index)

    def update_matches(self):
        # Convention: always update the last round
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
                self.model.update_match(match, score1, score2)
                match_index += 1
            else:
                self.view.show_error("score", "[0/0.5/1], sum of scores must be 1")
        self.model.update_round(matches)
        last_round, last_round_index = self.model.get_last_round()
        self.view.show_round(last_round, last_round_index)

    def run_tournament(self):
        self.create_tournament()
        try:
            nb_rounds = self.model.get_number_of_rounds()
            round_index = 1
            while round_index <= nb_rounds:
                self.get_pairs(round_index)
                self.make_new_round()
                self.update_matches()
                round_index += 1
        except TypeError:
            print("Something is wrong. Tournament is not happened!")
        else:
            print("All is done".upper())


if __name__ == "__main__":
    controller = Controller()
    controller.view.start_view()
    controller.run_tournament()


