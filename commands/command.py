class Command:

    def __init__(self):
        self.handle()

    def handle(self):
        raise NotImplementedError("Method handle is not implemented!")
