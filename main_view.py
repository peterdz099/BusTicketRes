from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from account_view import AccountWindow
from search_view import SearchWindow
from tickets_view import TicketsWindow


class MainWindow(Screen):

    def switch_screen(self, instance_navigation_rail, instance_navigation_rail_item):
        self.ids.screen_manager.current = instance_navigation_rail_item.text

    def on_start(self):
        Builder.load_file('SearchWindow.kv')
        Builder.load_file('TicketsWindow.kv')
        Builder.load_file('AccountWindow.kv')
        self.ids.screen_manager.add_widget(SearchWindow(name="Search"))
        self.ids.screen_manager.add_widget(TicketsWindow(name="Tickets"))
        self.ids.screen_manager.add_widget(AccountWindow(name="Account"))
        self.ids.screen_manager.get_screen("Search").load_dropdown_items()
