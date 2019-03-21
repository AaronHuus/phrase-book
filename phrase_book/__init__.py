import json
import logging.config
import os
from configparser import ConfigParser

from flask import Flask, jsonify

from phrase_book.settings.constants import PHRASE_BOOK_SETTINGS
from phrase_book.settings.settings import Settings

# Set up Logging
if not os.path.isdir('logs'):
    os.mkdir('logs')

with open('logging.json') as f:
    logging_config = json.load(f)
logging.config.dictConfig(logging_config)

logger = logging.getLogger(__name__)

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

# Set up Flask App
from phrase_book.api.books import books_blueprint
from phrase_book.api.phrases import phrases_blueprint

app = Flask(__name__)
# app.register_blueprint(display_blueprint, url_prefix='/')
app.register_blueprint(books_blueprint, url_prefix='/books')
app.register_blueprint(phrases_blueprint, url_prefix='/books/<book_id>')


###############
# Base Routes
###############

@app.route('/version.json', methods=['GET'])
def version():
    try:
        with open('version.json', 'r') as version_file:
            version_json = json.loads(version_file.read())
        return jsonify(version_json)
    except FileNotFoundError:
        return jsonify({
            'status': 404,
            'message': 'version.json file does not exist'
        }), 404


# Catch all error handler. Can start breaking out into more specific error handling as needed
@app.errorhandler(Exception)
def error_handler(e):
    status_code = e.code if hasattr(e, 'code') else 500
    return jsonify(_generate_response(status_code, e.description if hasattr(e, 'description') else str(e))), status_code


def _generate_response(status_code: int, message: str):
    return {
        'status_code': status_code,
        'message': message
    }
