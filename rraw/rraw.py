import json
from time import time
from os import path

from oauthlib.oauth2 import LegacyApplicationClient, TokenExpiredError
from requests_oauthlib import OAuth2Session

TOKEN_URL = 'https://www.reddit.com/api/v1/access_token'
OAUTH_BASE = 'https://oauth.reddit.com'

class Reddit:
    def __init__(self, client_id, client_secret, username, password, app, token_file=None):
        self.rate = {}
        self.token = {}
        self.username = username
        self.password = password
        self.client_id = client_id
        self.client_secret = client_secret

        if token_file and path.exists(token_file):
            self.token = json.load(open(token_file, 'r'))

        self.token_file = token_file

        client = LegacyApplicationClient(client_id=client_id)

        session = OAuth2Session(client=client, token=self.token)

        user_agent = '{app} (by {username})'.format(app=app, username=username)

        session.headers.update({ 'User-Agent': user_agent })

        self.session = session

    def update_token(self, force=True):

        expiration = self.token.get('expires_at', 0)

        if time() < expiration and not force:
            return

        self.token = self.session.fetch_token(
            token_url=TOKEN_URL,
            username=self.username,
            password=self.password,
            client_id=self.client_id,
            client_secret=self.client_secret,
        )

        if self.token_file:
            json.dump(self.token, open(self.token_file, 'w'))

    def get(self, endpoint, params={}, raw=False):
        return self.request('GET', endpoint, params=params)

    def put(self, endpoint, json=None, params={}, raw=False):
        return self.request('PUT', endpoint, json=json)

    def post(self, endpoint, json=None, params={}, raw=False):
        return self.request('POST', endpoint, json=json, params=params)

    def delete(self, endpoint, params={}, raw=False):
        return self.request('DELETE', endpoint, json=json, params=params)

    def request(self, method, endpoint, json=None, data={}, params={}, raw=False):
        params.update({'raw_json': 1})

        limit = self.rate_limit()

        if limit:
            print('Rate limited. Sleeping for', limit, 'seconds')
            sleep(limit)

        self.update_token()

        url = OAUTH_BASE + endpoint

        response = self.session.request(method, url, json=json, data=data, params=params)

        self.update_rate(response.headers)

        if not response.ok:
            raise Exception(response.reason, response.text)

        if raw:
            return response.text

        return response.json()

    def rate_limit(self):

        if not self.rate or self.rate['remaining']:
            return 0

        now = time()

        duration = now - self.rate['reset']

        return duration

    def update_rate(self, headers):

        used = int(headers.get('x-ratelimit-used', 0))
        # Remaining is an estimate
        remaining = float(headers.get('x-ratelimit-remaining', 0))
        reset = int(headers.get('x-ratelimit-reset', 0))

        now = time()

        self.rate = {
            'used': used,
            'remaining': remaining,
            'reset': now + reset,
        }

