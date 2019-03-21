import ast
import os

from phrase_book.settings.constants import TRUTHY_INPUT
from phrase_book.utils.util import camel_case_to_snake_case

DATABASE = 'Database'

HOST = 'Host'

PASSWORD = 'Password'
POSTGRES_SECTION = 'Postgres'

USER = 'User'


def get_int(config, section, key, default_value: int) -> int:
    return _get_value(config, section, key, default_value, int(1))


def get_boolean(config, section, key, default_value: bool) -> bool:
    return _get_value(config, section, key, default_value, True)


def get_float(config, section, key, default_value: float) -> float:
    return _get_value(config, section, key, default_value, float(1.0))


def get_string(config, section, key, default_value: str) -> str:
    return _get_value(config, section, key, default_value, str('type'))


def get_tuple(config, section, key, default_value: tuple) -> tuple:
    return _get_value(config, section, key, default_value, tuple(()))


def get_list(config, section, key, default_value: list) -> list:
    return _get_value(config, section, key, default_value, list(()))


def get_dict(config, section, key, default_value: dict) -> dict:
    return _get_value(config, section, key, default_value, dict(()))


def _get_value(config, section, key, default_value, value_type):
    environment_variable_name = f'{camel_case_to_snake_case(section).upper()}_{camel_case_to_snake_case(key).upper()}'
    value = os.environ.get(environment_variable_name, config.get(section, key, fallback=None))

    if isinstance(default_value, bool):
        if isinstance(value, str):
            return value.lower() in TRUTHY_INPUT
        else:
            return bool(value)
    elif isinstance(value_type, list):
        return value.split(',')
    elif isinstance(value_type, dict):
        d = ast.literal_eval(value)
        return d
    else:
        return type(value_type)(value) if value else value
