from database_handler.init_db import Database
from mysql.connector import Error


class Tickets:

    def __init__(self, database: Database):
        self.connection = database.get_connection()

    # THO CHYBA MUSI BYC WYKONYWANE DLA KAZDEGO BILETU ALE TO RACZEJ W PETLI SIE JEBNIE
    def add_ticket(self, ride_id, user_id, seats):
        add_ticket_query = """
                        INSERT IGNORE INTO ticket 
                        (ticket_id, ride_id, user_id, seat_no, cost) 
                        VALUES (%s, %s, %s, %s, %s)
                        """

        get_ticket_cost_query = """
                        SELECT price FROM rides WHERE
                        ride_id = %s 
                        """
        get_max_seats_query = """
                       SELECT seats FROM rides WHERE
                       ride_id = %s
                       """
        get_taken_seats_query = """
                        SELECT seat_no FROM ticket WHERE
                        ride_id = %s
        """
        get_departure_time_query = """
                        SELECT NOW() < departure FROM rides WHERE
                        ride_id = %s"""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(get_departure_time_query, (ride_id,))
                temp = cursor.fetchall()
                if temp[0][0] != 1:
                    print('Autobus juz odjechał')
                    self.connection.rollback()
                    return

        except Error as e:
            print("Sprawdz czy autobus juz nie odjachal")
            return

        cost = 0
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
            return

        seat_numbers = []
        max_seats = 0
        temp = None
        with self.connection.cursor() as cursor:
            cursor.execute(get_max_seats_query, (ride_id,))
            max_seats = cursor.fetchall()
            cursor.execute(get_taken_seats_query, (ride_id,))
            temp = cursor.fetchall()


        for seat in range(max_seats[0][0] + 1):
            seat_numbers.append(seat)

        avaliable_seats = []
        if temp == []:
            avaliable_seats = seat_numbers
        else:
            temp2 = []
            for field in temp:
                temp2.append(field[0])

            for seat in seat_numbers:
                if seat not in temp2:
                    avaliable_seats.append(seat)

        try:
            with self.connection.cursor() as cursor:
                for i in range(seats):
                    ticket_id = str(ride_id) + '-' + str(avaliable_seats[i])
                    ticket_values = (ticket_id, ride_id, user_id, avaliable_seats[i], cost)
                    cursor.execute(add_ticket_query, ticket_values)
                self.connection.commit()
        except:
            self.connection.rollback()
            s = "error with ticket selection"
            print("error with ticket selection")
            return s

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
        except:
            self.connection.rollback()

    def list_user_tickets(self, user_id):
        list_user_tickets_query = """
                                    SELECT * FROM ticket WHERE
                                    user_id = %s"""
        temp = None
        with self.connection.cursor() as cursor:
            cursor.execute(list_user_tickets_query, (user_id,))
            temp = cursor.fetchall()
        ticket_listing = []
        for listing in temp:
            ticket_id = listing[0]
            ride_id = listing[1]
            seat_no = listing[3]
            price = listing[4]

            item = {"ticket_id": ticket_id, "ride_id": ride_id, "seat_no": seat_no,
                    "price": price}

            ticket_listing.append(item)

        return ticket_listing

if __name__ == "__main__":
    db = Database()
    db.create_all()
    tickets = Tickets(db)
    #(tickets.add_ticket('1-WaKrk-202302101003',1,22))