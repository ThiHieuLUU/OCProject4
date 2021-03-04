from consolemenu import *
from consolemenu.format import *
from consolemenu.items import *
from controller import Controller as Controller
import tournament

controller = Controller()

# nbr_t = 4
# tournament_list = []
# for i in range(nbr_t):
#     t = tournament.Tournament()
#     t.name = "Tournement " + str(i)
#     tournament_list.append(t)


# round_index = 0

def create_tournament():
    # print("Hello World")
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


def see_players():
    print("Players")


def see_tournaments():
    print("Tournaments")


def see_actors():
    print("Actors")


def get_last_ranking():
    # print("Ranking")
    controller.get_last_ranking()

def get_info_new_tournament():
    controller.get_info_tournament()

def get_rounds_new_tournament():
    controller.get_rounds()

def get_players_new_tournament():
    controller.get_players()

def get_matches_new_tournament():
    controller.get_matches()


def get_actors_alphabetical_order():
    controller.get_actors_alphabetical_order()

def get_actors_ranking_order():
    controller.get_actors_ranking_order()


def get_tournaments():
    return controller.get_tounaments()

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
    submenu = SelectionMenu([], title="New Tournament",
                            subtitle="Create and take place a new tournament",
                            formatter=menu_format, exit_option_text='Return to Main Menu')

    create_tournament_function = FunctionItem("Create Tournament", create_tournament)
    submenu.append_item(create_tournament_function)

    submenu_level2 = SelectionMenu([], title="Take Place Tournament ",
                                   # subtitle="Taking place a new tournament",
                                   formatter=menu_format, exit_option_text='Return to New Tournament')

    get_pairs_function = FunctionItem("Get Pairs", get_pairs)
    submenu_level2.append_item(get_pairs_function)

    start_round_function = FunctionItem("Start Round", make_new_round)
    submenu_level2.append_item(start_round_function)

    update_scores_function = FunctionItem("Update Matches", update_matches)
    submenu_level2.append_item(update_scores_function)

    end_round_function = FunctionItem("End Round", end_round)
    submenu_level2.append_item(end_round_function)

    # get_ranking_function = FunctionItem("Last Ranking", get_last_ranking)
    # submenu_level2.append_item(get_ranking_function)

    submenu_level2_item = SubmenuItem("Take Place Tournament", submenu=submenu_level2)
    submenu.append_item(submenu_level2_item)

    submenu_level2 = SelectionMenu([], title="Tournament's Info",
                                   # subtitle="Taking place a new tournament",
                                   formatter=menu_format, exit_option_text='Return to New Tournament')

    get_info_function = FunctionItem("Main Info", get_info_new_tournament)
    submenu_level2.append_item(get_info_function)

    get_players_function = FunctionItem("Players", get_players_new_tournament)
    submenu_level2.append_item(get_players_function)

    get_rounds_function = FunctionItem("Rounds", get_rounds_new_tournament)
    submenu_level2.append_item(get_rounds_function)

    get_matches_function = FunctionItem("Matches", get_matches_new_tournament)
    submenu_level2.append_item(get_matches_function)

    get_ranking_function = FunctionItem("Last Ranking", get_last_ranking)
    submenu_level2.append_item(get_ranking_function)

    submenu_level2_item = SubmenuItem("Tournament's Info", submenu=submenu_level2)
    submenu.append_item(submenu_level2_item)


    # get_ranking_function = FunctionItem("Last Ranking", get_last_ranking)
    # submenu.append_item(get_ranking_function)

    submenu_item = SubmenuItem("New Tournament", submenu=submenu)
    menu.append_item(submenu_item)

    # Tournaments
    items = ["players", "rounds", "matches"]
    submenu_level2 = SelectionMenu(items, title="Tournament's Information", formatter=menu_format,
                                   exit_option_text='Return to Tournaments')

    # "rounds, matches, players",subtitle="See here tournament's information: "
    submenu = SelectionMenu([], title="Tournaments", subtitle="See here tournament's information",
                            formatter=menu_format, exit_option_text='Return to Main Menu')

    tournament_list = get_tournaments()
    print(tournament_list)
    for t in tournament_list:
        submenu_level2_item = SubmenuItem(t.name, submenu=submenu_level2)
        submenu.append_item(submenu_level2_item)

    submenu_item = SubmenuItem("Tournaments", submenu=submenu)
    menu.append_item(submenu_item)

    # Actors
    submenu = SelectionMenu([], title="Actors",
                            formatter=menu_format, exit_option_text='Return to Main Menu')

    get_actors_by_letter_function = FunctionItem("Actors in alphabetical order", get_actors_alphabetical_order)
    submenu.append_item(get_actors_by_letter_function)

    get_actors_by_ranking_function = FunctionItem("Actors in ranking order", get_actors_ranking_order)
    submenu.append_item(get_actors_by_ranking_function)

    submenu_item = SubmenuItem("Actors", submenu=submenu)
    menu.append_item(submenu_item)

    menu.show()


if __name__ == '__main__':
    main()
