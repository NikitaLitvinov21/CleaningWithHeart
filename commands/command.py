from abc import ABCMeta, abstractmethod


class Command(ABCMeta):

    def __init__(self):
        self.handle()

    @abstractmethod
    def handle(self):
        pass
