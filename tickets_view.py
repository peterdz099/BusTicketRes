from kivy.uix.screenmanager import Screen


class TicketsWindow(Screen):

    def go_to_ticket(self):
        self.ids.tickets_sm.current = "ticket_details"
        self.ids.tickets_sm.transition.direction = "left"

    def back_to_ticket(self):
        self.ids.tickets_sm.current = "ticket"
        self.ids.tickets_sm.transition.direction = "right"
