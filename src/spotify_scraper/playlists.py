from utility import variables as var
from utility.utility import is_success_code
import pandas as pd
import requests
from requests import Response
import time
import os
import json

# sample curl request of a playlist
"""
curl --request GET \
  --url https://api.spotify.com/v1/playlists/3cEYpjA9oz9GiPac4AsH4n \
  --header 'Authorization: Bearer 1POdFZRZbvb...qqillRxMr2z'
"""

SPOTIFY_PLAYLISTS_PATH = f"{var.DATA_PATH}/spotify_playlists"
PLAYLISTS_DATA_PATH = f"{SPOTIFY_PLAYLISTS_PATH}/playlist_data"
PLAYLISTS_CSV_PATH = f"{SPOTIFY_PLAYLISTS_PATH}/playlists.csv"


def scrape_playlists():
    """
    """
    print('SCRAPING PLAYLISTS')
    df = pd.read_csv(PLAYLISTS_CSV_PATH)
    for _, row in df.iterrows():
        playlist_id = row['PLAYLIST ID']
        playlist_path = f"{PLAYLISTS_DATA_PATH}/{playlist_id}.json"
        # skip if the playlist has already been scraped
        if os.path.exists(playlist_path):
            print(f"Playlist {playlist_id} is cached, skip scraping.")
            continue
        # if we exceed time limit, re scrape after time sleep
        res = scrape_single_playlist(playlist_id)
        while (res.status_code == var.SPOTIFY_RATE_LIMIT_RESPONSE_CODE):
            print(f"INFO: Exceeded rate limit, sleeping for {res.headers['Retry-After']} seconds")
            time.sleep(seconds=res.headers['Retry-After'])

        # check if we still have a success code
        if not is_success_code(res.status_code):
            raise Exception(f"Status error code while fetching {playlist_id}: {res.status_code}")

        print(f"Successfully scraped {playlist_id}: {res.status_code}")
        # dump playlist data in its own file
        with open(playlist_path, "w") as f:
            json.dump(res.json(), f, indent=2)


def scrape_single_playlist(playlist_id) -> Response:
    """
    """
    URL = f"{var.SPOTIFY_API_URL}/{var.SPOTIFY_PLAYLIST_ENDPOINT}/{playlist_id}"
    headers = {
        'Authorization': f"{var.SPOTIFY_AUTH_TOKEN.get_authorization()}"
    }
    res = requests.get(url=URL, headers=headers)
    return res
