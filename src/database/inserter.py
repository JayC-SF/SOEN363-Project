import time
from typing import List
from os.path import abspath, join as joinpath

import mysql.connector
import pandas as pd

from spotify.models.album_model import AlbumModel
from spotify.models.artist_model import ArtistModel
from spotify.parser import SpotifyParser
from utility.variables import DATABASE_HOST, DATABASE_USER, DATABASE_PASSWORD, DATABASE_NAME, SPOTIFY_DATA_PATH


class DatabaseInserter:
    def __init__(self, data_type: str):
        self.__data_type = data_type
        self.__db = mysql.connector.connect(
            host=DATABASE_HOST,
            user=DATABASE_USER,
            password=DATABASE_PASSWORD,
            database=DATABASE_NAME
        )

    def insert_data(self):
        match self.__data_type:
            case 'genres':
                self.__insert_genres()
            case 'albums':
                self.__insert_albums()
            case 'artists':
                self.__insert_artists()
            case _:
                print(f"Error: The function to insert data for {self.__data_type} has not been implemented yet.")

    def __insert_genres(self):
        cursor = self.__db.cursor()
        data_path = abspath(joinpath(SPOTIFY_DATA_PATH, 'genres'))
        csv_genres_path = abspath(joinpath(data_path, 'genres.csv'))
        df = pd.read_csv(csv_genres_path)

        start_time = time.time()
        num_genres = 0

        for _, row in df.iterrows():
            genre_name = row['GENRES']
            check_query = "SELECT EXISTS(SELECT 1 FROM Genre WHERE genre_name = %s)"
            cursor.execute(check_query, (genre_name,))
            exists = cursor.fetchone()[0]
            if not exists:
                insert_query = """
                            INSERT INTO Genre (genre_name)
                            VALUES (%s)
                            """
                cursor.execute(insert_query, (genre_name,))
                self.__db.commit()
                print(f"Inserted genre data for {genre_name}")
                num_genres += 1
            else:
                print(f"Row already exists for {genre_name}, skipping.")

        end_time = time.time()
        print(f"Successfully inserted {num_genres} albums in {end_time - start_time} seconds")

    def __insert_albums(self):
        parser = SpotifyParser('albums', AlbumModel)
        albums: List[AlbumModel] = parser.parse_all()
        cursor = self.__db.cursor()

        start_time = time.time()
        num_albums = 0

        for album in albums:
            check_query = "SELECT EXISTS(SELECT 1 FROM Album WHERE spotify_id = %s)"
            cursor.execute(check_query, (album.spotify_id,))
            exists = cursor.fetchone()[0]
            if not exists:
                # If the album does not exist, insert it
                insert_query = """
                            INSERT INTO Album (album_name, spotify_id, total_tracks, popularity, release_date, label, external_url, href, type)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                            """
                album_data = (
                    album.album_name, album.spotify_id, album.total_tracks, album.popularity, album.release_date,
                    album.label, album.external_url, album.href, album.type
                )
                cursor.execute(insert_query, album_data)
                self.__db.commit()
                print(f"Inserted album data for {album.spotify_id}")
                num_albums += 1
            else:
                print(f"Row already exists for {album.spotify_id, album.album_name}, skipping.")

        end_time = time.time()
        print(f"Successfully inserted {num_albums} albums in {end_time - start_time} seconds")

    def __insert_artists(self):
        parser = SpotifyParser('artists', ArtistModel)
        artists: List[ArtistModel] = parser.parse_all()
        cursor = self.__db.cursor()

        start_time = time.time()
        num_artists = 0

        for artist in artists:
            check_query = "SELECT EXISTS(SELECT 1 FROM Artist WHERE spotify_id = %s)"
            cursor.execute(check_query, (artist.spotify_id,))
            exists = cursor.fetchone()[0]
            if not exists:
                insert_query = """
                            INSERT INTO Artist (spotify_id, artist_name, nb_followers, popularity, external_url, href, uri)
                            VALUES (%s, %s, %s, %s, %s, %s, %s)
                            """
                artist_data = (
                    artist.spotify_id, artist.artist_name, artist.nb_followers, artist.popularity, artist.external_url,
                    artist.href, artist.uri
                )
                cursor.execute(insert_query, artist_data)
                self.__db.commit()
                print(f"Inserted artist data for {artist.spotify_id}")
                num_artists += 1
            else:
                print(f"Row already exists for {artist.spotify_id, artist.artist_name}, skipping.")

        end_time = time.time()
        print(f"Successfully inserted {num_artists} artists in {end_time - start_time} seconds")
