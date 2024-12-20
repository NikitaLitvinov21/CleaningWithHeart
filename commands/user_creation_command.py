from datetime import date
from getpass import getpass

from commands.command import Command
from exceptions.command_exception import CommandException
from schemes.user_scheme import UserScheme
from services.user_service import UserService
from utils.load_env_file import load_env_file


class UserCreationCommand:

    def __init__(self):
        self.user_service = UserService()
        # self.super().__init__()
        self.handle()

    def handle(self) -> None:
        username = input("[Required] Input username: ")
        password = getpass("[Required] Input password (It is hidden): ")
        first_name = input("[Optional] Input first name: ")
        last_name = input("[Optional] Input last name: ")
        phone_number = input("[Optional] Input phone number: ")
        email_address = input("[Optional] Input email: ")
        try:
            birth_date = date(
                input("[Optional] Input birth date (Example, '2000-12-28'): ")
            )
        except TypeError:
            birth_date = None

        UserScheme(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            email_address=email_address,
            birth_date=birth_date,
        )

        if self.user_service.is_user_exists(username=username):
            raise CommandException("User already exists!")

        if username and password:
            self.user_service.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                phone_number=phone_number,
                email_address=email_address,
                birth_date=birth_date,
            )
            print("Registered new user!")
        else:
            CommandException("Username and Password are required!")
