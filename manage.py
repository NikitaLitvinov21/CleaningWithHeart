from sys import argv

from common.utils.load_env_file import load_env_file  # noqa: Must be first!
from commands.user_creation_command import UserCreationCommand

match argv[1]:
    case "create_user":
        UserCreationCommand()
    case _:
        print("Incorrect command")
