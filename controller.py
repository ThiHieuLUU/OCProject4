from model import Person
import view

class Controller(object):

    def __init__(self, model, view):
        self.model = model
        self.view = view

    def show_items(self, bullet_points=False):
        items = self.model.read_items()
        item_type = self.model.item_type
        if bullet_points:
            self.view.show_bullet_point_list(item_type, items)
        else:
            self.view.show_number_point_list(item_type, items)




#
# def showAll():
#     #gets list of all Person objects
#     people_in_db = Person.getAll()
#     #calls view
#     return view.showAllView(people_in_db)
#
# def start():
#     view.startView()
#     input_ = input()
#     if input_ == 'y':
#         return showAll()
#     else:
#         return view.endView()
#
# if __name__ == "__main__":
#     #running controller function
#     start()