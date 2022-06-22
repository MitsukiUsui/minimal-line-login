import os
import urllib.parse
from logging import getLogger

import requests

CLIENT_ID = os.getenv('LINE_CLIENT_ID')
CLIENT_SECRET = os.getenv('LINE_CLIENT_SECRET')

AUTH_URL = 'https://access.line.me/oauth2/v2.1/authorize'
TOKEN_URL = 'https://api.line.me/oauth2/v2.1/token'
PROFILE_URL = 'https://api.line.me/v2/profile'
REVOKE_URL = 'https://api.line.me/oauth2/v2.1/revoke'
CALLBACK_URL = 'http://127.0.0.1:5000/callback'

LOGGER = getLogger(__name__)


def build_login_url(state):
    query_params = {
        'response_type': 'code',
        'client_id': CLIENT_ID,
        'redirect_uri': CALLBACK_URL,
        'state': state,
        'scope': 'profile'
    }
    return AUTH_URL + '?' + urllib.parse.urlencode(query_params)


def fetch_token(code):
    LOGGER.debug(f'fetch token')
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': CALLBACK_URL,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    }
    response = requests.post(TOKEN_URL, headers=headers, data=data)
    data = response.json()
    LOGGER.debug(f'fetched token data: {data}')
    return data


def fetch_profile(access_token):
    LOGGER.debug(f'fetch profile')
    # TODO: verify access_token
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(PROFILE_URL, headers=headers)
    data = response.json()
    LOGGER.debug(f'fetched profile data: {data}')
    return data


def revoke_token(access_token):
    LOGGER.debug(f'revoke token')
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'access_token': access_token
    }
    response = requests.post(REVOKE_URL, headers=headers, data=data)
    if not response.ok:
        raise RuntimeError(response.text)
    return True
