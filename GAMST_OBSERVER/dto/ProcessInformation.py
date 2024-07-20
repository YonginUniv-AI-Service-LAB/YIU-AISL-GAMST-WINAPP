class ProcessInformation:
    def __init__(self, name=None, title=None, time=None):
        self.identifier = None
        self.name = name
        self.title = title
        self.time = time

    def update_state(self, identifier, name, title, time):
        self.identifier = identifier
        self.name = name
        self.title = title
        self.time = time


from GAMST_OBSERVER.configuration.address import *

ps_informations = [ProcessInformation() for _ in range(len(OUTBOUND_HOST))]
