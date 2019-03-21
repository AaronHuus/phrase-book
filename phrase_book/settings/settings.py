import logging

from phrase_book.settings import get_string, POSTGRES_SECTION, HOST, USER, PASSWORD, DATABASE

logger = logging.getLogger(__name__)

HIDDEN_SETTINGS = []


class Settings:
    def __init__(self):
        self._postgres_host = None
        self._postgres_user = 'popshop'
        self._postgres_password = None
        self._postgres_database = 'popshop'

    def init_from_config(self, config):
        self.postgres_host = get_string(config, POSTGRES_SECTION, HOST, self._postgres_host)
        self.postgres_user = get_string(config, POSTGRES_SECTION, USER, self._postgres_user)
        self.postgres_password = get_string(config, POSTGRES_SECTION, PASSWORD, self._postgres_password)
        self.postgres_database = get_string(config, POSTGRES_SECTION, DATABASE, self._postgres_database)

    def to_json(self):
        property_names = [p for p in dir(Settings) if isinstance(getattr(Settings, p), property)]
        configs = {}
        for prop in [p for p in property_names if p.upper() not in HIDDEN_SETTINGS]:
            value = getattr(self, prop)
            configs[prop] = value

        return configs

    # Properties

    @property
    def postgres_host(self) -> int:
        return self._postgres_host

    @postgres_host.setter
    def postgres_host(self, value):
        self._postgres_host = value

    @property
    def postgres_user(self) -> int:
        return self._postgres_user

    @postgres_user.setter
    def postgres_user(self, value):
        self._postgres_user = value

    @property
    def postgres_password(self) -> int:
        return self._postgres_password

    @postgres_password.setter
    def postgres_password(self, value):
        self._postgres_password = value

    @property
    def postgres_database(self) -> int:
        return self._postgres_database

    @postgres_database.setter
    def postgres_database(self, value):
        self._postgres_database = value
