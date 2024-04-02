from dotenv import load_dotenv
from os import getenv
from os.path import abspath, join, dirname

load_dotenv(".env")

# LOAD ENVIRONMENT VARIABLES
SPOTIFY_CLIENT_ID = getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = getenv("SPOTIFY_CLIENT_SECRET")

# DEFINE PROGRAM CONSTANTS
DATA_PATH = abspath(join(dirname(__file__), "../../data"))
TEMP_PATH = abspath(join(dirname(__file__), "../../tmp"))

# DEFINE SPOTIFY CONSTANTS
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_RATE_LIMIT_RESPONSE_CODE = 429
SPOTIFY_BATCH_MAX_ITEMS = 20
SPOTIFY_ITEMS_CSV_NAME = "ids.csv"
SPOTIFY_ITEMS_FOLDER_NAME = "items"
SPOTIFY_MAPPING_FILE_NAME = "mapping.json"
SPOTIFY_API_URL = "https://api.spotify.com/v1"
SPOTIFY_DATA_PATH = abspath(join(DATA_PATH, 'spotify'))

# DEFINE MUSICBRAINZ CONSTANTS
MUSICBRAINZ_DATA_PATH = abspath(join(DATA_PATH, 'musicbrainz'))
MUSICBRAINZ_ITEMS_CSV_NAME = "alias_ids.csv"
MUSICBRAINZ_ITEMS_FOLDER_NAME = "items"
MUSICBRAINZ_API_URL = "https://musicbrainz.org/ws/2/release"
