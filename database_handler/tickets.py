from database_handler.init_db import Database
from mysql.connector import Error


class Tickets:

    def __init__(self, database: Database):
        self.connection = database.get_connection()

    # THO CHYBA MUSI BYC WYKONYWANE DLA KAZDEGO BILETU ALE TO RACZEJ W PETLI SIE JEBNIE
    def add_ticket(self, ticket_id, ride_id, user_id, seat_no):
        add_ticket_query = """
                        INSERT INTO ticket 
                        (ticket_id, ride_id, user_id, seat_no, cost) 
                        VALUES (%s, %s, %s, %s, %s)
                        """
        get_ticket_cost_query = """
                        SELECT price FROM rides WHERE
                        ride_id = %s 
                        """
        try:
            with self.connection.cursor() as cursor:
                cost = cursor.execute(get_ticket_cost_query, ride_id)
        except Error as e:
            print(e)

        ticket_values = (ticket_id, ride_id, user_id, seat_no, cost)
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(add_ticket_query, ticket_values)
                self.connection.commit()
        except Error as e:
            print(e)

    def remove_ticket(self, ticket_id, ride_id, user_id, seat_no):
        add_ticket_query = """
                        DELETE FROM ticket WHERE
                        ticket_id = %s 
                        AND ride_id = %s 
                        AND user_id = %s 
                        AND seat_no = %s 
                        """

        ticket_values = (ticket_id, ride_id, user_id, seat_no)
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(add_ticket_query, ticket_values)
                self.connection.commit()
        except Error as e:
            print(e)