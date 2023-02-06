import datetime
from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivy.metrics import dp
from kivymd.uix.list import TwoLineAvatarListItem, ImageLeftWidget
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.pickers import MDDatePicker

from database_handler.init_db import Database
from database_handler.tickets import Tickets
from global_variables import db, ticketsResources, sm


class SearchWindow(Screen):
    date = None
    menu_from = None
    menu_to = None
    counter = 0
    free_seats = 25
    dialog = None
    user_id = None
    ride_id = None

    def set_user_id(self, user_id):
        self.user_id = user_id

    def go_to_tickets(self):
        self.ids.book_error.text = ""
        self.ids.search_sm.current = "search_tickets"
        self.ids.search_sm.transition.direction = "down"

    def back_to_main(self):
        self.ids.book_error.text = ""
        self.ids.search_sm.current = "search_main"
        self.ids.search_sm.transition.direction = "up"
        self.clear_connections()
        self.ids.connection_details.text = ""
        self.ids.ticket_details_img.source = ""


    def go_to_details(self):
        self.ids.list_sm.current = "ticket_details"
        self.ids.list_sm.transition.direction = "left"

    def back_to_ticket(self):
        self.counter = 0
        self.ids.connection_details.text = ""
        self.ids.ticket_details_img.source = ""
        self.ids.counter_text.text = str(self.counter)
        self.ids.list_sm.current = "ticket"
        self.ids.list_sm.transition.direction = "right"

    def book_tickets(self):

        ticketsResources = Tickets(db)
        msg = ticketsResources.add_ticket(self.ride_id, self.user_id, self.counter)

        sm.get_screen("main").ids.screen_manager.get_screen("Tickets").clear_user_tickets()
        sm.get_screen("main").ids.screen_manager.get_screen("Tickets").load_user_tickets()
        self.dialog_close()
        self.back_to_ticket()
        self.back_to_main()
        if msg is not None:
            self.ids.book_error.text = msg


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

    def show_date_picker(self):

        min_date = datetime.date.today()
        max_date = datetime.date(2023, 2, 17)

        date_dialog = MDDatePicker(primary_color="#f59122",
                                   selector_color="#f59122",
                                   text_button_color="black")

        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()

    def clear_connections(self):
        self.ids.scroll_connections.clear_widgets()

    def load_connections(self):
        source = self.ids.drop_from.text
        destination = self.ids.drop_to.text
        db = Database()
        connections = db.list_connections(source, destination, str(self.date))
        image_src = db.get_city_img_link(destination)
        if connections:
            for connection in connections:
                self.ids.scroll_connections.add_widget(TwoLineAvatarListItem(
                    ImageLeftWidget(
                        source=f"{image_src}"),
                    text=f"{connection.get('src')} - {connection.get('destination')}",
                    secondary_text=f"{connection.get('departure')}",
                    id=f"{connections.index(connection)}",
                    on_release=(lambda x: self.load_connection_details(connections[int(x.id)], image_src))
                ))
            self.go_to_tickets()

        elif self.date is None:
            self.ids.book_error.text = "Select Date"

        elif len(connections) == 0:
            self.ids.book_error.text = "No connections on this day"

    def load_connection_details(self, connection, image_src):
        self.ride_id = connection.get('ride_id')
        self.go_to_details()
        self.ids.ticket_details_img.source = image_src
        self.ids.connection_details.text = f"Beginning:{connection.get('src')}\n\n" \
                                           f"Destination: {connection.get('destination')}\n\n" \
                                           f"Price(1 Ticket): {connection.get('price')}\n\n" \
                                           f"Departure date: {connection.get('departure')}\n\n" \
                                           f"Arrival Date: {connection.get('arrival')}\n\n" \
                                           f"Number of free Seats: {connection.get('free_seats')}"
        self.free_seats = connection.get('free_seats')

    def set_item_from(self, text_item):
        self.ids.drop_from.text = text_item
        self.menu_from.dismiss()

    def set_item_to(self, text_item):
        self.ids.drop_to.text = text_item
        self.menu_to.dismiss()

    def load_dropdown_items(self):
        cities = db.list_cities()
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

    def show_alert_dialog(self,):
        if self.counter > 0:

            self.dialog = MDDialog(
                text=f"Are you sure You want to book {self.ids['counter_text'].text} tickets?",
                buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        theme_text_color="Custom",
                        md_bg_color="#f59122",
                        text_color=(1, 1, 1, 1),
                        on_press=lambda x: self.dialog_close(),
                    ),
                    MDFlatButton(
                        text="YES",
                        md_bg_color="#f59122",
                        theme_text_color="Custom",
                        text_color=(1, 1, 1, 1),
                        on_press=lambda x: self.book_tickets(),
                    ),
                ],
            )
        self.dialog.open()

    def dialog_close(self):
        self.dialog.dismiss(force=True)

    def increase(self):
        if self.counter <= self.free_seats:
            self.counter += 1
            self.ids['counter_text'].text = str(self.counter)

    def decrease(self):
        if self.counter <= 1:
            pass
        else:
            self.counter -= 1
            self.ids['counter_text'].text = str(self.counter)
