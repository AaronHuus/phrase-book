import os

from configparser import ConfigParser

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from phrase_book import app, db, Settings, PHRASE_BOOK_SETTINGS

# Set up Settings
settings: Settings = Settings()
config_parser = ConfigParser()

if PHRASE_BOOK_SETTINGS in os.environ:
    config_path = os.environ[PHRASE_BOOK_SETTINGS]
else:
    config_path = f'{os.getcwd()}/etc/phrase-book-config.ini'

if not os.path.isfile(config_path):
    raise FileNotFoundError(f'{config_path} is not a valid path to a config file')
config_parser.read(config_path)

settings.init_from_config(config_parser)
settings.load_into_app_config(app.config)

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
