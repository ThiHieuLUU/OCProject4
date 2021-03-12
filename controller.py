#! /usr/bin/venv python3
# coding: utf-8

"""This module connects the View and Model in MVC pattern."""

from datetime import datetime

import chessmodel.model as model
import mvc_exceptions as mvc_exc
import constants as const
import view


class Controller:
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

        # Set time_control to begin the loop.
        time_control = ''
        # Start a loop that will run until the time control type is one of given types.
        while time_control.lower() not in const.TIME_CONTROL_LIST:
            # Ask the user for a time control type.
            time_control = input(f"Enter time control {const.TIME_CONTROL_LIST}: ")
            if time_control.lower() in const.TIME_CONTROL_LIST:
                break
            else:
                self.view.show_error("time control", const.TIME_CONTROL_LIST)
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
    #         gender = input("Gender (M/F): ").upper()
    #         ranking = input("Ranking (Elo rating): ")
    #
    #         _player = self.model.build_player(first_name, last_name, date_of_birth, gender, ranking)
    #         players.append(player)
    #
    #         self.view.show_question("add more player")
    #         res = input()
    #         if res.lower() in const.Y_RES:
    #             player_index += 1
    #         else:
    #             break
    #     return players

    def input_players(self):
        """Read a given list of players and use it as the players of the tournament."""

        return self.model.get_player_sample()

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

        date_format = const.DATE_FORMAT  # "%d/%m/%Y"
        while True:
            try:
                date_entry = input(msg)
                datetime.strptime(str(date_entry), date_format)
                break
            except ValueError:
                self.view.show_error("date", const.DATE_REQUEST)
        return date_entry

    def create_tournament(self):
        """Build a tournament from the input data."""

        res = input("Do you want to create a tournament [y/n]? ")
        if res.lower() in const.Y_RES:
            name = str(input("Enter the name of the tournament: "))
            _date = self.input_date("Enter the date of the tournament: ")
            number_of_rounds = self.input_int("Enter the number of rounds: ")
            description = input("Enter your description: ")
            location = self.input_location()
            players = self.input_players()
            time_control = self.input_time_control()

            self.model.create_tournament(name, location, _date, number_of_rounds, players, time_control, description)

            self.view.show_question("see the tournament's information")
            res = input()
            if res.lower() in const.Y_RES:
                self.view.show_tournament_info(self.model.tournament)

            input("You have created a tournament. Press Enter to continue...".upper())
        else:
            input("You did not create a tournament. Press Enter to continue...".upper())

    def show_pairs(self):
        """Get pairs of the next round in order to show these pairs to the user."""

        round_index = self.get_last_round_index() + 1
        try:
            # Players exist is a condition for taking place a tournament (get pairs, make round, update round).
            self.model.check_exist_players()
        except mvc_exc.EmptyListError as error:
            self.view.show_except_error(error)
            input("Press Enter to continue...".upper())
        else:
            try:
                # Check if the new_round/new pairs can be created.
                # The new round index must not be over the number of rounds.
                self.model.check_if_new_round()
            except mvc_exc.RoundIndexError as error:
                self.view.show_except_error(error)
                input("Press Enter to continue...".upper())
            else:
                # Do not need to check if at least a round has been already created.
                # Before the first round we have already the pairs if the players exist.
                nbr_rounds = self.model.tournament.number_of_rounds
                if round_index <= nbr_rounds:
                    self.view.show_question(f"see the pairs of the round {round_index}")
                    res = input()
                    if res.lower() in const.Y_RES:
                        pairs = self.model.get_pairs(round_index)
                        self.view.show_pairs(pairs, round_index)
                        input(f"You have seen the pairs of the round {round_index}. "
                              f"Press Enter to continue...".upper())

    def get_last_round_index(self):
        """Get the index of the last round in the list of rounds taken place."""

        return self.model.get_last_round_index()

    def make_new_round(self):
        """Start a round of the tournament and mark automatically the start time."""

        # The new round becomes the last round in the list of rounds.
        try:
            # Players exist is a condition for taking place a tournament (get pairs, make rounds, update rounds).
            self.model.check_exist_players()
        except mvc_exc.EmptyListError as error:
            self.view.show_except_error(error)
            input("Press Enter to continue...".upper())
        else:
            try:
                # Check if the new_round/new pairs can be created.
                # The new round index must not be over the number of rounds.
                self.model.check_if_new_round()
            except mvc_exc.RoundIndexError as error:
                self.view.show_except_error(error)
                input("Press Enter to continue...".upper())
            else:
                last_round_index = self.get_last_round_index()
                res = input(f"Do you want to start the round {last_round_index + 1} now {const.Y_N}? ".upper())
                if res.lower() in const.Y_RES:
                    now = datetime.now()
                    start_time = now.strftime("%H:%M:%S")

                    self.model.make_new_round(start_time)

                    last_round, last_round_index = self.model.get_last_round()
                    self.view.show_round(last_round, last_round_index)
                    input(f"You have started the round {last_round_index}. Press Enter to continue...".upper())

    def update_matches(self):
        """Update the scores of a match with input scores from user."""

        # Convention: always update the last round.
        try:
            # Players exist is a condition for taking place a tournament (get pairs, make round, update round).
            self.model.check_exist_players()
        except mvc_exc.EmptyListError as error:
            self.view.show_except_error(error)
            input("Press Enter to continue...".upper())
        else:
            try:
                # Check if at least a round has already created/started in the tournament.
                last_round, last_round_index = self.model.get_last_round()
            except mvc_exc.RoundIndexError as error:
                self.view.show_except_error(error)
                input("Press Enter to continue...".upper())
            else:
                matches = last_round.matches
                self.view.show_updating_round(last_round_index)
                match_index = 1
                while match_index <= len(matches):
                    # Each match is an object with an attribute 'match' where:
                    # match = ([player_1, score1], [player_2, score2])
                    match = matches[match_index - 1]
                    player1, player2 = self.model.get_players_from_match(match)

                    self.view.show_updating_match(last_round_index, match_index)
                    score1 = float(input(f'{player1}, score = '))
                    score2 = float(input(f'{player2}, score = '))

                    score_list = const.SCORE_LIST
                    if score1 in score_list and score2 in score_list and score1 + score2 == 1.0:
                        self.model.update_match(match, score1, score2)
                        match_index += 1
                    else:
                        self.view.show_error("score", f"{score_list}, sum of scores must be 1")

                self.model.update_round(matches)
                self.view.show_question(f"see the last round updated (round {last_round_index})")
                res = input()
                if res.lower() in const.Y_RES:
                    self.view.show_round(last_round, last_round_index)
                    input(f"You have updated the scores for the Round {last_round_index}."
                          " Press Enter to continue...".upper())

    def end_round(self):
        """Ask the user if the round is finished and then mark automatically the end time for the round."""

        try:
            # Players exist is a condition for taking place a tournament (get pairs, make round, update round).
            self.model.check_exist_players()
        except mvc_exc.EmptyListError as error:
            self.view.show_except_error(error)
            input("Press Enter to continue...".upper())
        else:
            try:
                # Check if at least a round has been already created/started in the tournament.
                last_round, last_round_index = self.model.get_last_round()
            except mvc_exc.RoundIndexError as error:
                self.view.show_except_error(error)
                input("Press Enter to continue...".upper())
            else:
                res = input(f"Is the round {last_round_index} finished {const.Y_N}? ".upper())
                if res.lower() in const.Y_RES:
                    now = datetime.now()
                    current_time = now.strftime("%H:%M:%S")
                    last_round, last_round_index = self.model.get_last_round()
                    last_round.end_time = current_time
                    self.view.show_round(last_round, last_round_index)
                    input(f"You have finished the round {last_round_index}. Press Enter to continue...".upper())

    def show_items(self, fct, _obj):
        """Build a pattern for getting and showing players, rounds, matches."""

        try:
            items = fct(_obj)
            self.view.show_items(items)
        except mvc_exc.EmptyListError as error:
            self.view.show_except_error(error)
        input("Press Enter to continue...".upper())

    def show_info_tournament(self, _tournament):
        """Get and show information of a given tournament."""

        self.view.show_tournament_info(_tournament)
        input("Press Enter to continue...".upper())

    def show_players(self, _tournament):
        """Get and show players of a given tournament."""

        fct = self.model.get_players
        self.show_items(fct, _tournament)

    def show_rounds(self, _tournament):
        """Get and show the list of rounds of a given tournament."""

        fct = self.model.get_rounds
        self.show_items(fct, _tournament)

    def show_matches(self, _tournament):
        """Get and show the list of matches of a given tournament."""

        fct = self.model.get_matches
        self.show_items(fct, _tournament)

    def show_last_ranking(self, _tournament):
        """Get and show the last ranking of a given tournament."""
        try:
            last_ranking, last_round_index = self.model.get_last_ranking(_tournament)
        except mvc_exc.EmptyListError as error:
            self.view.show_except_error(error)
            input("Press Enter to continue...".upper())
        else:
            self.view.show_last_ranking(last_ranking, last_round_index)
            input("Press Enter to continue...".upper())

    def show_info_new_tournament(self):
        """Get and show information of the current tournament."""

        self.view.show_tournament_info(self.model.tournament)
        input("Press Enter to continue...".upper())

    def show_players_new_tournament(self):
        """Get and show the list of players of the current tournament."""

        self.show_players(self.model.tournament)

    def show_rounds_new_tournament(self):
        """Get and show the list of rounds of the current tournament."""

        self.show_rounds(self.model.tournament)

    def show_matches_new_tournament(self):
        """Show the list of matches of the current tournament."""

        self.show_matches(self.model.tournament)

    def show_last_ranking_new_tournament(self):
        """Show the ranking of the last round of the current tournament.

        The last round may not be the final round.
        """

        try:
            self.model.check_exist_players()
        except mvc_exc.EmptyListError as error:
            self.view.show_except_error(error)
            input("Press Enter to continue...".upper())
        else:
            last_ranking = self.model.get_last_ranking_new_tournament()
            last_round_index = self.model.get_last_round_index()
            self.view.show_last_ranking(last_ranking, last_round_index)
            input("Press Enter to continue...".upper())

    def get_tournaments(self):
        """Get the list of all tournaments from the database (with TinyDB here)."""

        return self.model.get_tournaments()

    def show_actors_alphabetical_order(self):
        """Get from the database and show the list of all actors in the alphabetical order."""

        actors = self.model.get_actors_alphabetical_order()
        self.view.show_items(actors)
        input("Press Enter to continue...".upper())

    def show_actors_ranking_order(self):
        """Get from the database and show the list of all actors in the descending ranking order."""

        actors = self.model.get_actors_ranking_order()
        self.view.show_items(actors)
        input("Press Enter to continue...".upper())
