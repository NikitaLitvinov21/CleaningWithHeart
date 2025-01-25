from getpass import getpass

from commands.base_command import BaseCommand
from common.exceptions.command_exception import CommandException
from schemes.user_scheme import UserScheme
from services.user_service import UserService


class UserCreationCommand(BaseCommand):

    def __init__(self):
        self.user_service = UserService()
        self.handle()

    def handle(self) -> None:
        username = input("[Required] Input username: ")
        password = getpass("[Required] Input password (It is hidden): ")
        first_name = input("[Optional] Input first name: ")
        last_name = input("[Optional] Input last name: ")
        phone_number = input("[Optional] Input phone number: ")
        email_address = input("[Optional] Input email: ")

        if phone_number == "":
            phone_number = None

        UserScheme(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            email_address=email_address,
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
            )
            print("Registered new user!")
        else:
            raise CommandException("Username and Password are required!")
