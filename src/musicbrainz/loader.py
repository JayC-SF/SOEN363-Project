import pandas as pd
import os
import json
import csv

from musicbrainz.util import setup_musicbrainz_folders
from utility.variables import MUSICBRAINZ_ARTISTS_DATA_ITEMS

class AliasLoader:

    def __init__(self, endpoint: str):
        self.__endpoint = endpoint
        self.__artists_items_path = MUSICBRAINZ_ARTISTS_DATA_ITEMS
        self.__data_path, self.__csv_file_path, self.__items_folder_path = setup_musicbrainz_folders(endpoint)


    def get_artist_names_from_json(self):
        # List to store the paths of JSON files
        artist_names = []

        # Iterate through all files in the folder
        for root, dirs, files in os.walk(self.__artists_items_path):
            for file in files:
                # Check if the file has a .json extension
                if file.endswith('.json'):
                    # Construct the full path to the JSON file
                    json_file_path = os.path.join(root, file)
                    with open(json_file_path, 'r') as f:
                        # Load JSON content
                        content = json.load(f)
                        # Append JSON content to the list
                        artist_names.append(content["name"])

        return artist_names
    
    def write_artist_names_to_csv(self):
        artist_names = self.get_artist_names_from_json()

        # Write artist names to CSV file
        csv_file_path = os.path.join(self.__csv_file_path)

        print(f"Writing artist names to '{csv_file_path}' ...")
        df = pd.DataFrame({"Names": artist_names})
        df.to_csv(csv_file_path, index=False)

        # df2 = pd.read_csv(csv_file_path)
        # print(df2["Names"].to_list())

        
        
