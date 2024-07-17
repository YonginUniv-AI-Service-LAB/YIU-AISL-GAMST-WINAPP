class PsInfo:
    identifier = None
    name = None
    title = None
    time = None

    @classmethod
    def update_state(cls, identifier, name, title, time):
        cls.identifier = identifier
        cls.name = name
        cls.title = title
        cls.time = time
