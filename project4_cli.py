"""This module is used as a CLI (command line interface) for user in order to:
- create and take place a new tournament
- See information of previous tournaments (players, rounds, matches, ranking)
- See information of all players (actors) coming from previous tournaments.

"""

from consolemenu import ConsoleMenu, SelectionMenu, MenuFormatBuilder
from consolemenu.items import FunctionItem, SubmenuItem
from consolemenu.format import MenuBorderStyleType

from controller import Controller as Controller

controller = Controller()


def create_tournament():
    controller.create_tournament()


def get_pairs():
    last_round_index = controller.get_last_round_index()
    # Pairs for next round
    controller.get_pairs(last_round_index + 1)


def make_new_round():
    controller.make_new_round()


def update_matches():
    controller.update_matches()


def end_round():
    controller.end_round()


def get_last_ranking_new_tournament():
    controller.get_last_ranking_new_tournament()


def get_info_new_tournament():
    controller.get_info_new_tournament()


def get_rounds_new_tournament():
    controller.get_rounds_new_tournament()


def get_players_new_tournament():
    controller.get_players_new_tournament()


def get_matches_new_tournament():
    controller.get_matches_new_tournament()


def get_actors_alphabetical_order():
    controller.get_actors_alphabetical_order()


def get_actors_ranking_order():
    controller.get_actors_ranking_order()


def get_tournaments():
    return controller.get_tournaments()


def get_info_tournament(_tournament):
    return controller.get_info_tournament(_tournament)


def get_players(_tournament):
    return controller.get_players(_tournament)


def get_rounds(_tournament):
    return controller.get_rounds(_tournament)


def get_matches(_tournament):
    return controller.get_matches(_tournament)


def get_last_ranking(_tournament):
    return controller.get_last_ranking(_tournament)


def main():
    menu_format = MenuFormatBuilder().set_border_style_type(MenuBorderStyleType.HEAVY_BORDER) \
        .set_prompt("SELECT>") \
        .set_title_align('center') \
        .set_subtitle_align('center') \
        .set_left_margin(4) \
        .set_right_margin(4) \
        .show_header_bottom_border(True)

    # Main menu
    menu = ConsoleMenu("Chess Application", subtitle="Main Menu", formatter=menu_format)

    # """************ BEGIN : Menu for a new tournament ************"""
    submenu = SelectionMenu([], title="New Tournament",
                            subtitle="Create and take place a new tournament",
                            formatter=menu_format, exit_option_text='Return to Main Menu')

    create_tournament_function = FunctionItem("Create Tournament", create_tournament)
    submenu.append_item(create_tournament_function)

    submenu_level2 = SelectionMenu([], title="Take Place Tournament ",
                                   formatter=menu_format, exit_option_text='Return to New Tournament')

    get_pairs_function = FunctionItem("Get Pairs", get_pairs)
    submenu_level2.append_item(get_pairs_function)

    start_round_function = FunctionItem("Start Round", make_new_round)
    submenu_level2.append_item(start_round_function)

    update_scores_function = FunctionItem("Update Matches", update_matches)
    submenu_level2.append_item(update_scores_function)

    end_round_function = FunctionItem("End Round", end_round)
    submenu_level2.append_item(end_round_function)

    get_ranking_function = FunctionItem("Last Ranking", get_last_ranking_new_tournament)
    submenu_level2.append_item(get_ranking_function)

    submenu_level2_item = SubmenuItem("Take Place Tournament", submenu=submenu_level2)
    submenu.append_item(submenu_level2_item)

    submenu_level2 = SelectionMenu([], title="New Tournament's Info",
                                   formatter=menu_format, exit_option_text='Return to New Tournament')

    get_info_new_tournament_function = FunctionItem("Main Info", get_info_new_tournament)
    submenu_level2.append_item(get_info_new_tournament_function)

    get_players_function = FunctionItem("Players", get_players_new_tournament)
    submenu_level2.append_item(get_players_function)

    get_rounds_function = FunctionItem("Rounds", get_rounds_new_tournament)
    submenu_level2.append_item(get_rounds_function)

    get_matches_function = FunctionItem("Matches", get_matches_new_tournament)
    submenu_level2.append_item(get_matches_function)

    get_ranking_function = FunctionItem("Last Ranking", get_last_ranking_new_tournament)
    submenu_level2.append_item(get_ranking_function)

    submenu_level2_item = SubmenuItem("Tournament's Info", submenu=submenu_level2)
    submenu.append_item(submenu_level2_item)

    # get_ranking_function = FunctionItem("Last Ranking", get_last_ranking)
    # submenu.append_item(get_ranking_function)

    submenu_item = SubmenuItem("New Tournament", submenu=submenu)
    menu.append_item(submenu_item)
    # """************ END : Menu for a new tournament ************"""

    # """************ BEGIN : Menu for the list of tournaments ************"""
    submenu = SelectionMenu([], title="Tournaments",
                            subtitle="Here are tournaments in the past",
                            formatter=menu_format, exit_option_text='Return to Main Menu')

    tournament_list = get_tournaments()

    for _tournament in tournament_list:
        submenu_level2 = SelectionMenu([], title="Tournament's Information", formatter=menu_format,
                                       subtitle="Here is a tournament in the past",
                                       exit_option_text='Return to Tournaments')

        get_info_tournament_function = FunctionItem("Main Info", get_info_tournament, [_tournament])
        submenu_level2.append_item(get_info_tournament_function)

        get_players_function = FunctionItem("Players", get_players, [_tournament])
        submenu_level2.append_item(get_players_function)

        get_rounds_function = FunctionItem("Rounds", get_rounds, [_tournament])
        submenu_level2.append_item(get_rounds_function)

        get_matches_function = FunctionItem("Matches", get_matches, [_tournament])
        submenu_level2.append_item(get_matches_function)

        get_last_ranking_function = FunctionItem("Last ranking", get_last_ranking, [_tournament])
        submenu_level2.append_item(get_last_ranking_function)

        submenu_level2_item = SubmenuItem(repr(_tournament), submenu=submenu_level2)
        submenu.append_item(submenu_level2_item)

    submenu_item = SubmenuItem("Tournaments", submenu=submenu)
    menu.append_item(submenu_item)
    # """************ END : Menu for the list of tournaments ************"""

    # """************ BEGIN : Menu for the list of actors ************"""
    submenu = SelectionMenu([], title="Actors",
                            formatter=menu_format, exit_option_text='Return to Main Menu')

    get_actors_by_letter_function = FunctionItem("Actors in alphabetical order", get_actors_alphabetical_order)
    submenu.append_item(get_actors_by_letter_function)

    get_actors_by_ranking_function = FunctionItem("Actors in elo ranking order", get_actors_ranking_order)
    submenu.append_item(get_actors_by_ranking_function)

    submenu_item = SubmenuItem("Actors", submenu=submenu)
    menu.append_item(submenu_item)
    # """************ END : Menu for the list of tournaments ************"""

    menu.show()


if __name__ == '__main__':
    main()
