from abc import ABC, abstractmethod


class BaseCommand(ABC):
    """
    Abstract base class for all commands.
    """

    @abstractmethod
    def handle(self) -> None:
        """
        Main method for executing the command.
        """
        pass
