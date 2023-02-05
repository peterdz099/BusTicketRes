from kivy.core.window import Window
from kivy.lang import Builder
from kivy.config import Config
from kivymd.app import MDApp
from login_view import LoginWindow
from main_view import MainWindow
from register_view import RegisterWindow
from global_variables import sm, db


def back():
    sm.current = "login"


class MyApp(MDApp):
    def build(self):
        #Window.borderless = True
        self.theme_cls.theme_style = "Light"
        self.theme_cls.material_style = "M3"

        Builder.load_file('register_view.kv')
        Builder.load_file('login_view.kv')
        Builder.load_file('main_view.kv')
        sm.add_widget(LoginWindow(name="login"))
        sm.add_widget(RegisterWindow(name="register"))
        sm.add_widget(MainWindow(name="main"))
        sm.get_screen("main").on_start()
        sm.current = "login"
        #db.create_all()
        return sm

if __name__ == '__main__':
    Config.set('graphics', 'width', '1000')
    Config.set('graphics', 'height', '800')
    Config.set('graphics', 'resizable', False)
    Config.write()
    MyApp().run()


