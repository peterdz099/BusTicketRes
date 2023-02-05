from kivy.uix.screenmanager import Screen
from kivymd.uix.list import OneLineAvatarListItem, ImageLeftWidget, TwoLineAvatarListItem, OneLineListItem

from global_variables import ticketsResources, db


class TicketsWindow(Screen):

    ticket_id = None
    ride_id = None
    user_id = None
    seat_no = None

    def set_user_id(self, user_id):
        self.user_id = user_id

    def load_user_tickets(self):

        #ids.scroll_user_tickets
        #ids.ticket_details_img
        # ids.ticket_details

        user_tickets = ticketsResources.list_user_tickets(self.user_id)
        #user_tickets[0].get('ride_id')
        if user_tickets:
            a = 1
            for ticket in user_tickets:
                connection = db.get_ride_from_ride_id(ticket.get('ride_id'))[0]
                image_src = db.get_city_img_link(connection.get('destination'))
                self.ids.scroll_user_tickets.add_widget(TwoLineAvatarListItem(
                    ImageLeftWidget(
                        source=f"{image_src}"),
                    text=f"{connection.get('src')} - {connection.get('destination')}",
                    secondary_text=f"Seat: {ticket.get('seat_no')}   Ticket ID: {ticket.get('ticket_id')}",
                    id=f"{user_tickets.index(ticket)}",
                    on_release=(lambda x: self.load_ticket_details(connection,image_src,
                                                                   user_tickets[int(x.id)].get('seat_no'),
                                                                   user_tickets[int(x.id)].get('ticket_id'),
                                                                   user_tickets[int(x.id)].get('ride_id')
                                                                   ))
                ))

        elif user_tickets is None:
            self.ids.scroll_connections.add_widget(OneLineListItem(
                text=f"You don't have any tickets"))
        elif len(user_tickets) == 0:
            self.ids.scroll_user_tickets.add_widget(OneLineListItem(text=f"You don't have any tickets"))


    def load_ticket_details(self, connection, image_src, seat_no, ticket_id, ride_id):
        self.ids.ticket_details_img.source = image_src
        self.ids.ticket_details.text = f"Beginning: {connection.get('src')}\n\n" \
                                       f"Destination: {connection.get('destination')}\n\n" \
                                       f"Ticket ID: {ticket_id}\n\n" \
                                       f"Departure date: {connection.get('departure')}\n\n" \
                                       f"Arrival Date: {connection.get('arrival')}\n\n" \
                                       f"Seat: {seat_no}"

        self.ticket_id = ticket_id
        self.ride_id = ride_id
        self.seat_no = seat_no
        self.go_to_ticket()

    def remove_ticket(self):
        print(self.ticket_id, self.ride_id, self.seat_no, f"USER: {self.user_id}")
        ticketsResources.remove_ticket(self.ticket_id, self.ride_id, self.user_id, self.seat_no)
        self.clear_user_tickets()
        self.load_user_tickets()
        self.back_to_tickets()

    def clear_user_tickets(self):
        self.ids.scroll_user_tickets.clear_widgets()

    def go_to_ticket(self):
        self.ids.tickets_sm.current = "ticket_details"
        self.ids.tickets_sm.transition.direction = "left"

    def back_to_tickets(self):
        self.ids.tickets_sm.current = "ticket"
        self.ids.tickets_sm.transition.direction = "right"
