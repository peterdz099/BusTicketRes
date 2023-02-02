from database_handler.init_db import Database
from global_variables import db
from mysql.connector import Error


class Tickets:

    def __init__(self, database: Database):
        self.connection = database.get_connection()

    # THO CHYBA MUSI BYC WYKONYWANE DLA KAZDEGO BILETU ALE TO RACZEJ W PETLI SIE JEBNIE
    def add_ticket(self, ride_id, user_id, seat_no):
        add_ticket_query = """
                        INSERT IGNORE INTO ticket 
                        (ticket_id, ride_id, user_id, seat_no, cost) 
                        VALUES (%s, %s, %s, %s, %s)
                        """

        get_ticket_cost_query = """
                        SELECT price FROM rides WHERE
                        ride_id = %s 
                        """

        cost = 0
        ticket_id = str(ride_id) + '-' + str(seat_no)
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(get_ticket_cost_query, (ride_id,))
                temp = cursor.fetchall()
                if temp != []:
                    cost = temp[0][0]
                else:
                    print("Nie ma takiej linii")
                    return

        except Error as e:
            print("Błąd przy znajdowaniu kosztu biletu")

        ticket_values = (ticket_id, ride_id, user_id, seat_no, cost)
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(add_ticket_query, ticket_values)
                self.connection.commit()
        except Error as e:
            print(e)

    def remove_ticket(self, ticket_id, ride_id, user_id, seat_no):
        remove_ticket_query = """
                        DELETE FROM ticket WHERE
                        ticket_id = %s 
                        AND ride_id = %s 
                        AND user_id = %s 
                        AND seat_no = %s 
                        """

        ticket_values = (ticket_id, ride_id, user_id, seat_no)
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(remove_ticket_query, ticket_values)
                self.connection.commit()
        except Error as e:
            print(e)

"""if __name__ == "__main__":
    db = Database()
    db.create_all()
    tickets = Tickets(db)
    tickets.add_ticket(4,1,0)"""