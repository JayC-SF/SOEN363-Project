-- Active: 1712015075548@@walidoow.com@3306@project
-- Drop existing tables if they exist

DROP TABLE IF EXISTS Audiobooks_Chapters;
DROP TABLE IF EXISTS Audiobooks_Authors;
DROP TABLE IF EXISTS Available_Markets_Albums;
DROP TABLE IF EXISTS Available_Markets_Tracks;
DROP TABLE IF EXISTS Albums_Genres;
DROP TABLE IF EXISTS Audiobook;
DROP TABLE IF EXISTS Tracks_Artists;
DROP TABLE IF EXISTS Artists_Aliases;

DROP TABLE IF EXISTS Alias;
DROP TABLE IF EXISTS Artist;

DROP TABLE IF EXISTS Track;
DROP TABLE IF EXISTS Audio;
DROP TABLE IF EXISTS Playlist;
DROP TABLE IF EXISTS Album;
DROP TABLE IF EXISTS Market;
DROP TABLE IF EXISTS Chapter;
DROP TABLE IF EXISTS Author;
DROP TABLE IF EXISTS Genre;
DROP TABLE IF EXISTS Chapters;

-- CREATE ALL TABLES

CREATE TABLE Audio (
    audio_id INT AUTO_INCREMENT,
    audio_name VARCHAR(100) NOT NULL,
    spotify_url VARCHAR(200),
    href VARCHAR(200),
    explicit BIT,
    PRIMARY KEY (audio_id)
);

CREATE TABLE Track(
    track_id INT AUTO_INCREMENT,
    popularity INT,
    type VARCHAR(100),
    duration_ms INT,
    external_url VARCHAR(200),
    is_playable BIT,
    preview_url VARCHAR(200),
    disc_number INT,
    PRIMARY KEY (track_id),
    FOREIGN KEY (track_id) REFERENCES Audio(audio_id) ON DELETE CASCADE
);

CREATE TABLE Audiobook (
    audiobook_id INT AUTO_INCREMENT,
    description TEXT,
    edition VARCHAR(200),
    publisher VARCHAR(200),
    total_chapters INT,
    media_type VARCHAR(200),
    PRIMARY KEY (audiobook_id),
    FOREIGN KEY (audiobook_id) REFERENCES Audio(audio_id) ON DELETE CASCADE
);

CREATE TABLE Artist(
    artist_id INT AUTO_INCREMENT,
    artist_name VARCHAR(200) NOT NULL,
    nb_followers INT,
    popularity INT,
    spotify_url VARCHAR(200),
    href VARCHAR(200),
    PRIMARY KEY (artist_id)
);

CREATE TABLE Playlist(
    playlist_id INT AUTO_INCREMENT,
    playlist_name VARCHAR(200) NOT NULL,
    description TEXT,
    nb_followers INT,
    collaborative BIT,
    snapshot_id INT,
    spotify_url VARCHAR(200),
    href VARCHAR(200),
    external_url VARCHAR(200),
    PRIMARY KEY (playlist_id)
);

CREATE TABLE Alias(
    alias_id INT AUTO_INCREMENT,
    alias_name VARCHAR(200) NOT NULL,
    PRIMARY KEY (alias_id)
);

CREATE TABLE Album(
    album_id INT AUTO_INCREMENT,
    album_name VARCHAR(200) NOT NULL,
    total_tracks INT,
    popularity INT,
    release_date DATETIME,
    label VARCHAR(200),
    external_urls VARCHAR(200),
    href VARCHAR(200),
    type VARCHAR(200),
    PRIMARY KEY (album_id)
);

CREATE TABLE Genre (
    genre_id INT AUTO_INCREMENT,
    genre_name VARCHAR(200) NOT NULL,
    PRIMARY KEY (genre_id)
);

CREATE TABLE Market (
    market_id INT AUTO_INCREMENT,
    country_code VARCHAR(200) NOT NULL,
    PRIMARY KEY (market_id)
);

CREATE TABLE Author(
    author_id INT AUTO_INCREMENT,
    author_name VARCHAR(200),
    PRIMARY KEY (author_id)
);

CREATE TABLE Chapter(
    chapter_id INT AUTO_INCREMENT,
    chapter_number INT,
    description TEXT,
    chapter_name VARCHAR(200),
    PRIMARY KEY (chapter_id)
);

CREATE TABLE Tracks_Artists(
    track_id INT NOT NULL,
    artist_id INT NOT NULL,
    PRIMARY KEY (track_id, artist_id),
    FOREIGN KEY (track_id) REFERENCES Track(track_id) ON DELETE CASCADE,
    FOREIGN KEY (artist_id) REFERENCES Artist(artist_id) ON DELETE CASCADE
);

CREATE TABLE Artists_Aliases(
    artist_id INT NOT NULL,
    alias_id INT NOT NULL,
    PRIMARY KEY (artist_id, alias_id),
    FOREIGN KEY (artist_id) REFERENCES Artist(artist_id) ON DELETE CASCADE,
    FOREIGN KEY (alias_id) REFERENCES Alias(alias_id) ON DELETE CASCADE
);

CREATE TABLE Tracks_Albums(
    track_id INT NOT NULL,
    album_id INT NOT NULL,
    PRIMARY KEY (track_id, album_id),
    FOREIGN KEY (track_id) REFERENCES Track(track_id) ON DELETE CASCADE,
    FOREIGN KEY (album_id) REFERENCES Album(album_id) ON DELETE CASCADE
);

CREATE TABLE Albums_Genres(
    album_id INT NOT NULL,
    genre_id INT NOT NULL,
    PRIMARY KEY (album_id, genre_id),
    FOREIGN KEY (album_id) REFERENCES Album(album_id) ON DELETE CASCADE,
    FOREIGN KEY (genre_id) REFERENCES Genre(genre_id) ON DELETE CASCADE
);

CREATE TABLE Available_Markets_Albums(
    album_id INT NOT NULL,
    market_id INT NOT NULL,
    PRIMARY KEY (album_id, market_id),
    FOREIGN KEY (album_id) REFERENCES Album(album_id) ON DELETE CASCADE,
    FOREIGN KEY (market_id) REFERENCES Market(market_id) ON DELETE CASCADE
);

CREATE TABLE Available_Markets_Tracks(
    track_id INT NOT NULL,
    market_id INT NOT NULL,
    PRIMARY KEY (track_id, market_id),
    FOREIGN KEY (track_id) REFERENCES Track(track_id) ON DELETE CASCADE,
    FOREIGN KEY (market_id) REFERENCES Market(market_id) ON DELETE CASCADE
);

CREATE TABLE Playlists_Tracks(
    track_id INT NOT NULL,
    playlist_id INT NOT NULL,
    PRIMARY KEY (track_id, playlist_id),
    FOREIGN KEY (track_id) REFERENCES Track(track_id) ON DELETE CASCADE,
    FOREIGN KEY (playlist_id) REFERENCES Playlist(playlist_id) ON DELETE CASCADE
);

CREATE TABLE Audiobooks_Authors (
    author_id INT NOT NULL,
    audiobook_id INT NOT NULL,
    PRIMARY KEY (author_id, audiobook_id),
    FOREIGN KEY (author_id) REFERENCES Author(author_id) ON DELETE CASCADE,
    FOREIGN KEY (audiobook_id) REFERENCES Audiobook(audiobook_id) ON DELETE CASCADE 
);

CREATE TABLE Audiobooks_Chapters (
    chapter_id INT AUTO_INCREMENT,
    audiobook_id INT NOT NULL,
    PRIMARY KEY (chapter_id),
    FOREIGN KEY (audiobook_id) REFERENCES Audiobook(audiobook_id) ON DELETE CASCADE 
);