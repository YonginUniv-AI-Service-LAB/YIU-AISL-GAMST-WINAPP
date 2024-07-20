class ProcessInformation:
    def __init__(self):
        self.identifier = None
        self.foreground_name = None
        self.foreground_title = None
        self.cursor_name = None
        self.cursor_title = None
        self.time = None

    def update_state(self, identifier, fg_name, fg_title, cs_name, cs_title, time):
        self.identifier = identifier
        self.foreground_name = fg_name
        self.foreground_title = fg_title
        self.cursor_name = cs_name
        self.cursor_title = cs_title
        self.time = time


from GAMST_OBSERVER.configuration.address import *

ps_informations = [ProcessInformation() for _ in range(len(OUTBOUND_HOST))]
