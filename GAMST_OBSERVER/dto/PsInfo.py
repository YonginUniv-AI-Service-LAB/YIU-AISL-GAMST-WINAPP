class PsInfo:
    identifier = None
    name = None
    title = None

    @classmethod
    def update_state(cls, identifier, name, title):
        cls.identifier = identifier
        cls.name = name
        cls.title = title
