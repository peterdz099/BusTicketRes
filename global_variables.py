from kivy.uix.screenmanager import ScreenManager
from database_handler.init_db import Database
from database_handler.users import Users


sm = ScreenManager()

db = Database()
db.create_all()

usersResources = Users(db)

