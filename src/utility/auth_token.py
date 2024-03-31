from datetime import datetime
from datetime import timedelta
import requests
from utility.utility import is_success_code
import json
import os
from os.path import abspath, join

from utility.variables import SPOTIFY_AUTH_URL, SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, TEMP_PATH


class AuthToken:
    seconds_bias = 3

    def __init__(self, auth_url: str, client_id: str, client_secret: str, local_storage_path: str):
        """
        """
        self.auth_url: str = auth_url
        self.client_id: str = client_id
        self.client_secret: str = client_secret
        self.local_storage_path = local_storage_path

        # load from localstorage, otherwise initialize with null values
        if os.path.exists(local_storage_path):
            self.loadToken()
        else:
            self.access_token: str = ""
            self.token_type: str = ""
            # expiration date should always start as expired
            self.expires_in = datetime.fromtimestamp(0)

    def get_authorization(self):
        """
        This function refreshes the token before returning the authorization information.
        """
        self.refresh_token()
        return f"{self.token_type} {self.access_token}"

    def is_expired(self) -> bool:
        """
        Check whether the token is about to expire, in case it is, return true.
        """
        # add bias of 3 seconds for expiration
        return self.expires_in < datetime.now() + timedelta(seconds=AuthToken.seconds_bias)

    def refresh_token(self):
        """
        This function refreshes a token if it is about to expire.
        It sends a request to the authenticating server api and resets all attributes
        corresponding to the new token retrieved.
        """
        # no need to refresh token if expired.
        if not self.is_expired():
            return
        # setup authentication headers, send as x-www-form-urlencoded type of data
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        # setup request body
        body = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }
        # send post request
        res = requests.post(self.auth_url, headers=headers, data=body)
        # make sure to have a 200 status code
        if not is_success_code(res.status_code):
            raise Exception("Unable to retrieve access token.")
        # convert response to json and update attributes
        json_res = res.json()
        self.access_token = json_res['access_token']
        self.token_type = json_res['token_type']
        # set the time of expiration to be now + seconds until expiration
        self.expires_in = datetime.now() + timedelta(seconds=json_res['expires_in'])

        # store the token to be reused if not expired
        self.storeTokenToFile()

    def loadToken(self):
        with open(self.local_storage_path, "r") as f:
            token = json.load(f)
        # load information from the token
        self.access_token = token['access_token']
        self.token_type = token['token_type']
        self.expires_in = datetime.fromisoformat(token['expires_in'])

    def storeTokenToFile(self):
        with open(self.local_storage_path, "w") as f:
            store = {
                'access_token': self.access_token,
                'token_type': self.token_type,
                'expires_in': self.expires_in.isoformat()
            }
            json.dump(store, f)


SPOTIFY_AUTH_TOKEN = AuthToken(
    SPOTIFY_AUTH_URL,
    SPOTIFY_CLIENT_ID,
    SPOTIFY_CLIENT_SECRET,
    abspath(join(TEMP_PATH, "spotify_auth_token.json")),
)
