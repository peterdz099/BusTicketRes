from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu


class SearchWindow(Screen):
    #date = datetime()
    menu_from = None
    menu_to = None
    counter = 1
    dialog = None

    def go_to_tickets(self):
        self.ids.search_sm.current = "search_tickets"
        self.ids.search_sm.transition.direction = "down"

    def back_to_main(self):
        self.ids.search_sm.current = "search_main"
        self.ids.search_sm.transition.direction = "up"

    def go_to_details(self):
        self.ids.list_sm.current = "ticket_details"
        self.ids.list_sm.transition.direction = "left"

    def back_to_ticket(self):
        self.counter = 1
        self.ids.counter_text.text = str(self.counter)
        self.ids.list_sm.current = "ticket"
        self.ids.list_sm.transition.direction = "right"

    def load_tickets(self):
        pass

    def load_ticket_details(self):
        pass

    def set_item_from(self, text_item):
        self.ids.drop_from.text = text_item
        self.menu_from.dismiss()

    def set_item_to(self, text_item):
        self.ids.drop_to.text = text_item
        self.menu_to.dismiss()

    def load_dropdown_items(self):
        cities = ['Bydgoszcz', 'Kraków', 'Rzeszów', 'Tarnów', 'Toruń', 'Warszawa', 'Wrocław']

        self.ids.drop_from.text = cities[0].upper()
        self.ids.drop_to.text = cities[1].upper()

        menu_items_from = [
            {
                "viewclass": "OneLineListItem",
                "text": f"{i.upper()}",
                "height": dp(56),
                "on_release": lambda x=f"{i.upper()}": self.set_item_from(x),
            } for i in cities
        ]
        self.menu_from = MDDropdownMenu(
            caller=self.ids.drop_from,
            items=menu_items_from,
            position="center",
            width_mult=4,
        )
        menu_items_to = [
            {
                "viewclass": "OneLineListItem",
                "text": f"{i.upper()}",
                "height": dp(56),
                "on_release": lambda x=f"{i.upper()}": self.set_item_to(x),
            } for i in cities
        ]

        self.menu_to = MDDropdownMenu(
            caller=self.ids.drop_to,
            items=menu_items_to,
            position="center",
            width_mult=4,
        )

    def book_tickets(self):
        self.dialog_close()
        self.back_to_ticket()
        print("Booked")

    def show_alert_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                text=f"Are you sure You want to book {self.counter} ticets?",
                buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        theme_text_color="Custom",
                        md_bg_color="#f59122",
                        text_color=(1, 1, 1, 1),
                        on_press=lambda x: self.dialog_close(),
                    ),
                    MDFlatButton(
                        text="Yes",
                        md_bg_color="#f59122",
                        theme_text_color="Custom",
                        text_color=(1,1,1,1),
                        on_press=lambda x: self.book_tickets(),
                    ),
                ],
            )
        self.dialog.open()

    def dialog_close(self):
        self.dialog.dismiss(force=True)

    def increase(self):
        self.counter += 1
        self.ids['counter_text'].text = str(self.counter)

    def decrease(self):
        if self.counter <= 1:
            pass
        else:
            self.counter -= 1
            self.ids['counter_text'].text = str(self.counter)



