from kivy.uix.screenmanager import Screen
from kivymd import app
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from global_variables import sm


class AccountWindow(Screen):
    dialog = None

    def log_out(self):
        self.dialog_close()
        sm.get_screen("main").ids.screen_manager.current = "Search"
        sm.get_screen("main").ids.screen_manager.get_screen("Search").back_to_main()
        sm.get_screen("main").ids.navigation_rail.deselect_item(sm.get_screen("main").ids.search3)
        sm.get_screen("main").ids.navigation_rail.set_current_selected_item(sm.get_screen("main").ids.search1)
        sm.current = "login"

    def show_alert_dialog(self, str):
        if str == "quit":
            self.dialog = MDDialog(
                text=f"Are you sure You want to {str}?",
                buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        theme_text_color="Custom",
                        md_bg_color="#f59122",
                        text_color=(1, 1, 1, 1),
                        on_press=lambda x: self.dialog_close(),
                    ),
                    MDFlatButton(
                        text="QUIT",
                        md_bg_color="#f59122",
                        theme_text_color="Custom",
                        text_color=(1,1,1,1),
                        on_press=lambda x: app.MDApp.get_running_app().stop(),
                    ),
                ],
            )
        elif str == "Log out":
            self.dialog = MDDialog(
                text=f"Are you sure You want to {str}?",
                buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        theme_text_color="Custom",
                        md_bg_color="#f59122",
                        text_color=(1, 1, 1, 1),
                        on_press=lambda x: self.dialog_close(),
                    ),
                    MDFlatButton(
                        text="LOG OUT",
                        md_bg_color="#f59122",
                        theme_text_color="Custom",
                        text_color=(1,1,1,1),
                        on_press= lambda x: self.log_out(),
                    ),
                ],
            )
        self.dialog.open()

    def dialog_close(self):
        self.dialog.dismiss(force=True)

