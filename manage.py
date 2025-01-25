from sys import argv

from commands.user_creation_command import UserCreationCommand
from common.utils.load_env_file import load_env_file  # noqa

match argv[1]:
    case "create_user":
        UserCreationCommand()
    case _:
        print("Incorrect command")
