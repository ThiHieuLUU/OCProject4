#! /usr/bin/venv python3
# coding: utf-8

"""This module is used to display messages, information to user."""


class View:
    """The View class deals with how the data is presented to the user.
    Only a Controller should call View's methods.
    """

    @staticmethod
    def show_request(obj):
        """To display the request of entering input for an object."""

        print(f'Enter the information of {obj}: ')

    @staticmethod
    def show_error(key, value):
        """To display the request of re-entering value for a variable 'key'."""

        print(f'The {key} is not correct. Re-enter {key} ({value}): ')

    @staticmethod
    def show_question(action):
        """To display the yes-no request."""

        print("*" * 40)
        print(f'Do you want to {action} [y/n]? '.upper())

    @staticmethod
    def show_pairs(pairs, round_index):
        """To display the pairs of a chess round."""

        print("*" * 40)
        print(f"Pairs of the round {round_index}:".upper())
        for pair in pairs:
            print(pair)
        print("*" * 40)

    @staticmethod
    def show_round(_round, round_index):
        """To display the information of a chess round."""

        print("*" * 40)
        print(f"Information of the round {round_index}:".upper())
        print(_round)
        print("*" * 40)

    @staticmethod
    def show_round_error(error):
        """To display the error with a chess round (not having players, index over the number of rounds...)."""

        print("*" * 40)
        print(error)
        print("*" * 40)

    @staticmethod
    def show_updating_round(round_index):
        """To display the request for entering the result of matches of a round."""

        print("*" * 40)
        print(f"Enter the result of matches for the round {round_index}:".upper())
        print("*" * 40)

    @staticmethod
    def show_updating_match(round_index, match_index):
        """To display which match."""

        print(f"* Round {round_index}, match {match_index}:".upper())

    @staticmethod
    def show_last_ranking(last_ranking, last_round_index):
        """To display the ranking after a round, here that is the last round."""

        # Last_ranking is a list.
        # Its elements have the following format: [player, elo_ranking] or [player, total_point, elo_ranking]
        print("*" * 40)

        if last_round_index == 0:
            print("This is the elo ranking before starting the tournament:".upper())
            print('{:<10} {:<45} {:<12}'.format("Ranking", "Player", "Elo Ranking"))
            i = 1
            for item in last_ranking:
                print('{:<10} {:<45} {:<12}'.format(i, item[0], item[1]))
                i += 1
        else:
            print(f"This is the ranking after the round {last_round_index}:".upper())
            print('{:<10} {:<45}  {:<12}  {:<12}'.format("Ranking", "Player", "Total Point", "Elo Ranking"))
            i = 1
            for item in last_ranking:
                print('{:<10} {:<45}  {:<12}  {:<12}'.format(i, item[0], item[1], item[2]))
                i += 1
        print("*" * 40)

    @staticmethod
    def show_tournament_info(tournament):
        """To display all information of a tournament."""

        print("*" * 40)
        print("Information of the tournament:".upper())
        print(tournament)
        print("*" * 40)

    @staticmethod
    def show_except_error(error):
        """To display an exception error caught by the instruction 'try'."""

        print("*" * 40)
        print(error)
        print("*" * 40)

    @staticmethod
    def show_items(items):
        """To display a list of items."""

        print("*" * 40)
        if not items:
            print("Error: list is empty!")
        else:
            for index, item in enumerate(items):
                print(f'{index+1}. {item}')
        print("*" * 40)
