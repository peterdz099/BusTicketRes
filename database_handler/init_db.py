import datetime
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

    def update_db(self):
        select_finished_courses_query = """
                                        SELECT * FROM rides WHERE
                                        arrival > NOW()
                                        AND date(arrival) = date(NOW())
                                        """

        insert_into_rides_query = """
                                INSERT IGNORE INTO rides 
                                (ride_id, arrival, departure, destination, src, seats, price) VALUES
                                (%s, %s, %s, %s, %s, %s, %s)"""

        with self._connection.cursor() as cursor:
            cursor.execute(select_finished_courses_query)
            temp = cursor.fetchall()
            try:
                for listing in temp:

                    arrival = listing[1] + datetime.timedelta(weeks=1)
                    departure = listing[2] + datetime.timedelta(weeks=1)

                    ride_id = listing[0]
                    sub_str = "-"
                    occurrence = 2

                    # Finding nth occurrence of substring
                    val = -1
                    for i in range(0, occurrence):
                        val = ride_id.find(sub_str, val + 1)
                    id = ride_id[:val+1]
                    temp = str(arrival)
                    temp = temp[:-2]
                    temp = temp.replace("-", '')
                    temp = temp.replace(' ', '')
                    temp = temp.replace(':', '')
                    ride_id = id + temp
                    destination = listing[3]
                    src = listing[4]
                    seats = listing[5]
                    price = listing[6]
                    values = (ride_id, arrival, departure, destination, src, seats, price)
                    cursor.execute(insert_into_rides_query, values)
                self._connection.commit()
            except:
                self._connection.close()






    def get_connection(self):
        return self._connection

    def close_connection(self):
        self._connection.close()

    def get_city_img_link(self, city):
        get_city_link_query = """
                               SELECT img_link FROM cities WHERE
                               city=%s"""
        with self._connection.cursor() as cursor:
            cursor.execute(get_city_link_query, (city,))
            temp = cursor.fetchall()
            return temp[0][0]


    def get_free_seats(self, ride_id):
        get_max_seats_query = """
                               SELECT seats FROM rides WHERE
                               ride_id = %s
               """
        get_taken_seats_query = """
                                SELECT count(*) FROM ticket WHERE
                                ride_id = %s"""
        max_seats = 0
        taken_seats = 0
        with self._connection.cursor() as cursor:
            cursor.execute(get_taken_seats_query, (ride_id,))
            taken_seats = cursor.fetchall()
            cursor.execute(get_max_seats_query, (ride_id,))
            max_seats = cursor.fetchall()

        return max_seats[0][0]-taken_seats[0][0] + 1

    def get_ride_from_ride_id(self, ride_id):
        get_ride_from_ride_id_query = """
                                       SELECT * FROM rides WHERE
                                       ride_id = %s
                       """
        city_data = []
        with self._connection.cursor() as cursor:
            cursor.execute(get_ride_from_ride_id_query, (ride_id,))
            temp = cursor.fetchall()
            for listing in temp:
                ride_id = listing[0]
                arrival = listing[1]
                departure = listing[2]
                destination = listing[3]
                src = listing[4]
                #free_seats = self.get_free_seats(listing[0])
                price = listing[6]

                item = {"ride_id": ride_id, "arrival": arrival, "departure": departure, "destination": destination,
                        "src": src,  "price": price}

                city_data.append(item)
        return city_data

    def list_cities(self):
        list_city_query = """
        SELECT city FROM cities
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

    def list_connections(self, source, destination, date):
        list_connections_query = """
        SELECT * FROM rides WHERE 
        src = %s
        AND destination = %s
        AND date(departure) = %s
        AND departure > NOW()
        """

        connections_list = []

        connection_values = (source, destination, date)
        temp = None
        with self._connection.cursor() as cursor:
            cursor.execute(list_connections_query, connection_values)
            temp = cursor.fetchall()

        for listing in temp:
            ride_id = listing[0]
            arrival = listing[1]
            departure = listing[2]
            destination = listing[3]
            src = listing[4]
            free_seats = self.get_free_seats(listing[0])
            price = listing[6]

            item = {"ride_id": ride_id, "arrival": arrival, "departure": departure, "destination": destination,
                    "src": src, "free_seats": free_seats, "price": price}

            connections_list.append(item)

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
            city varchar(255) NOT NULL UNIQUE,
            img_link VARCHAR(255))"""

        insert_into_cities_query = """
        INSERT IGNORE INTO cities (city, img_link) VALUES
            ('Toruń', 'https://imgs.search.brave.com/Soh5XOt330xU5SPGKU7Ffq25Ts1mHJXtiHxpQLrZL90/rs:fit:1200:1060:1/g:ce/aHR0cDovL3d3dy53/ZWlzcy10cmF2ZWwu/Y29tL3dwLWNvbnRl/bnQvdXBsb2Fkcy8y/MDE4LzAxL1RvcnVu/LXN3aWV0by5qcGc'),
            ('Kraków', 'https://imgs.search.brave.com/HMdj6Gmuu4WVD2xkPDeiTEly-cM83jR8-6q-yeNO1Ak/rs:fit:1200:1200:1/g:ce/aHR0cHM6Ly9kbWNw/b2xhbmQuY29tL3dw/LWNvbnRlbnQvdXBs/b2Fkcy8yMDE3LzAy/L2tyYWtvdzMuanBn'),
            ('Warszawa', 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c9/Poland-00808_-_Castle_Square_%2831215382745%29.jpg/800px-Poland-00808_-_Castle_Square_%2831215382745%29.jpg'),
            ('Bydgoszcz', 'https://imgs.search.brave.com/eM6ucCwizZvIhNnDJ__ZD7J3x1r_GjqkpZoasSOh_5A/rs:fit:1200:960:1/g:ce/aHR0cHM6Ly93d3cu/c3RheXBvbGFuZC5j/b20vd3AtY29udGVu/dC91cGxvYWRzLzIw/MTcvMDgvYnlkZ29z/emN6LTkwNDA5M18x/MjgwLmpwZw'),
            ('Rzeszów', 'https://imgs.search.brave.com/MHbxCQ_6Llfcgso4cI9Hk8aOsukadb8HtLoMFmeSk1k/rs:fit:1110:600:1/g:ce/aHR0cHM6Ly9zdGF0/aWMucG9sc2tpZXN6/bGFraS5wbC96ZGpl/Y2lhL3d5Y2llY3pr/aS8yMDE2LTA0LzEx/MTBfNjAwLzMyNjI5/LW56LTE0NjEyMzcz/MzIuanBn')
        """

        with self._connection.cursor() as cursor:
            cursor.execute(create_cities_table_query)
            cursor.execute(insert_into_cities_query)
            self._connection.commit()

    def create_ticket_table(self):
        create_ticket_table_query = """
        CREATE TABLE IF NOT EXISTS ticket (
            ticket_id VARCHAR(53) NOT NULL PRIMARY KEY,
            ride_id VARCHAR(50) NOT NULL,
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
            ride_id VARCHAR(50) NOT NULL PRIMARY KEY,
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
            ('1-WaKrk-202302101003', '2023-02-10 10:03:00', '2023-02-10 09:01:00', 'Warszawa', 'Kraków', 23,  175),
            ('5-WaKrk-202302101011', '2023-02-10 10:11:00', '2023-02-10 09:21:00', 'Warszawa', 'Kraków', 24,  176),
            ('3-RzeTor-202302071213', '2023-02-07 12:13:00', '2023-02-07 10:13:00', 'Rzeszów', 'Toruń', 23,  205)
            """

        with self._connection.cursor() as cursor:
            cursor.execute(create_ride_table_query)
            cursor.execute(insert_into_rides)
            self._connection.commit()

    def create_all(self):
        self.create_cities_table()
        self.create_rides_table()
        self.create_users_table()
        self.create_ticket_table()


if __name__ == "__main__":
    xd = Database()
    #xd.create_all()

    """print(xd.list_connections("Kraków", "Warszawa", '2023-02-10'))
    print(xd.list_connections("Kraków", "Warszawa", '2023-02-10'))
    print(xd.get_city_img_link("Kraków"))
    print(xd.get_free_seats('1-WaKrk-202302101003'))"""
    (xd.update_db())

