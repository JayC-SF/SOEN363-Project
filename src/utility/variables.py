from dotenv import load_dotenv
from os import getenv
from os.path import abspath, join, dirname

load_dotenv("../.env")

# LOAD ENVIRONMENT VARIABLES
SPOTIFY_CLIENT_ID = getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = getenv("SPOTIFY_CLIENT_SECRET")

# DEFINE CONSTANTS
SPOTIFY_API_URL = "https://api.spotify.com/v1"
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_RATE_LIMIT_RESPONSE_CODE = 429
DATA_PATH = abspath(join(dirname(__file__), "../../data"))
TEMP_PATH = abspath(join(dirname(__file__), "../../tmp"))
SPOTIFY_DATA_PATH = f"{DATA_PATH}/spotify"
SPOTIFY_PLAYLISTS_PATH = f"{DATA_PATH}/spotify/spotify_playlists"
SPOTIFY_TRACKS_PATH = f"{DATA_PATH}/spotify/spotify_tracks"
SPOTIFY_PLAYLIST_ENDPOINT = "playlists"
SPOTIFY_TRACK_ENDPOINT = "tracks"
SPOTIFY_ITEMS_CSV_NAME = "ids.csv"
SPOTIFY_ITEMS_FOLDER_NAME = "items"
