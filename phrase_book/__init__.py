import json
import logging.config
import os
from configparser import ConfigParser
from http.client import HTTPException

from authlib.flask.error import _HTTPException
from authlib.flask.oauth2 import ResourceProtector
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

from phrase_book.settings.constants import PHRASE_BOOK_SETTINGS, SQLALCHEMY_TRACK_MODIFICATIONS
from phrase_book.settings.settings import Settings

# Set up Logging
from phrase_book.utils.oauth2 import HydraBearerTokenValidator
from phrase_book.utils.phrase_book_json_encoder import PhraseBookJSONEncoder

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

app = Flask(__name__)
app.url_map.strict_slashes = False
app.json_encoder = PhraseBookJSONEncoder
settings.load_into_app_config(app.config)
app.config[SQLALCHEMY_TRACK_MODIFICATIONS] = False
db = SQLAlchemy(app)

# Set up Flask App
require_oauth = ResourceProtector()
require_oauth.register_token_validator(HydraBearerTokenValidator())
from phrase_book.api.phrases import phrases_blueprint
from phrase_book.api.books import books_blueprint
app.register_blueprint(books_blueprint, url_prefix='/books')
app.register_blueprint(phrases_blueprint, url_prefix='/books/<book_id>/phrases')

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


# Oauth 2.0 Unauthorized
@app.errorhandler(_HTTPException)
def handle_http_exception(e):
    body = json.loads(e.body)
    body['status'] = 'PERMISSION_DENIED'
    return jsonify(body), e.code

# Catch all error handler. Can start breaking out into more specific error handling as needed
@app.errorhandler(Exception)
def error_handler(e):
    print(type(e))
    status_code = e.code if hasattr(e, 'code') else 500
    return jsonify(_generate_response(status_code, e.description if hasattr(e, 'description') else str(e))), status_code


def _generate_response(status_code: int, message: str):
    return {
        'status_code': status_code,
        'message': message
    }
