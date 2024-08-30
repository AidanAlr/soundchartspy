from types import SimpleNamespace


class Album(SimpleNamespace):
    def __str__(self):
        return "Album({})".format(self.get_name())

    def __dict__(self):
        return {
            "name": self.get_name(),
            "creditName": self.get_credit_name(),
            "releaseDate": self.get_release_date(),
            "uuid": self.get_uuid(),
            "default": self.get_default(),
            "type": self.get_type()
        }

    def get_name(self):
        return self.name

    def get_credit_name(self):
        return self.credit_name

    def get_release_date(self):
        return self.release_date

    def get_uuid(self):
        return self.uuid

    def get_default(self) -> bool:
        return bool(self.default)

    def get_type(self):
        return self.type
