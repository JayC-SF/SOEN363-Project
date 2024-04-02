
from pathlib import Path
from spotify.util import setup_spotify_folders
import pandas as pd
import os
from os.path import abspath, join as joinpath, exists
import json

from utility.variables import SPOTIFY_DATA_PATH, SPOTIFY_ITEMS_CSV_NAME


def load_info_from_playlists():
    _, tracks_csv, _, _ = setup_spotify_folders('tracks')
    _, playlists_csv, playlist_items_folder, _ = setup_spotify_folders('playlists')
    _, albums_csv, _, _ = setup_spotify_folders('albums')
    _, artists_csv, _, _ = setup_spotify_folders('artists')
    playlists_df = pd.read_csv(playlists_csv)
    tracks_df = pd.read_csv(tracks_csv)
    tracks_size = len(tracks_df)
    albums_df = pd.read_csv(albums_csv)
    albums_size = len(albums_df)
    artists_df = pd.read_csv(artists_csv)
    artists_size = len(artists_df)
    for _, playlist_row in playlists_df.iterrows():
        playlist_id = playlist_row['ID']
        new_tracks_df, new_albums_df, new_artists_df = load_info_from_playlist(playlist_id, playlist_items_folder)
        # append new dfs in original dataframe set
        tracks_df = pd.concat([tracks_df, new_tracks_df], ignore_index=True)
        albums_df = pd.concat([albums_df, new_albums_df], ignore_index=True)
        artists_df = pd.concat([artists_df, new_artists_df], ignore_index=True)
    # drop duplicates
    tracks_df.drop_duplicates(subset=['ID'], inplace=True)
    albums_df.drop_duplicates(subset=['ID'], inplace=True)
    artists_df.drop_duplicates(subset=['ID'], inplace=True)
    # store to csv file
    tracks_df.to_csv(tracks_csv, index=False)
    albums_df.to_csv(albums_csv, index=False)
    artists_df.to_csv(artists_csv, index=False)
    print(f"Added {len(tracks_df) - tracks_size} new tracks from playlists.")
    print(f"Added {len(albums_df) - albums_size} new albums from playlists.")
    print(f"Added {len(artists_df) - artists_size} new artists from playlists.")


def load_info_from_playlist(playlist_id, playlist_items_folder):
    # check if the playlist has been scraped
    playlist_json_file = os.path.join(playlist_items_folder, f"{playlist_id}.json")
    if not os.path.exists(playlist_json_file):
        print(f"Playlist {playlist_id} needs to be scraped before loading tracks")
        return
    data = {'ID': [], 'CACHED': []}
    tracks_df = pd.DataFrame(data)
    albums_df = tracks_df.copy()
    artists_df = tracks_df.copy()
    # load the json object
    with open(playlist_json_file, "r") as f:
        playlist_json = json.load(f)

    # find all the tracks
    tracks = playlist_json['tracks']['items']
    for track in tracks:
        track = track['track']
        # add new track in the dataframe
        tracks_df.loc[len(tracks_df)] = [track['id'], False]
        albums_df.loc[len(albums_df)] = [track['album']['id'], False]
        # add artists in albums
        for artist in track['album']['artists']:
            artists_df.loc[len(artists_df)] = [artist['id'], False]
        # add artists in track
        for artist in track['artists']:
            artists_df.loc[len(artists_df)] = [artist['id'], False]

    # drop all duplicates in the dataframe
    tracks_df.drop_duplicates(subset=['ID'])
    albums_df.drop_duplicates(subset=['ID'])
    artists_df.drop_duplicates(subset=['ID'])
    return (tracks_df, albums_df, artists_df)


def load_authors_from_audiobooks():
    _, _, items_audiobooks_folder_path, _ = setup_spotify_folders('audiobooks')
    _, _, items_authors_folder_path, _ = setup_spotify_folders('authors')

    if not os.path.exists(items_audiobooks_folder_path):
        print(f"No directory was found at {items_audiobooks_folder_path}")
        return

    files = [f for f in os.listdir(items_audiobooks_folder_path) if
             os.path.isfile(os.path.join(items_audiobooks_folder_path, f)) and f.endswith('.json')]

    author_files = [f for f in os.listdir(items_authors_folder_path) if
                    os.path.isfile(os.path.join(items_authors_folder_path, f)) and f.endswith('.json')]
    authors_size = len(author_files)

    if not files:
        print(f"No data was found at {items_audiobooks_folder_path}")
        return
    for file in files:
        file_path = os.path.join(items_audiobooks_folder_path, file)
        with open(file_path, 'r') as f:
            load_authors_from_single_audiobook(f, file_path, items_authors_folder_path)

    author_files = [f for f in os.listdir(items_authors_folder_path) if
                    os.path.isfile(os.path.join(items_authors_folder_path, f)) and f.endswith('.json')]
    print(f"Added {len(author_files) - authors_size} new audiobooks with authors.")


def load_authors_from_single_audiobook(file, file_path, items_authors_folder_path):
    data = json.load(file)
    if data:
        audiobook_id = data['id']
        authors = data['authors']

        author = {'authors': authors, 'audiobook_id': audiobook_id}
        if os.path.isfile(f'{items_authors_folder_path}/{author['audiobook_id']}.json'):
            return
        with open(f'{items_authors_folder_path}/{author['audiobook_id']}.json', 'w') as f:
            json.dump(author, f, ensure_ascii=False, indent=2)
    else:
        print(f"Warning: Empty JSON file skipped - {file_path}")


def load_chapters_from_audiobooks():
    _, _, items_audiobooks_folder_path, _ = setup_spotify_folders('audiobooks')
    _, _, items_chapters_folder_path, _ = setup_spotify_folders('chapters')

    if not os.path.exists(items_audiobooks_folder_path):
        print(f"No directory was found at {items_audiobooks_folder_path}")
        return

    files = [f for f in os.listdir(items_audiobooks_folder_path) if
             os.path.isfile(os.path.join(items_audiobooks_folder_path, f)) and f.endswith('.json')]

    chapter_files = [f for f in os.listdir(items_chapters_folder_path) if
                     os.path.isfile(os.path.join(items_chapters_folder_path, f)) and f.endswith('.json')]
    chapters_size = len(chapter_files)

    if not files:
        print(f"No data was found at {items_audiobooks_folder_path}")
        return
    for file in files:
        file_path = os.path.join(items_audiobooks_folder_path, file)
        with open(file_path, 'r') as f:
            load_chapters_from_single_audiobook(f, file_path, items_chapters_folder_path)

    chapter_files = [f for f in os.listdir(items_chapters_folder_path) if
                     os.path.isfile(os.path.join(items_chapters_folder_path, f)) and f.endswith('.json')]
    print(f"Added {len(chapter_files) - chapters_size} new chapters.")


def load_chapters_from_single_audiobook(file, file_path, items_chapters_folder_path):
    data = json.load(file)
    if data:
        chapter_items = data['chapters']['items']
        audiobook = data.copy()
        del audiobook['chapters']

        for chapter in chapter_items:
            chapter['audiobook'] = audiobook
            if os.path.isfile(f'{items_chapters_folder_path}/{chapter['id']}.json'):
                return
            with open(f'{items_chapters_folder_path}/{chapter['id']}.json', 'w') as f:
                json.dump(chapter, f, ensure_ascii=False, indent=2)
    else:
        print(f"Warning: Empty JSON file skipped - {file_path}")


def load_genres():
    endpoint = 'genres'
    data_path = abspath(joinpath(SPOTIFY_DATA_PATH, endpoint))
    csv_genres_path = abspath(joinpath(data_path, 'genres.csv'))

    # create data folder if they don't exist
    Path(data_path).mkdir(parents=True, exist_ok=True)
    if not exists(csv_genres_path):
        with open(csv_genres_path, "w") as f:
            f.write('GENRES')
        # log info
        print(f"No data currently stored for {endpoint}, successfully created folders and csv file.")

    # get paths for artists and albums
    _, artists_csv, artists_items_folder, _ = setup_spotify_folders('artists')
    _, albums_csv, albums_items_folder, _ = setup_spotify_folders('albums')
    artists_df = pd.read_csv(artists_csv)
    albums_df = pd.read_csv(albums_csv)
    genres_df = pd.read_csv(csv_genres_path)
    genres_count = len(genres_df)

    # keep only the ones that are cached
    artists_df = artists_df[artists_df['CACHED']]
    albums_df = albums_df[albums_df['CACHED']]

    for _, row in artists_df.iterrows():
        artist_id = row['ID']
        artist_json_file = os.path.join(artists_items_folder, f"{artist_id}.json")
        with open(artist_json_file, "r") as f:
            artist_json = json.load(f)
        # combine the genres from artists
        for g in artist_json['genres']:
            genres_df.loc[len(genres_df)] = [g]

    for _, row in albums_df.iterrows():
        album_id = row['ID']
        album_json_file = os.path.join(albums_items_folder, f"{album_id}.json")
        with open(album_json_file, "r") as f:
            album_json = json.load(f)
        # combine the genres from album
        for g in album_json['genres']:
            genres_df.loc[len(genres_df)] = [g]

    genres_df.drop_duplicates(subset=['GENRES'], inplace=True)
    genres_df.to_csv(csv_genres_path, index=False)
    print(f"Total number of genres added: {len(genres_df)-genres_count}")
