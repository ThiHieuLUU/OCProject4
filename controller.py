#! /usr/bin/venv python3
# coding: utf-8

"""This module connect the View and Model in mvc pattern."""

from datetime import datetime, date

import model
import view
import constants as const
import mvc_exceptions as mvc_exc
import player


class Controller(object):
    """The Controller class associates the user input to a Model and a View.
    The Controller class handles the user's inputs, invokes Model's methods to
    alter the data, and calls specific View's methods to present the data back
    to the user. Model and View should be initialized by the Controller.
    """

    def __init__(self):
        self.model = model.Model()
        self.view = view.View()

    def input_time_control(self):
        """To control the input for the time control of the tournament."""

        while True:
            time_control = input("Enter time control (bullet/blitz/rapid): ")
            while time_control.lower() not in ["bullet", "blitz", "rapid"]:
                self.view.show_error("time control", "bullet/blitz/rapid")
                time_control = input("Re-enter time control (bullet/blitz/rapid): ")
            break
        return time_control

    def input_int(self, msg):
        """To control the input for the number of rounds of the tournament."""

        while True:
            try:
                int_entry = int(input(msg))
                break
            except ValueError:
                self.view.show_error("input", "integer")
        return int_entry

    # def input_players(self):
    #     """To control the input for the list of players of the tournament."""
    #
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
        """Read a given list of players and use it as the players of the tournament."""

        return player.players

    def input_location(self):
        """To control the input for the location of the tournament."""

        self.view.show_request("location")
        building_number = input("Location: \nBuilding number: ")
        street = input("Street: ")
        city = input("City: ")
        zipcode = input("Zipcode: ")
        location = self.model.build_location(building_number, street, city, zipcode)
        return location

    def input_date(self, msg):
        """To control the input for the date of the tournament."""

        date_format = "%d/%m/%Y"
        while True:
            try:
                date_entry = input(msg)
                datetime.strptime(str(date_entry), date_format)
                break
            except ValueError as e:
                self.view.show_error("date", "d/m/y")
        return date_entry

    def create_tournament(self):
        """Build a tournament from the input data."""

        res = input("Do you want to create a tournament [y/n]? ")
        if res == 'y':
            name = str(input("Enter the name of the tournament: "))
            _date = self.input_date("Enter the date of the tournament: ")
            number_of_rounds = self.input_int("Enter the number of rounds: ")
            description = input("Enter your description: ")
            location = self.input_location()
            players = self.input_players()
            time_control = self.input_time_control()

            self.model.create_tournament(name, location, _date, number_of_rounds, players, time_control, description)

            self.view.show_question(f"see the tournament's information")
            res = input()
            if res.lower() in ["y", "yes"]:
                self.view.show_tournament_info(self.model.tournament)

            input("You have created a tournament. Press Enter to continue...".upper())
            return self.model.tournament

        else:
            input("You did not create a tournament. Press Enter to continue...".upper())
            return None

    def get_pairs(self, round_index):
        """Get pairs of each round in order to show to the user."""

        try:
            self.model.check_exist_players()

            nbr_rounds = self.model.tournament.number_of_rounds
            if round_index <= nbr_rounds:
                self.view.show_question(f"see the pairs of the round {round_index}")
                res = input()
                if res.lower() in ["y", "yes"]:
                    pairs = self.model.get_pairs(round_index)
                    self.view.show_pairs(pairs, round_index)
                    input(f"You have seen the pairs of the round {round_index}. Press Enter to continue...".upper())
            else:
                self.view.show_round_error(f"You can not get the pairs for the round {round_index} "
                                           f"because the number of rounds is limited by {nbr_rounds}.".upper())
                input(f"Press Enter to continue...".upper())

        except mvc_exc.EmptyListError as e:
            self.view.show_except_error(e)
            input(f"Press Enter to continue...".upper())

        except mvc_exc.RoundIndexError as e:
            self.view.show_except_error(e)
            input(f"Press Enter to continue...".upper())

    def get_last_round_index(self):
        """Get the index of the last round in the list of rounds taken place."""

        return self.model.get_last_round_index()

    def make_new_round(self):
        """Start a round of the tournament and mark automatically the start time."""

        # The new round becomes the last round in the list of rounds.
        try:
            self.model.check_exist_players()

            last_round_index = self.get_last_round_index()
            nbr_rounds = self.model.tournament.number_of_rounds
            if last_round_index <= nbr_rounds - 1:
                res = input(f"Do you want to start the round {last_round_index + 1} now {const.y_n}? ".upper())
                if res.lower() in const.y_res:
                    now = datetime.now()
                    start_time = now.strftime("%H:%M:%S")

                    self.model.make_new_round(start_time)

                last_round, last_round_index = self.model.get_last_round()
                self.view.show_round(last_round, last_round_index)
                input(f"You have started the round {last_round_index}. Press Enter to continue...".upper())
            else:
                self.view.show_round_error(
                    f"You can not start the new round (round {last_round_index + 1}) because the "
                    f"number of rounds is limited by {nbr_rounds}.".upper())
                input(f"Press Enter to continue...".upper())

        except mvc_exc.EmptyListError as e:
            self.view.show_except_error(e)
            input(f"Press Enter to continue...".upper())

    def update_matches(self):
        """Update the scores of a match with input scores from user."""

        # Convention: always update the last round
        try:
            self.model.check_exist_players()

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
            self.view.show_question(f"see the last round updated (round {last_round_index})")
            res = input()
            if res.lower() in ["y", "yes"]:
                self.view.show_round(last_round, last_round_index)

            input(f"You have updated the scores for the Round {last_round_index}. Press Enter to continue...".upper())

        except mvc_exc.EmptyListError as e:
            self.view.show_except_error(e)
            input(f"Press Enter to continue...".upper())

        except TypeError:
            self.view.show_except_error("Can not update matches because there is no round at the moment!")
            input(f"Press Enter to continue...".upper())

    def end_round(self):
        """Ask the user if the round is finished and mark automatically the end time."""

        try:
            self.model.check_exist_players()

            last_round, last_round_index = self.model.get_last_round()
            res = input(f"Is the round {last_round_index} finished {const.y_n}? ".upper())
            if res.lower() in const.y_res:
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                last_round.end_time = current_time

            self.view.show_round(last_round, last_round_index)
            input(f"You have finished the round {last_round_index}. Press Enter to continue...".upper())

        except mvc_exc.EmptyListError as e:
            self.view.show_except_error(e)
            input(f"Press Enter to continue...".upper())

    def get_last_ranking(self):
        """Get and show the ranking of the last round."""

        try:
            self.model.check_exist_players()

            last_ranking = self.model.get_last_ranking()
            last_round_index = self.model.get_last_round_index()
            self.view.show_last_ranking(last_ranking, last_round_index)
        except mvc_exc.EmptyListError as e:
            self.view.show_except_error(e)
        input("Press Enter to continue...".upper())

    def get_info_tournament(self):
        """Get and show information of the tournament."""

        self.view.show_tournament_info(self.model.tournament)
        input("Press Enter to continue...".upper())

    def get_items(self, fct):
        """Build a pattern for getting and showing players, rounds, matches."""

        try:
            items = fct()
            self.view.show_items(items)
        except mvc_exc.EmptyListError as e:
            self.view.show_except_error(e)
        input("Press Enter to continue...".upper())

    def get_players(self):
        """Get and show players."""

        fct = self.model.get_players
        self.get_items(fct)

    def get_rounds(self):
        """Get and show the list of rounds."""

        fct = self.model.get_rounds
        self.get_items(fct)

    def get_matches(self):
        """Get and show the list of matches."""

        try:
            matches = self.model.get_matches()
            self.view.show_items(matches)
        except mvc_exc.EmptyListError as e:
            self.view.show_except_error(e)
        input("Press Enter to continue...".upper())
