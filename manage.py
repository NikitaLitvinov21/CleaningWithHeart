from sys import argv

from dotenv import load_dotenv

from commands.user_creation_command import UserCreationCommand

load_dotenv()

try:
    match argv[1]:
        case "create_user":
            UserCreationCommand()
        case _:
            print("Incorrect command")
except IndexError:
    print("The command required!")
