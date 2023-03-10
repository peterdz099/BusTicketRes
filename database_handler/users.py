import bcrypt
from database_handler.init_db import Database
from mysql.connector import Error


# Returns hashed plain-text password with salt
def hash_password(password):
    byte_pwd = password.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(byte_pwd, salt)


# Checks if plain-text password matches with hashed
def is_pwd_correct(pwd, hashed_pwd) -> bool:
    pwd_byte = pwd.encode('utf-8')
    hashed_pwd_byte = hashed_pwd.encode('utf-8')
    return bcrypt.checkpw(pwd_byte, hashed_pwd_byte)


# Managing users table
class Users:
    def __init__(self, database: Database):
        self.connection = database.get_connection()

    # Inserting user data; Takes plain-text password as argument
    def add_user(self, username, password, email):
        insert_users_query = """
                INSERT INTO users 
                (username, password, email) 
                VALUES (%s, %s, %s)
                """

        hashed_pwd = hash_password(password)
        users_record = (username, hashed_pwd, email)  # arguments passed as query values

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(insert_users_query, users_record)
                self.connection.commit()
        except Error as e:
            print(e)

    # Returns single users row by user_id, username or email (passed as kwargs)
    def select_user(self, **user_fields: object) -> dict:
        select_user_query = """
                        SELECT * FROM users
                        WHERE user_id = %s
                        OR username = %s
                        OR email = %s
                        """

        # Retrieved arguments passed as query values
        user_args = (user_fields.get('id'), user_fields.get('username'), user_fields.get('email'))

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(select_user_query, user_args)
                output = cursor.fetchone()
                if output is not None:
                    # Returns dict containing user data
                    return {'id': output[0], 'username': output[1], 'email': output[2], 'password': output[3],
                            'is_verified': output[4]}
                else:
                    raise Error('No user found')
        except Error as e:
            print(e)

    # Set a user (specified by user_id, username or email in kwargs) is_verified field to 1
    def verify_user(self, **user_fields):
        verify_user_query = """
                UPDATE users
                SET is_verified = true
                WHERE user_id = %s
                OR username = %s
                OR email = %s
                """

        # Retrieved arguments passed as query values
        user_args = (user_fields.get('id'), user_fields.get('username'), user_fields.get('email'))

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(verify_user_query, user_args)
                self.connection.commit()
        except Error as e:
            print(e)
