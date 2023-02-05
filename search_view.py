from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.list import TwoLineAvatarListItem, ImageLeftWidget
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.pickers import MDDatePicker

from global_variables import db


class SearchWindow(Screen):
    date = None
    menu_from = None
    menu_to = None
    counter = 1
    dialog = None
    connections = []

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

    def book_tickets(self):
        self.dialog_close()
        self.back_to_ticket()
        print("Booked")

    def on_cancel(self, instance, value):
        '''Events called when the "CANCEL" dialog box button is clicked.'''

    def on_save(self, instance, value, date_range):
        '''
        Events called when the "OK" dialog box button is clicked.

        :type instance: <kivymd.uix.picker.MDDatePicker object>;
        :param value: selected date;
        :type value: <class 'datetime.date'>;
        :param date_range: list of 'datetime.date' objects in the selected range;
        :type date_range: <class 'list'>;
        '''

        self.date = value
        print(self.date)

    def show_date_picker(self):
        date_dialog = MDDatePicker(primary_color="#f59122", selector_color="#f59122",text_button_color="black")
        date_dialog.bind( on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()

    def load_connections(self):
        source = self.ids.drop_from.text
        destination = self.ids.drop_to.text
        self.connections = db.list_connections(source, destination, str(self.date))
        image_src = "https://imgs.search.brave.com/HMdj6Gmuu4WVD2xkPDeiTEly-cM83jR8-6q-yeNO1Ak/rs:fit:1200:1200:1/g:ce/aHR0cHM6Ly9kbWNw/b2xhbmQuY29tL3dw/LWNvbnRlbnQvdXBs/b2Fkcy8yMDE3LzAy/L2tyYWtvdzMuanBn"
        if self.connections:
            for connection in self.connections:
                self.ids.scroll.add_widget(TwoLineAvatarListItem(
                    ImageLeftWidget(
                        source=f"{image_src}"),
                    text=f"{connection.get('src')} - {connection.get('destination')}",
                    secondary_text=f"{connection.get('departure')}",
                    on_release=(lambda x: self.go_to_details())
                ))
            self.go_to_tickets()

        elif len(self.connections) == 0:
            self.ids.book_error.text = "No connections on this day"

    def load_ticket_details(self):
        pass

    def set_item_from(self, text_item):
        self.ids.drop_from.text = text_item
        self.menu_from.dismiss()

    def set_item_to(self, text_item):
        self.ids.drop_to.text = text_item
        self.menu_to.dismiss()

    def load_dropdown_items(self):

        cities = db.list_cities()
        print(cities)
        self.ids.drop_from.text = cities[0]
        self.ids.drop_to.text = cities[1]

        menu_items_from = [
            {
                "viewclass": "OneLineListItem",
                "text": f"{i}",
                "height": dp(56),
                "on_release": lambda x=f"{i}": self.set_item_from(x),
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
                "text": f"{i}",
                "height": dp(56),
                "on_release": lambda x=f"{i}": self.set_item_to(x),
            } for i in cities
        ]

        self.menu_to = MDDropdownMenu(
            caller=self.ids.drop_to,
            items=menu_items_to,
            position="center",
            width_mult=4,
        )

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



