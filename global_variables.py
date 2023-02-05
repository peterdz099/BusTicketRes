from kivy.uix.screenmanager import ScreenManager
from database_handler.init_db import Database
from database_handler.tickets import Tickets
from database_handler.users import Users


sm = ScreenManager()

db = Database()

usersResources = Users(db)

ticketsResources = Tickets(db)



