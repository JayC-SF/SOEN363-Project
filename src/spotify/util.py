import os
from os.path import join as joinpath, abspath
from pathlib import Path

from utility.variables import SPOTIFY_DATA_PATH, SPOTIFY_ITEMS_CSV_NAME, SPOTIFY_ITEMS_FOLDER_NAME


def setup_spotify_folders(endpoint) -> tuple[str]:
    data_path = abspath(joinpath(SPOTIFY_DATA_PATH, endpoint))
    csv_file_path = abspath(joinpath(SPOTIFY_DATA_PATH, f"{endpoint}/{SPOTIFY_ITEMS_CSV_NAME}"))
    items_folder_path = joinpath(data_path, SPOTIFY_ITEMS_FOLDER_NAME)
    # Create folders if they don't exist
    Path(items_folder_path).mkdir(parents=True, exist_ok=True)
    # add a .gitkeep file if it doesn't exist
    open(joinpath(items_folder_path, ".gitkeep"), "a")
    # create csv file if doesn't exist
    if not os.path.exists(csv_file_path):
        with open(csv_file_path, "w") as f:
            f.write('ID')
        # log info
        print(f"No data currently stored for {endpoint}, successfully created folders and file.")
    return (data_path, csv_file_path, items_folder_path)
