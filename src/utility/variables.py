from dotenv import load_dotenv
import os
from utility.auth_token import AuthToken

load_dotenv("../.env")

# LOAD ENVIRONMENT VARIABLES
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

# DEFINE CONSTANTS
SPOTIFY_API_URL = 'https://api.spotify.com/v1'
SPOTIFY_PLAYLIST_ENDPOINT = 'playlists'
SPOTIFY_AUTH_URL = 'https://accounts.spotify.com/api/token'

DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data"))
TEMP_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../tmp"))
SPOTIFY_AUTH_TOKEN = AuthToken(
    SPOTIFY_AUTH_URL, 
    SPOTIFY_CLIENT_ID, 
    SPOTIFY_CLIENT_SECRET, 
    os.path.abspath(os.path.join(TEMP_PATH, "spotify_auth_token.json"))
    )

SPOTIFY_RATE_LIMIT_RESPONSE_CODE = 429
