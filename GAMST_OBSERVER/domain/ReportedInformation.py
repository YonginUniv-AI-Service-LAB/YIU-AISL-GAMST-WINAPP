class ReportedInformation:
    def __init__(self):
        self.identifier = None
        self.foreground_name = None
        self.foreground_title = None
        self.cursor_name = None
        self.cursor_title = None
        self.unix_time = None

    def update_state(self, identifier, fg_name, fg_title, cs_name, cs_title, unix_time):
        self.identifier = identifier
        self.foreground_name = fg_name
        self.foreground_title = fg_title
        self.cursor_name = cs_name
        self.cursor_title = cs_title
        self.unix_time = unix_time


from GAMST_OBSERVER.connection.address import *

ps_informations = [ReportedInformation() for _ in range(CLIENT_COUNTS)]
