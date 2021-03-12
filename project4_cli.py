#! /usr/bin/venv python3
# coding: utf-8

"""This module is used as a CLI (command line interface) for user in order to:
- create and take place a new tournament
- See information of previous tournaments (players, rounds, matches, ranking)
- See information of all players (actors) coming from previous tournaments.
"""

from consolemenu import ConsoleMenu, SelectionMenu, MenuFormatBuilder
from consolemenu.items import FunctionItem, SubmenuItem
from consolemenu.format import MenuBorderStyleType

from controller import Controller as Controller


def append_new_tournament_menu(menu, menu_format, controller):
    """Build a submenu in order to help the user entries/updates information for a new tournament.
    This submenu is added to the main menu.
    """

    submenu = SelectionMenu([], title="New Tournament",
                            subtitle="Create and take place a new tournament",
                            formatter=menu_format, exit_option_text='Return to Main Menu')

    create_tournament_function = FunctionItem("Create Tournament", controller.create_tournament)
    submenu.append_item(create_tournament_function)

    submenu_level2 = SelectionMenu([], title="Take Place Tournament ",
                                   formatter=menu_format, exit_option_text='Return to New Tournament')

    # Pairs for next round
    show_pairs_function = FunctionItem("Get Pairs", controller.show_pairs)
    submenu_level2.append_item(show_pairs_function)

    start_round_function = FunctionItem("Start Round", controller.make_new_round)
    submenu_level2.append_item(start_round_function)

    update_scores_function = FunctionItem("Update Matches", controller.update_matches)
    submenu_level2.append_item(update_scores_function)

    end_round_function = FunctionItem("End Round", controller.end_round)
    submenu_level2.append_item(end_round_function)

    show_ranking_function = FunctionItem("Last Ranking", controller.show_last_ranking_new_tournament)
    submenu_level2.append_item(show_ranking_function)

    submenu_level2_item = SubmenuItem("Take Place Tournament", submenu=submenu_level2)
    submenu.append_item(submenu_level2_item)

    submenu_level2 = SelectionMenu([], title="New Tournament's Info",
                                   formatter=menu_format, exit_option_text='Return to New Tournament')

    show_info_new_tournament_function = FunctionItem("Main Info", controller.show_info_new_tournament)
    submenu_level2.append_item(show_info_new_tournament_function)

    show_players_function = FunctionItem("Players", controller.show_players_new_tournament)
    submenu_level2.append_item(show_players_function)

    show_rounds_function = FunctionItem("Rounds", controller.show_rounds_new_tournament)
    submenu_level2.append_item(show_rounds_function)

    show_matches_function = FunctionItem("Matches", controller.show_matches_new_tournament)
    submenu_level2.append_item(show_matches_function)

    show_ranking_function = FunctionItem("Last Ranking", controller.show_last_ranking_new_tournament)
    submenu_level2.append_item(show_ranking_function)

    submenu_level2_item = SubmenuItem("Tournament's Info", submenu=submenu_level2)
    submenu.append_item(submenu_level2_item)

    submenu_item = SubmenuItem("New Tournament", submenu=submenu)
    menu.append_item(submenu_item)


def append_tournaments_menu(menu, menu_format, controller):
    """Build a submenu in order to display the list of tournaments. This submenu is added to the main menu."""

    submenu = SelectionMenu([], title="Tournaments",
                            subtitle="Here are tournaments in the past",
                            formatter=menu_format, exit_option_text='Return to Main Menu')

    tournament_list = controller.get_tournaments()

    for _tournament in tournament_list:
        submenu_level2 = SelectionMenu([], title="Tournament's Information", formatter=menu_format,
                                       subtitle="Here is a tournament in the past",
                                       exit_option_text='Return to Tournaments')

        show_info_tournament_function = FunctionItem("Main Info", controller.show_info_tournament, [_tournament])
        submenu_level2.append_item(show_info_tournament_function)

        show_players_function = FunctionItem("Players", controller.show_players, [_tournament])
        submenu_level2.append_item(show_players_function)

        show_rounds_function = FunctionItem("Rounds", controller.show_rounds, [_tournament])
        submenu_level2.append_item(show_rounds_function)

        show_matches_function = FunctionItem("Matches", controller.show_matches, [_tournament])
        submenu_level2.append_item(show_matches_function)

        show_last_ranking_function = FunctionItem("Last ranking", controller.show_last_ranking, [_tournament])
        submenu_level2.append_item(show_last_ranking_function)

        submenu_level2_item = SubmenuItem(repr(_tournament), submenu=submenu_level2)
        submenu.append_item(submenu_level2_item)

    submenu_item = SubmenuItem("Tournaments", submenu=submenu)
    menu.append_item(submenu_item)


def append_actors_menu(menu, menu_format, controller):
    """Build a submenu in order to display actors. This submenu is added to the main menu."""

    submenu = SelectionMenu([], title="Actors",
                            formatter=menu_format, exit_option_text='Return to Main Menu')

    show_actors_by_letter_function = FunctionItem("Actors in alphabetical order",
                                                  controller.show_actors_alphabetical_order)
    submenu.append_item(show_actors_by_letter_function)

    show_actors_by_ranking_function = FunctionItem("Actors in elo ranking order", controller.show_actors_ranking_order)
    submenu.append_item(show_actors_by_ranking_function)

    submenu_item = SubmenuItem("Actors", submenu=submenu)
    menu.append_item(submenu_item)


def main():
    controller = Controller()

    menu_format = MenuFormatBuilder().set_border_style_type(MenuBorderStyleType.HEAVY_BORDER) \
        .set_prompt("SELECT>") \
        .set_title_align('center') \
        .set_subtitle_align('center') \
        .set_left_margin(4) \
        .set_right_margin(4) \
        .show_header_bottom_border(True)

    # Main menu
    menu = ConsoleMenu("Chess Application", subtitle="Main Menu", formatter=menu_format)
    append_new_tournament_menu(menu, menu_format, controller)
    append_tournaments_menu(menu, menu_format, controller)
    append_actors_menu(menu, menu_format, controller)

    menu.show()


if __name__ == '__main__':
    main()
