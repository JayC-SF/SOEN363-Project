from utility.auth_token import SPOTIFY_AUTH_TOKEN
from utility.utility import is_success_code, send_request_with_wait
import pandas as pd
import requests
from requests import Response
import os
import json
from pathlib import Path

from utility.variables import SPOTIFY_API_URL, SPOTIFY_DATA_PATH, SPOTIFY_ITEMS_CSV_NAME, SPOTIFY_ITEMS_FOLDER_NAME

# sample curl request of a playlist
"""
curl --request GET \
  --url https://api.spotify.com/v1/playlists/3cEYpjA9oz9GiPac4AsH4n \
  --header 'Authorization: Bearer 1POdFZRZbvb...qqillRxMr2z'
"""


def scrape_scrape_items(items_folder: str, item_type: str):
    """
    """
    # setup path string of where the json items are stored
    items_data_path = f"{items_folder}/{SPOTIFY_ITEMS_FOLDER_NAME}"
    csv_file_path = f"{items_folder}/{SPOTIFY_ITEMS_CSV_NAME}"
    # Create folders if they don't exist
    Path(items_data_path).mkdir(parents=True, exist_ok=True)
    # add a .gitkeep file if it doesn't exist
    open(f"{items_data_path}/.gitkeep", "a")
    # log info
    print(f'SCRAPING {item_type.upper()}')
    # create csv file if doesn't exist
    if not os.path.exists(csv_file_path):
        with open(csv_file_path, "w") as f:
            f.write('ID')
        print(f"No data currently stored for {item_type}, successfully created folders and file.")
    # read csv file
    df = pd.read_csv(csv_file_path)
    for _, row in df.iterrows():
        id = row['ID']
        item_file_path = f"{items_data_path}/{id}.json"
        # skip if the item has already been scraped
        if os.path.exists(item_file_path):
            print(f"{item_type} {id} is cached, skip scraping.")
            continue
        # if we exceed time limit, re scrape after time sleep
        res = send_request_with_wait(scrape_single_item, id)

        # check if we still have a success code
        if not is_success_code(res.status_code):
            raise Exception(f"Status error code while fetching {id}: {res.status_code}")

        print(f"Successfully scraped {id}: {res.status_code}")
        # dump playlist data in its own file
        with open(item_file_path, "w") as f:
            json.dump(res.json(), f, indent=2)


def scrape_single_item(id, endpoint) -> Response:
    """
    """
    URL = f"{SPOTIFY_API_URL}/{endpoint}/{id}"
    headers = {
        'Authorization': f"{SPOTIFY_AUTH_TOKEN.get_authorization()}"
    }
    res = requests.get(url=URL, headers=headers)
    return res
