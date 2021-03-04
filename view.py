#! /usr/bin/venv python3
# coding: utf-8

"""This module is used to display all messages, information to user."""


class View(object):
    """The View class deals with how the data is presented to the user.
    A View should never call its own methods. Only a Controller should do it.
    """

    @staticmethod
    def show_request(obj):
        print(f'Enter the information of {obj}: ')

    @staticmethod
    def show_error(key, value):
        print(f'The {key} is not correct. Re-enter {key} ({value}): ')

    @staticmethod
    def show_question(action):
        print("*" * 40)
        print(f'Do you want to {action} [y/n]? '.upper())

    @staticmethod
    def show_pairs(pairs, round_index):
        print("*" * 40)
        print(f"Pairs of the round {round_index}:".upper())
        for pair in pairs:
            print(pair)
            # print(f'{pair[0]} \t {pair[1]}')
        print("*" * 40)

    @staticmethod
    def show_round(_round, round_index):
        print("*" * 40)
        print(f"Information of the round {round_index}:".upper())
        print(_round)
        print("*" * 40)

    def show_round_error(self, error):
        print("*" * 40)
        print(error)
        print("*" * 40)

    @staticmethod
    def show_updating_round(round_index):
        print("*" * 40)
        print(f"Enter the result of matches for the round {round_index}:".upper())
        print("*" * 40)

    @staticmethod
    def show_updating_match(round_index, match_index):
        print(f"* Round {round_index}, match {match_index}:".upper())

    def show_last_ranking(self, last_ranking, last_round_index):
        # last_ranking is a list. Its element is also a list of type: [player, elo_ranking] or [player,
        # total_point, elo_ranking]
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
        print("*" * 40)
        print(f"information of the tournament:".upper())
        print(tournament)
        print("*" * 40)

    @staticmethod
    def show_except_error(e):
        print("*" * 40)
        print(e)
        print("*" * 40)

    @staticmethod
    def show_items(items):
        print("*" * 40)
        if items is not None and len(items) > 0:
            for item in items:
                print(item)
        else:
            print("For the moment, there is any element in the list!")
        print("*" * 40)
