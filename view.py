# VIEW
# model_view_controller.py
"""docstring"""
class View():
    """docstring"""

    @staticmethod
    def start_view():
        print
        'MVC - the simplest example'
        print
        'Do you want to see everyone in my db?[y/n]'

    @staticmethod
    def show_tournament(tournament):
        """docstring"""
        print('**************************************************************')
        print('Tournament information:')
        print(tournament)
        print('**************************************************************')

    @staticmethod
    def show_round(round):
        """docstring"""
        print('**************************************************************')
        print('Round information:')
        print(round)
        print('**************************************************************')

    @staticmethod
    def show_player(player):
        """docstring"""
        print('**************************************************************')
        print('Player information:')
        print(player)
        print('**************************************************************')

    @staticmethod
    def show_match(match):
        """docstring"""
        print('**************************************************************')
        print('match information:')
        print(match)
        print('**************************************************************')

    @staticmethod
    def show_tournaments(tournaments):
        """docstring"""
        print('**************************************************************')
        print('List of tournaments:')
        index = 1
        for tournament in tournaments:
            print(f'{index}.Tournament:')
            print(tournament)
            index += 1
        print('**************************************************************')

    @staticmethod
    def show_rounds(rounds):
        """docstring"""
        print('**************************************************************')
        print('List of rounds:')
        index = 1
        for round in rounds:
            print(f'{index}. Round:')
            print(round)
            index += 1
        print('**************************************************************')

    @staticmethod
    def show_players(players):
        """docstring"""
        print('**************************************************************')
        print('List of players:')
        index = 1
        for player in players:
            print(f'{index}. Player:')
            print(player)
            index += 1
        print('**************************************************************')

    @staticmethod
    def show_matchs(matchs):
        """docstring"""
        print('**************************************************************')
        print('List of matchs:')
        index = 1
        for match in matchs:
            print(f'{index}. Match:')
            print(match)
            index += 1
        print('**************************************************************')

    @staticmethod
    def show_tournament_ranking(tournament_rankings):
        """docstring"""
        print('**************************************************************')
        print('List of tournament rankings:')
        index = 1
        for rank in rankings:
            print(f'{index}. {rank}')
            index += 1
        print('**************************************************************')

    @staticmethod
    def show_elo_rating():
        """docstring"""

