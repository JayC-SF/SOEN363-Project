import threading
import time
from queue import Queue
from typing import List
from os.path import abspath, join as joinpath

import mysql.connector
import pandas as pd

from spotify.models.album_model import AlbumModel
from spotify.models.artist_model import ArtistModel
from spotify.models.audiobook_model import AudiobookModel
from spotify.models.chapter_model import ChapterModel
from spotify.models.playlist_model import PlaylistModel
from spotify.models.track_model import TrackModel
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
            case 'artists_genres':
                self.__insert_artists_genres()
            case 'chapters':
                self.__insert_chapters_genres()
            case 'playlists':
                self.__insert_playlists()
            case 'tracks':
                self.__insert_tracks()
            case 'audiobooks':
                self.__insert_audiobooks()
            case 'authors':
                pass
            case 'aliases':
                pass
            case 'tracks_artists':
                self.__insert_tracks_artists()
                pass
            case 'artists_aliases':
                pass
            case 'tracks_albums':
                pass
            case 'artists_genres':
                pass
            case 'available_markets_albums':
                pass
            case 'available_markets_tracks':
                pass
            case 'playlists_tracks':
                pass
            case 'audiobooks_authors':
                pass
            case 'audiobooks_chapters':
                pass
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

    def __insert_artists_genres(self):
        parser = SpotifyParser('artists', ArtistModel)
        artists: List[ArtistModel] = parser.parse_all(
            middleware=lambda mapped_object, json_data: (
                    setattr(mapped_object, 'genres', json_data.get('genres')) or mapped_object
            )
        )
        cursor = self.__db.cursor()
        start_time = time.time()
        num_inserts = 0

        for artist in artists:
            cursor.execute("SELECT artist_id FROM Artist WHERE spotify_id = %s", (artist.spotify_id,))
            artist_result = cursor.fetchone()
            if artist_result:
                artist_id = artist_result[0]
            else:
                continue

            for genre_name in artist.genres:
                cursor.execute("SELECT genre_id FROM Genre WHERE genre_name = %s", (genre_name,))
                genre_result = cursor.fetchone()
                if genre_result:
                    genre_id = genre_result[0]
                else:
                    continue

                check_query = "SELECT COUNT(1) FROM Artists_Genres WHERE artist_id = %s AND genre_id = %s"
                cursor.execute(check_query, (artist_id, genre_id))
                if cursor.fetchone()[0] == 0:
                    cursor.execute(
                        "INSERT INTO Artists_Genres (artist_id, genre_id) VALUES (%s, %s)",
                        (artist_id, genre_id)
                    )
                    self.__db.commit()
                    num_inserts += 1
                    print(f"Inserted artist and genre data for artist_id: {artist.spotify_id}, genre_id: {genre_id}")
                else:
                    print(f"Row already exists for artist_id: {artist.spotify_id}, genre_id: {genre_id}, skipping.")

        end_time = time.time()
        print(f"Successfully inserted {num_inserts} artists and genres in {end_time - start_time} seconds")

    def __insert_chapters_genres(self):
        parser = SpotifyParser('chapters', ChapterModel)
        chapters: List[ChapterModel] = parser.parse_all()
        queue = Queue()

        for chapter in chapters:
            queue.put(chapter)

        def worker():
            db = mysql.connector.connect(
                host=DATABASE_HOST,
                user=DATABASE_USER,
                password=DATABASE_PASSWORD,
                database=DATABASE_NAME
            )
            cursor = db.cursor()

            while not queue.empty():
                chapter = queue.get()
                try:
                    check_query = "SELECT EXISTS(SELECT 1 FROM Chapter WHERE spotify_id = %s)"
                    cursor.execute(check_query, (chapter.spotify_id,))
                    exists = cursor.fetchone()[0]
                    if not exists:
                        insert_query = """
                                       INSERT INTO Chapter (spotify_id, chapter_name, audio_preview_url, chapter_number, duration_ms, explicit, external_url, href, type, uri, release_date)
                                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                                       """
                        chapter_data = (
                            chapter.spotify_id, chapter.chapter_name, chapter.audio_preview_url, chapter.chapter_number,
                            chapter.description, chapter.html_description, chapter.duration_ms, chapter.explicit,
                            chapter.external_url, chapter.href, chapter.type, chapter.uri, chapter.release_date
                        )
                        cursor.execute(insert_query, chapter_data)
                        db.commit()
                        # print(f"Inserted chapter data for {chapter.spotify_id}")
                    # else:
                    # print(f"Row already exists for {chapter.spotify_id}, skipping.")
                finally:
                    queue.task_done()

        start_time = time.time()

        # Start a pool of worker threads
        threads = []
        for i in range(5):  # Number of threads
            thread = threading.Thread(target=worker)
            thread.start()
            threads.append(thread)

        # Wait for all tasks in the queue to be processed
        queue.join()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        count_query = "SELECT COUNT(*) FROM Chapter"
        cursor = self.__db.cursor()
        cursor.execute(count_query)
        row_count = cursor.fetchone()[0]

        end_time = time.time()
        print(f"Finished inserting chapters. Total chapters in database: {row_count}")
        print(f"Finished inserting chapters in {end_time - start_time} seconds")

    def __insert_playlists(self):
        parser = SpotifyParser('playlists', PlaylistModel)
        playlists: List[PlaylistModel] = parser.parse_all()
        queue = Queue()

        for playlist in playlists:
            queue.put(playlist)

        def worker():
            db = mysql.connector.connect(
                host=DATABASE_HOST,
                user=DATABASE_USER,
                password=DATABASE_PASSWORD,
                database=DATABASE_NAME
            )
            cursor = db.cursor()

            while not queue.empty():
                playlist: PlaylistModel = queue.get()
                try:
                    check_query = "SELECT EXISTS(SELECT 1 FROM Playlist WHERE spotify_id = %s)"
                    cursor.execute(check_query, (playlist.spotify_id,))
                    exists = cursor.fetchone()[0]
                    if not exists:
                        insert_query = """
                                          INSERT INTO Playlist (spotify_id, playlist_name, description, nb_followers, collaborative, snapshot_id, href, external_url, uri)
                                          VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                                       """
                        playlist_data = (
                            playlist.spotify_id, playlist.playlist_name, playlist.description, playlist.nb_followers,
                            playlist.collaborative, playlist.snapshot_id, playlist.href, playlist.external_url,
                            playlist.uri
                        )
                        cursor.execute(insert_query, playlist_data)
                        db.commit()
                finally:
                    queue.task_done()

        start_time = time.time()

        threads = []
        for i in range(5):
            thread = threading.Thread(target=worker)
            thread.start()
            threads.append(thread)

        queue.join()

        for thread in threads:
            thread.join()

        count_query = "SELECT COUNT(*) FROM Playlist"
        cursor = self.__db.cursor()
        cursor.execute(count_query)
        row_count = cursor.fetchone()[0]

        end_time = time.time()
        print(f"Finished inserting playlists. Total playlists in database: {row_count}")
        print(f"Finished inserting playlists in {end_time - start_time} seconds")

    def __insert_tracks(self):
        parser = SpotifyParser('tracks', TrackModel)
        tracks: List[TrackModel] = parser.parse_all()
        queue = Queue()

        for track in tracks:
            queue.put(track)

        def worker():
            db = mysql.connector.connect(
                host=DATABASE_HOST,
                user=DATABASE_USER,
                password=DATABASE_PASSWORD,
                database=DATABASE_NAME
            )
            cursor = db.cursor()

            while not queue.empty():
                track: TrackModel = queue.get()
                try:
                    check_query = "SELECT EXISTS(SELECT 1 FROM Audio WHERE spotify_id = %s)"
                    cursor.execute(check_query, (track.spotify_id,))
                    exists = cursor.fetchone()[0]
                    if not exists:
                        insert_query = """
                                        INSERT INTO Audio (spotify_id, audio_name, uri, href, external_url, explicit)
                                        VALUES (%s, %s, %s, %s, %s, %s)
                                               """
                        track_data = (
                            track.spotify_id, track.audio_name, track.uri, track.href, track.external_url,
                            track.explicit
                        )
                        cursor.execute(insert_query, track_data)
                        db.commit()

                        audio_id = cursor.lastrowid

                        insert_query = """
                                       INSERT INTO Track (track_id, popularity, type, duration_ms, preview_url, disc_number)
                                       VALUES (%s, %s, %s, %s, %s, %s)
                                               """
                        track_data = (
                            audio_id, track.popularity, track.type, track.duration_ms, track.preview_url,
                            track.disc_number
                        )
                        cursor.execute(insert_query, track_data)
                        db.commit()
                    #     print(f"Inserted track data for {track.spotify_id}")
                    # else:
                    #     print(f"Row already exists for {track.spotify_id}, skipping.")
                finally:
                    queue.task_done()

        start_time = time.time()

        threads = []
        for i in range(5):
            thread = threading.Thread(target=worker)
            thread.start()
            threads.append(thread)

        queue.join()

        for thread in threads:
            thread.join()

        count_query = "SELECT COUNT(*) FROM Track"
        cursor = self.__db.cursor()
        cursor.execute(count_query)
        row_count = cursor.fetchone()[0]

        end_time = time.time()
        print(f"Finished inserting tracks. Total tracks in database: {row_count}")
        print(f"Finished inserting tracks in {end_time - start_time} seconds")

    def __insert_audiobooks(self):
        parser = SpotifyParser('audiobooks', AudiobookModel)
        audiobooks: List[AudiobookModel] = parser.parse_all()
        queue = Queue()

        for audiobook in audiobooks:
            queue.put(audiobook)

        def worker():
            db = mysql.connector.connect(
                host=DATABASE_HOST,
                user=DATABASE_USER,
                password=DATABASE_PASSWORD,
                database=DATABASE_NAME
            )
            cursor = db.cursor()

            while not queue.empty():
                audiobook: AudiobookModel = queue.get()
                try:
                    check_query = "SELECT EXISTS(SELECT 1 FROM Audio WHERE spotify_id = %s)"
                    cursor.execute(check_query, (audiobook.spotify_id,))
                    exists = cursor.fetchone()[0]
                    if not exists:
                        insert_query = """
                                          INSERT INTO Audio (spotify_id, audio_name, uri, href, external_url, explicit)
                                          VALUES (%s, %s, %s, %s, %s, %s)
                                        """
                        audiobook_data = (
                            audiobook.spotify_id, audiobook.audio_name, audiobook.uri, audiobook.href,
                            audiobook.external_url, audiobook.explicit
                        )
                        cursor.execute(insert_query, audiobook_data)
                        db.commit()

                        audio_id = cursor.lastrowid

                        insert_query = """
                                          INSERT INTO Audiobook (audiobook_id, description, edition, publisher, total_chapters, media_type)
                                          VALUES (%s, %s, %s, %s, %s, %s)
                                        """
                        audiobook_data = (
                            audio_id, audiobook.description, audiobook.edition, audiobook.publisher,
                            audiobook.total_chapters, audiobook.media_type
                        )
                        cursor.execute(insert_query, audiobook_data)
                        db.commit()
                    #     print(f"Inserted audiobook data for {audiobook.spotify_id}")
                    # else:
                    #     print(f"Row already exists for {audiobook.spotify_id}, skipping.")
                finally:
                    queue.task_done()

        start_time = time.time()

        threads = []
        for i in range(5):
            thread = threading.Thread(target=worker)
            thread.start()
            threads.append(thread)

        queue.join()

        for thread in threads:
            thread.join()

        count_query = "SELECT COUNT(*) FROM Audiobook"
        cursor = self.__db.cursor()
        cursor.execute(count_query)
        row_count = cursor.fetchone()[0]

        end_time = time.time()
        print(f"Finished inserting audiobooks. Total audiobooks in database: {row_count}")
        print(f"Finished inserting audiobooks in {end_time - start_time} seconds")

    def __insert_tracks_artists(self):
        parser = SpotifyParser('tracks', TrackModel)
        tracks: List[TrackModel] = parser.parse_all(
            middleware=lambda mapped_object, json_data: (
                    setattr(mapped_object, 'artists', json_data.get('artists')) or mapped_object
            )
        )

        # Use buffered cursor to avoid "Unread result found" error
        cursor = self.__db.cursor(buffered=True)
        start_time = time.time()
        num_inserts = 0

        for track in tracks:
            cursor.execute("SELECT audio_id FROM Audio WHERE spotify_id = %s", (track.spotify_id,))
            result = cursor.fetchone()
            if result:
                track_id = result[0]
                # Verify the track_id in Track table
                cursor.execute("SELECT EXISTS(SELECT 1 FROM Track WHERE track_id = %s)", (track_id,))
                exists = cursor.fetchone()[0]
                if not exists:
                    continue
            else:
                continue

            for artist in track.artists:
                cursor.execute("SELECT artist_id FROM Artist WHERE artist_name = %s", (artist['name'],))
                result = cursor.fetchone()
                if result:
                    artist_id = result[0]
                else:
                    continue

                cursor.execute("SELECT COUNT(1) FROM Tracks_Artists WHERE track_id = %s AND artist_id = %s",
                               (track_id, artist_id))
                if cursor.fetchone()[0] == 0:
                    cursor.execute("INSERT INTO Tracks_Artists (track_id, artist_id) VALUES (%s, %s)",
                                   (track_id, artist_id))
                    self.__db.commit()
                    num_inserts += 1

        end_time = time.time()
        print(f"Successfully inserted {num_inserts} track-artist relationships in {end_time - start_time} seconds")
