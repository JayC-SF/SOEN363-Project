
from spotify.util import setup_spotify_folders
import pandas as pd


def load_tracks_from_playlists():
    _, track_csv, track_items_folder = setup_spotify_folders('tracks')
    _, playlist_csv, playlist_items_folder = setup_spotify_folders('playlists')
    playlist_df = pd.read_csv(playlist_csv)
    track_df = pd.read_csv(track_csv)
