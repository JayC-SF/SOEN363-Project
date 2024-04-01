from typing import Iterable
from utility.auth_token import SPOTIFY_AUTH_TOKEN
from utility.utility import is_success_code, send_request_with_wait
import pandas as pd
import requests
from requests import Response
import os
from os.path import join as joinpath, abspath
import json
from pathlib import Path

from utility.variables import DATA_PATH, SPOTIFY_API_URL, SPOTIFY_BATCH_MAX_ITEMS, SPOTIFY_DATA_PATH

# sample curl request of a playlist
"""
curl --request GET \
  --url https://api.spotify.com/v1/playlists/3cEYpjA9oz9GiPac4AsH4n \
  --header 'Authorization: Bearer 1POdFZRZbvb...qqillRxMr2z'
"""


class SpotifyScraper:

    def __init__(self, endpoint: str):
        self.__endpoint = endpoint
        self.__data_path = abspath(joinpath(SPOTIFY_DATA_PATH, endpoint))
        self.__csv_file_path = abspath(joinpath(SPOTIFY_DATA_PATH, f"{endpoint}/ids.csv"))
        self.__items_folder_path = joinpath(self.__data_path, 'items')
        self.setup_folders()

    def setup_folders(self):
        # Create folders if they don't exist
        Path(self.__items_folder_path).mkdir(parents=True, exist_ok=True)
        # add a .gitkeep file if it doesn't exist
        open(joinpath(self.__items_folder_path, ".gitkeep"), "a")
        # log info

        # create csv file if doesn't exist
        if not os.path.exists(self.__csv_file_path):
            with open(self.__csv_file_path, "w") as f:
                f.write('ID')
            print(f"No data currently stored for {self.__endpoint}, successfully created folders and file.")

    def scrape_items(self, batchmode: bool = False):
        """Scrapes items using ids defined in csv file

        Args:
            batchmode (bool, optional): Performs batchmode scraping request. Defaults to False.
        """
        if batchmode:
            self.scrape_batch_items()
        else:
            self.scrape_nonbatch_items()

    def scrape_nonbatch_items(self):
        """Scrapes items without using batchmode requests. Performs a request for each ids in the csv file.
        The function stores the output of the request in a json file.
        The function skips all ids that are cached.

        Raises:
            Exception: An exception is the code is neither 429 or a success code.
        """
        print(f'SCRAPING {self.__endpoint.upper()}')
        # read csv file
        df = pd.read_csv(self.__csv_file_path)
        error_request = set()
        for _, row in df.iterrows():
            id = row['ID']
            item_file_path = joinpath(self.__items_folder_path, f"{id}.json")
            # skip if the item has already been scraped
            if os.path.exists(item_file_path):
                print(f"{id} in {self.__endpoint} is cached, skip scraping.")
                continue

            # if we exceed time limit, re scrape after time sleep
            res = send_request_with_wait(SpotifyScraper.scrape_single_id, self, id)

            # check if we still have a success code
            if not is_success_code(res.status_code):
                error_request.add(id)
                print(f"Status error code while fetching {id}: {res.status_code}\n{res.json()}")
                continue

            print(f"Successfully scraped {id}: {res.status_code}")
            # dump playlist data in its own file
            with open(item_file_path, "w") as f:
                json.dump(res.json(), f, indent=2)

        df = df[~df['ID'].isin(error_request)]
        df.to_csv(self.__csv_file_path, index=False)
        print(f"\nScraping complete, total ids with error: {len(error_request)}")
        print(f"IDS with error request: {'\n'.join(error_request)}")

    def scrape_single_id(self, id: str) -> Response:
        """Scrapes the response of a single id for an item

        Args:
            id (str): Id of the item to be scraped.

        Returns:
            Response: Response object from `requests` library
        """
        URL = f"{SPOTIFY_API_URL}/{self.__endpoint}/{id}"
        headers = {
            'Authorization': f"{SPOTIFY_AUTH_TOKEN.get_authorization()}"
        }
        res = requests.get(url=URL, headers=headers)
        return res

    def scrape_batch_items(self):
        """_summary_

        Raises:
            Exception: _description_
        """
        print(f'SCRAPING {self.__endpoint.upper()}')
        # read csv file
        df = pd.read_csv(self.__csv_file_path)
        df.drop_duplicates()
        cached_ids: set[str] = set()
        # get the cached ids
        for _, row in df.iterrows():
            id = row['ID']
            item_file_path = joinpath(self.__items_folder_path, f"{id}.json")
            # skip if the item has already been scraped
            if os.path.exists(item_file_path):
                print(f"{id} in {self.__endpoint} is cached, skip scraping.")
                cached_ids.add(id)
        # drop ids that are already cached
        df = df[~df['ID'].isin(cached_ids)]

        while (len(df) != 0):
            # get the batch of ids to send in request
            batch_df = set(df[:SPOTIFY_BATCH_MAX_ITEMS]['ID'].to_list())
            df.drop(df.index[:SPOTIFY_BATCH_MAX_ITEMS], inplace=True)

            # send the batch request and check status codes
            res = send_request_with_wait(SpotifyScraper.scrape_batch_ids, self, batch_df)
            if not is_success_code(res.status_code):
                raise Exception(f"Status error code {res.status_code} while fetching:\n{str(res.content)}\n{"\n".join(batch_df)}")

            # get the json response
            items = res.json()
            with open("out.json", "w") as f:
                json.dump(items, f, indent=2)
            # store each scraped item in its folder.
            for item in items[self.__endpoint]:
                # skip the null ones
                if (item is None):
                    continue
                id = item['id']
                item_file_path = joinpath(self.__items_folder_path, f"{id}.json")
                print(f"Successfully scraped {id}: {res.status_code}.")
                # dump playlist data in its own file
                with open(item_file_path, "w") as f:
                    json.dump(item, f, indent=2)
                batch_df.remove(id)

            # log all missing ids from that batch request
            for missing_id in batch_df:
                f"Response is missing {missing_id} in batch request."

    def scrape_batch_ids(self, ids: Iterable[str]):
        """_summary_
        """
        if (len(ids) <= 0):
            raise Exception(f"Cannot send 0 ids in {self.__endpoint} batch request.")
        PARAMS = {
            "ids": ",".join(ids)
        }
        URL = f"{SPOTIFY_API_URL}/{self.__endpoint}"
        headers = {
            'Authorization': f"{SPOTIFY_AUTH_TOKEN.get_authorization()}"
        }
        res = requests.get(url=URL, headers=headers, params=PARAMS)
        return res
