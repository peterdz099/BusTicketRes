import os
import smtplib
import ssl
import webbrowser
from email.message import EmailMessage
import random
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from database_handler.users import is_pwd_correct
from global_variables import sm, usersResources


class LoginWindow(Screen):

    attempts = 0

    email_or_username = ObjectProperty(None)
    password = ObjectProperty(None)

    generated_code = None
    email = None

    def login(self):
        half_screen_manager = self.ids.half_screen_manager
        dictionary = usersResources.select_user(email=self.email_or_username.text, username=self.email_or_username.text)
        print(dictionary)

        if self.email_or_username.text != "" and self.password != "":
            if dictionary and dictionary.get('is_verified') == 1:
                if is_pwd_correct(self.password.text, dictionary.get('password')):
                    self.reset()
                    sm.current = "main"
                else:
                    self.ids.login_message.text = "Wrong password"

            elif dictionary and dictionary.get('is_verified') == 0:
                if is_pwd_correct(self.password.text, dictionary.get('password')):

                    half_screen_manager.current = "half_screen_verify"
                    half_screen_manager.transition.direction = "down"
                    LoginWindow.generated_code = random.randint(100000, 1000000)
                    LoginWindow.email = dictionary.get('email')

                    self.send_email()

                    print(dictionary.get('email'))
                    print(LoginWindow.generated_code)

                    self.reset()

                else:
                    self.ids.login_message.text = "Wrong password"
            else:
                self.ids.login_message.text = "User not found"
        else:
            self.ids.login_message.text = "Fill fields below"

    def verify(self):
        if LoginWindow.attempts <= 3:
            if self.ids.code.text != "":
                if self.ids.code.text == str(LoginWindow.generated_code):
                    print('success')
                    usersResources.verify_user(email=LoginWindow.email, username=LoginWindow.email)
                    self.ids.half_screen_manager.current = "half_screen_login"
                    self.reset_verify_screen()
                    self.ids.login_message.text = "Verification successful"

                else:
                    self.ids.verification_message.text = "Try again"
                    LoginWindow.attempts += 1
        else:
            LoginWindow.attempts = 0
            self.ids.half_screen_manager.current = "half_screen_login"
            self.reset_verify_screen()
            self.ids.login_message.text = "You have exceeded the number of verification attempts"

    @staticmethod
    def send_email():
        email_sender = "toysapp8@gmail.com"
        email_password = os.environ.get("EMAIL_PASSWORD")

        email_receiver = LoginWindow.email

        subject = "Verification Code"

        print(LoginWindow.generated_code)

        body = f"""Type your verification code in application\nYour Code: {LoginWindow.generated_code}"""

        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = email_receiver
        em['Subject'] = subject
        em.set_content(body)

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_receiver, em.as_string())

    def create_new_account(self):
        self.reset()
        sm.current = "register"

    def reset(self):
        self.email_or_username.text = ""
        self.password.text = ""
        self.ids.login_message.text = "Log in or create new account"

    def reset_verify_screen(self):
        self.ids.verification_message.text = "Enter the verification code sent to your email below"
        self.ids.code.text = ""
        self.ids.half_screen_manager.current = "half_screen_login"
        self.ids.half_screen_manager.transition.direction = "up"
        LoginWindow.generated_code = None

    @staticmethod
    def go_to_github():
        webbrowser.open("https://github.com/peterdz099/BusTicketRes")

    @staticmethod
    def go_to_py():
        webbrowser.open("https://www.python.org/")

    @staticmethod
    def go_to_sql():
        webbrowser.open("https://www.mysql.com/")

