# add bearer token validator
import time

import requests
from authlib.specs.rfc6749.util import scope_to_list
from authlib.specs.rfc6750 import BearerTokenValidator


class HydraBearerTokenValidator(BearerTokenValidator):
    def authenticate_token(self, token_string):
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json'
        }

        r = requests.post('http://localhost:4445/oauth2/introspect',
                          data={
                              'token': token_string
                          },
                          headers=headers)

        resp = r.json()
        return resp

    def token_expired(self, token):
        if not token['active']:
            return True
        expires_at = token['exp']
        return int(time.time()) > expires_at

    def request_invalid(self, request):
        return False

    def token_revoked(self, token):
        return False

    def scope_insufficient(self, token, scope, operator='AND'):
        if not scope:
            return False
        token_scopes = set(scope_to_list(token['scope']))
        resource_scopes = set(scope_to_list(scope))
        if operator == 'AND':
            return not token_scopes.issuperset(resource_scopes)
        if operator == 'OR':
            return not token_scopes & resource_scopes
        if callable(operator):
            return not operator(token_scopes, resource_scopes)
        raise ValueError('Invalid operator value')