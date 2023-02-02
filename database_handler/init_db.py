import os
from mysql.connector import connect


# This class provides database connection management and creating tables
# Operating with specific table requires passing Database object in constructor to initialize connection
class Database:
    def __init__(self):
        self._connection = None
        self.initialize_connection()

    def initialize_connection(self):
        db_user = os.environ.get('DB_USER')
        db_password = os.environ.get('DB_PASS')
        db_host = 'mysql.agh.edu.pl'
        self._connection = connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database='pdziula'
        )

    def get_connection(self):
        return self._connection

    def close_connection(self):
        self._connection.close()

    def list_cities(self):
        list_city_query = """
        SELECT * FROM cities
        """
        city_list = []
        temp = []
        with self._connection.cursor() as cursor:
            cursor.execute(list_city_query)
            temp.append(cursor.fetchall())

        for city in temp:
            for field in city:
                city_list.append(field[0])
        return city_list

    def list_connections(self, source, destination):
        list_connections_query = """
        SELECT * FROM rides WHERE 
        src = %s
        AND destination = %s
        """

        connections_list = {}

        connection_values = (source, destination)
        temp = None
        with self._connection.cursor() as cursor:
            cursor.execute(list_connections_query, connection_values)
            temp = cursor.fetchall()


        counter = 0

        for listing in temp:
            suggestions = []
            ride_id = listing[0]
            arrival = listing[1]
            departure = listing[2]
            destination = listing[3]
            src = listing[4]
            seats = listing[5]
            price = listing[6]
            item = {"ride_id": ride_id, "arrival": arrival, "departure": departure, "destination": destination,
                    "src": src, "seats": seats, "price": price}
            suggestions.append(item)
            connections_list.update({f'{counter}': suggestions})
            counter += 1
        return connections_list

    def create_users_table(self):
        create_users_table_query = """
           CREATE TABLE IF NOT EXISTS users (
               user_id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
               username VARCHAR(255) NOT NULL UNIQUE,
               email VARCHAR(255) NOT NULL UNIQUE,
               password VARCHAR(255) NOT NULL,
               is_verified BOOLEAN NOT NULL DEFAULT 0
           )
           """

        with self._connection.cursor() as cursor:
            cursor.execute(create_users_table_query)
            self._connection.commit()

    def create_cities_table(self):
        create_cities_table_query = """
        CREATE TABLE IF NOT EXISTS cities (
            city varchar(255) NOT NULL UNIQUE)"""

        insert_into_cities_query = """
        INSERT IGNORE INTO cities (city) VALUES
            ('Toruń'),
            ('Kraków'),
            ('Warszawa'),
            ('Bydgoszcz'),
            ('Rzeszów')
        """

        with self._connection.cursor() as cursor:
            cursor.execute(create_cities_table_query)
            cursor.execute(insert_into_cities_query)
            self._connection.commit()

    def create_ticket_table(self):
        create_ticket_table_query = """
        CREATE TABLE IF NOT EXISTS ticket (
            ticket_id VARCHAR(20) NOT NULL PRIMARY KEY,
            ride_id VARCHAR(20) NOT NULL,
            user_id int(11) NOT NULL,
            seat_no int(11) NOT NULL,
            cost int(11) NOT NULL,
            FOREIGN KEY (ride_id)
                REFERENCES rides(ride_id),
            FOREIGN KEY (user_id)
                REFERENCES users(user_id)
        ) """

        delete_check_seat_trigger_query = """
        DROP TRIGGER IF EXISTS check_seat_no;
        """
        check_seat_no_trigger = """
        CREATE TRIGGER check_seat_no BEFORE INSERT ON ticket
        FOR EACH ROW
            IF NEW.seat_no > (SELECT seats FROM rides r WHERE r.ride_id = NEW.ride_id)
        THEN 
            SIGNAL SQLSTATE '50002' SET MESSAGE_TEXT = 'Niepoprawny numer miejsca';
        END IF;
        """

        delete_check_unique_seat_to_ride_trigger_query = """
        DROP TRIGGER IF EXISTS check_unique_seat_to_ride;
        """

        check_unique_seat_to_ride_trigger_query = """
        CREATE TRIGGER check_unique_seat_to_ride BEFORE INSERT ON ticket
        FOR EACH ROW
            IF NEW.seat_no in (SELECT seat_no FROM ticket t WHERE NEW.ride_id = t.ride_id)
        THEN 
            SIGNAL SQLSTATE '50002' SET MESSAGE_TEXT = 'Miejsce zajęte';
        END IF;
        """

        with self._connection.cursor() as cursor:
            cursor.execute(create_ticket_table_query)
            cursor.execute(delete_check_seat_trigger_query)
            cursor.execute(delete_check_unique_seat_to_ride_trigger_query)
            cursor.execute(check_seat_no_trigger)
            cursor.execute(check_unique_seat_to_ride_trigger_query)
            self._connection.commit()

    def create_rides_table(self):
        create_ride_table_query = """
        CREATE TABLE IF NOT EXISTS rides (
            ride_id VARCHAR(20) NOT NULL PRIMARY KEY,
            arrival datetime NOT NULL,
            departure datetime NOT NULL,
            destination varchar(20) NOT NULL,
            src varchar(20) NOT NULL,
            seats int(11) NOT NULL,
            price int(11) NOT NULL,
            FOREIGN KEY (destination)
                REFERENCES cities(city),
            FOREIGN KEY (src)
                REFERENCES cities(city)
        )"""


        insert_into_rides = """
        INSERT IGNORE INTO rides (ride_id, arrival, departure, destination, src, seats, price) VALUES
            (1, '2022-02-10 10:03:00', '2022-02-10 09:01:00', 'Warszawa', 'Kraków', 23,  175),
            (5, '2022-02-10 10:11:00', '2022-02-10 09:21:00', 'Warszawa', 'Kraków', 24,  176),
            (2, '2022-02-05 11:15:00', '2022-02-05 10:05:00', 'Tarnów', 'Wrocław', 21,  185),
            (3, '2022-02-05 12:13:00', '2022-02-05 10:13:00', 'Rzeszów', 'Toruń', 23,  205),
            (4, '2022-02-05 12:13:00', '2022-02-05 10:13:00', 'Będzin', 'Toruń', 23,  205)"""

        with self._connection.cursor() as cursor:
            cursor.execute(create_ride_table_query)
            cursor.execute(insert_into_rides)
            self._connection.commit()

    def create_all(self):
        self.create_cities_table()
        self.create_rides_table()
        self.create_users_table()
        self.create_ticket_table()


"""if __name__ == "__main__":
    xd = Database()
    xd.create_all()
    print(xd.list_connections('dupa', 'Warszawa'))"""

