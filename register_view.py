from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from validate_email import validate_email

from global_variables import usersResources, sm


class RegisterWindow(Screen):

    email = ObjectProperty(None)
    username = ObjectProperty(None)
    password = ObjectProperty(None)
    repeatedPassword = ObjectProperty(None)

    def submit(self):

        if self.username.text != "" and self.email.text != "" and self.password.text != "" \
                and self.repeatedPassword.text != "":

            dictionary = usersResources.select_user(username=self.username.text, email=self.email.text)

            check = bool(dictionary)

            if not validate_email(self.email.text):
                self.ids.new_account_message.text = "use real e-mail"
                self.reset()

            elif self.password.text != self.repeatedPassword.text:
                self.ids.new_account_message.text = "Passwords don't match"
                self.reset()
            elif check:
                self.ids.new_account_message.text = "User Already Exists"
            else:
                if self.password.text == self.repeatedPassword.text and validate_email(self.email.text):
                    usersResources.add_user(self.username.text, self.password.text, self.email.text)
                    self.reset()
                    self.ids.new_account_message.text = "Create new account!"
                    sm.current = "login"
                    print("OK")
        else:
            self.ids.new_account_message.text = "Fill out all the form fields"
            self.reset()

    def reset(self):
        self.email.text = ""
        self.password.text = ""
        self.username.text = ""
        self.repeatedPassword.text = ""

    def back_to_login(self):
        self.reset()
        sm.current = "login"
