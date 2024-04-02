from spotify.util import setup_spotify_folders
import pandas as pd
import os
import json


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
            load_authors_from_audiobook(f, file_path, items_authors_folder_path)

    author_files = [f for f in os.listdir(items_authors_folder_path) if
                    os.path.isfile(os.path.join(items_authors_folder_path, f)) and f.endswith('.json')]
    print(f"Added {len(author_files) - authors_size} new audiobooks with authors.")


def load_authors_from_audiobook(file, file_path, items_authors_folder_path):
    data = json.load(file)
    if data:
        audiobook_id = data['id']
        authors = data['authors']

        author = {'authors': authors, 'audiobook_id': audiobook_id}
        write_authors_per_audiobook(author, items_authors_folder_path)
    else:
        print(f"Warning: Empty JSON file skipped - {file_path}")


def write_authors_per_audiobook(author, items_authors_folder_path):
    if os.path.isfile(f'{items_authors_folder_path}/{author['audiobook_id']}.json'):
        return
    with open(f'{items_authors_folder_path}/{author['audiobook_id']}.json', 'w') as f:
        json.dump(author, f, ensure_ascii=False, indent=2)
