class View(object):

    @staticmethod
    def start_view():
        print('**************************************************************')
        print('Welcome to the chess application!'.upper())
        print('Do you want to create a tournament?[y/n]: ')

    @staticmethod
    def end_view():
        print('Goodbye!')

    @staticmethod
    def show_request(event):
        print(f'Enter the information of {event}: ')

    @staticmethod
    def show_error(key, value):
        print(f'The {key} is not correct. Re-enter {key} ({value}): ')

    @staticmethod
    def show_question(action):
        print(f'Do you want to {action} [y/n]? ')

    @staticmethod
    def show_pairs(pairs, round_index):
        print("*" * 10)
        print(f"Pairs of the round {round_index}:".upper())
        for pair in pairs:
            print(pair)
            # print(f'{pair[0]} \t {pair[1]}')
        print("*" * 10)

    @staticmethod
    def show_round(_round, round_index):
        print("*" * 10)
        print(f"Information of the round {round_index}:".upper())
        print(_round)
        print("*" * 10)

    @staticmethod
    def show_updating_round(round_index):
        print("*" * 10)
        print(f"Enter result of the matches for the round {round_index}:".upper())
        print("*" * 10)

    @staticmethod
    def show_updating_match(round_index, match_index):
        print(f"- Round {round_index}, match {match_index}:".upper())


    @staticmethod
    def show_tournament_info(tournament):
        print("*" * 10)
        print(f"information of the tournament:".upper())
        print(tournament)
        print("*" * 10)
