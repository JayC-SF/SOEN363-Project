
# track to test 4u7EnebtmKWzUH433cf5Qv

import json
from requests import Response
import requests
import pandas as pd
import os
from utility.auth_token import SPOTIFY_AUTH_TOKEN
from utility.utility import is_success_code, send_request_with_wait
from utility.variables import DATA_PATH, SPOTIFY_API_URL, SPOTIFY_PLAYLIST_ENDPOINT

SPOTIFY_TRACKS_PATH = f"{DATA_PATH}/spotify_tracks"
TRACKS_DATA_PATH = f"{SPOTIFY_TRACKS_PATH}/tracks_data"
TRACKS_CSV_PATH = f"{SPOTIFY_TRACKS_PATH}/tracks.csv"


def scrape_tracks():
    print('SCRAPING TRACKS')
    df = pd.read_csv(TRACKS_CSV_PATH)
    for _, row in df.iterrows():
        track_id = row['TRACK ID']
        playlist_path = f"{TRACKS_DATA_PATH}/{playlist_id}.json"
        # skip if the playlist has already been scraped
        if os.path.exists(playlist_path):
            print(f"Playlist {playlist_id} is cached, skip scraping.")
            continue
        # if we exceed time limit, re scrape after time sleep
        res = send_request_with_wait(scrape_single_track, playlist_id)

        # check if we still have a success code
        if not is_success_code(res.status_code):
            raise Exception(f"Status error code while fetching {playlist_id}: {res.status_code}")

        print(f"Successfully scraped {playlist_id}: {res.status_code}")
        # dump playlist data in its own file
        with open(playlist_path, "w") as f:
            json.dump(res.json(), f, indent=2)


def scrape_single_track(track_id) -> Response:
    """Fetches a single track from the spotify api using a track id and returns the response object.

    Args:
        track_id (str): The track id of the track to fetch

    Returns:
        Response: A requests.Response object
    """
    URL = f"{SPOTIFY_API_URL}/{SPOTIFY_PLAYLIST_ENDPOINT}/{track_id}"
    headers = {
        'Authorization': f"{SPOTIFY_AUTH_TOKEN.get_authorization()}"
    }
    res = requests.get(url=URL, headers=headers)
    return res
