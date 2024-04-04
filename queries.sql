-- Active: 1712072836115@@walidoow.com@3306@project

-- Query Implementation
-- You need to provide demonstrate the following query types:

-- 1. Basic select with simple where clause.
SELECT * FROM Track
WHERE duration_ms > 300000;

-- 2. Basic select with simple group by clause (with and without having clause).

-- Retrieve the total number of tracks for each album
SELECT album_id, COUNT(track_id) AS total_tracks
FROM Tracks_Albums
GROUP BY album_id;

-- Retrieve albums that have more than 10 tracks
SELECT album_id, COUNT(track_id) AS total_tracks
FROM Tracks_Albums
GROUP BY album_id
HAVING COUNT(track_id) > 10;


-- 3. A simple join select query using cartesian product and where clause vs. a join query using on.

-- Cartesian product with WHERE clause
SELECT * FROM Track, Album
WHERE Track.album_id = Album.album_id;

-- Join query using ON keyword
SELECT *
FROM Track
JOIN Album ON Track.album_id = Album.album_id;

-- 4. A few queries to demonstrate various join types on the same tables: inner vs. outer (left and right) vs. full join. Use of null values in the database to show the differences is required.
SELECT * FROM Tracks_Albums AS TA
LEFT JOIN Album AS A ON TA.album_id = A.album_id;

SELECT * FROM Tracks_Albums AS TA
RIGHT JOIN Album AS A ON TA.album_id = A.album_id;

SELECT * FROM Tracks_Albums AS TA
LEFT JOIN Album AS A ON TA.album_id = A.album_id
UNION
SELECT * FROM Tracks_Albums AS TA
RIGHT JOIN Album AS A ON TA.album_id = A.album_id
WHERE TA.album_id IS NULL;

-- 5. A couple of examples to demonstrate correlated queries.

-- Correlated Subquery to Find Artists with More Than a Certain Number of Tracks:
SELECT artist_name FROM Artist a
WHERE (
    SELECT COUNT(*) FROM Tracks_Artists ta
    JOIN Track t ON ta.track_id = t.track_id
    WHERE ta.artist_id = a.artist_id
) > 5;

-- Correlated Subquery to Find Albums with Less Than the Average Popularity of Their Artists:
SELECT album_name FROM Album al
WHERE (
    SELECT AVG(popularity) FROM Artist ar
    INNER JOIN Tracks_Albums ta ON ar.artist_id = ta.artist_id
    INNER JOIN Track tr ON ta.track_id = tr.track_id
    WHERE ta.album_id = al.album_id
) < (
    SELECT AVG(popularity) FROM Artist
);

-- 6. One example per set operations: intersect, union, and difference vs. their equivalences without using set operations.

-- Using Set Operation (Intersect)
SELECT artist_name FROM Artist
INTERSECT
SELECT artist_name FROM Tracks_Artists ta
INNER JOIN Artist a ON ta.artist_id = a.artist_id
INNER JOIN Track t ON ta.track_id = t.track_id
INNER JOIN Tracks_Albums tra ON t.track_id = tra.track_id
INNER JOIN Album al ON tra.album_id = al.album_id
WHERE al.album_name = 'Album Name';

-- Equivalent without Set Operation
SELECT DISTINCT a.artist_name
FROM Artist a
INNER JOIN Tracks_Artists ta ON a.artist_id = ta.artist_id
INNER JOIN Track t ON ta.track_id = t.track_id
INNER JOIN Tracks_Albums tra ON t.track_id = tra.track_id
INNER JOIN Album al ON tra.album_id = al.album_id
WHERE al.album_name = 'Album Name'
AND EXISTS (
    SELECT 1 FROM Artist a2
    INNER JOIN Tracks_Artists ta2 ON a2.artist_id = ta2.artist_id
    INNER JOIN Track t2 ON ta2.track_id = t2.track_id
    INNER JOIN Tracks_Albums tra2 ON t2.track_id = tra2.track_id
    INNER JOIN Album al2 ON tra2.album_id = al2.album_id
    WHERE al2.album_name = 'Another Album Name'
    AND a.artist_id = a2.artist_id
);

-- Using Set Operation (Union)
SELECT artist_name FROM Artist
WHERE nb_followers > 1000
UNION SELECT artist_name FROM Artist
WHERE popularity > 70;

-- Equivalent without Set Operation
SELECT artist_name FROM Artist
WHERE nb_followers > 1000 OR popularity > 70;

-- Using Set Operation (Difference)
SELECT artist_name FROM Artist
EXCEPT
SELECT artist_name FROM Tracks_Artists ta
INNER JOIN Artist a ON ta.artist_id = a.artist_id
INNER JOIN Track t ON ta.track_id = t.track_id
INNER JOIN Tracks_Albums tra ON t.track_id = tra.track_id
INNER JOIN Album al ON tra.album_id = al.album_id
WHERE al.album_name = 'Album Name';

-- Equivalent without Set Operation
SELECT DISTINCT a.artist_name FROM Artist a
LEFT JOIN Tracks_Artists ta ON a.artist_id = ta.artist_id
LEFT JOIN Track t ON ta.track_id = t.track_id
LEFT JOIN Tracks_Albums tra ON t.track_id = tra.track_id
LEFT JOIN Album al ON tra.album_id = al.album_id
WHERE al.album_name != 'Album Name'
OR al.album_name IS NULL;


-- 7. An example of a view that has a hard-coded criteria, by which the content of the view may change upon changing the hard-coded value (see L09 slide 24).
-- Create a view to display detailed information about popular tracks by genre
CREATE VIEW PopularTracksByGenre AS
SELECT
    t.track_id,
    t.popularity,
    t.type AS track_type,
    t.duration_ms,
    t.preview_url,
    t.disc_number,
    a.artist_id,
    a.artist_name,
    al.album_id,
    al.album_name,
    g.genre_id,
    g.genre_name
FROM Track t
INNER JOIN Tracks_Artists ta ON t.track_id = ta.track_id
INNER JOIN Artist a ON ta.artist_id = a.artist_id
INNER JOIN Tracks_Albums tal ON t.track_id = tal.track_id
INNER JOIN Album al ON tal.album_id = al.album_id
INNER JOIN Artists_Genres ag ON a.artist_id = ag.artist_id
INNER JOIN Genre g ON ag.genre_id = g.genre_id
WHERE t.popularity > 80
ORDER BY t.popularity DESC;

-- 8. Two implementations of the division operator using a) a regular nested query using NOT IN and b) a correlated nested query using NOT EXISTS and EXCEPT.
-- Using a regular nested query with NOT IN
SELECT DISTINCT A.audiobook_id FROM Audiobook A
WHERE A.audiobook_id NOT IN (
    SELECT AC.audiobook_id FROM Audiobooks_Chapters AC
    WHERE AC.audiobook_id = A.audiobook_id
    EXCEPT
    SELECT T.track_id FROM Track T
);

-- Using a correlated nested query with NOT EXISTS and EXCEPT
SELECT DISTINCT A.audiobook_id FROM Audiobook A
WHERE NOT EXISTS (
    SELECT * FROM Audiobooks_Chapters AC
    WHERE AC.audiobook_id = A.audiobook_id
    EXCEPT
    SELECT T.track_id FROM Track T
);


-- 9. Provide queries that demonstrates the overlap and covering constraints.

-- Inserting overlapping data into Audiobook and Playlist tables
-- Both tables have a common attribute 'description'

-- Overlap Constraint: Inserting into Audiobook
INSERT INTO Audiobook (audiobook_id, description, edition, publisher, total_chapters, media_type)
VALUES (1, 'Overlap', 'Edition1', 'Publisher1', 10, 'AudioBook');

-- Inserting into Playlist with same description
INSERT INTO Playlist (playlist_id, spotify_id, playlist_name, description, nb_followers, collaborative, snapshot_id, uri, href, external_url)
VALUES (1, 'playlist_spotify_id', 'Overlap Playlist', 'Overlap', 100, 1, 'snapshot1', 'uri1', 'href1', 'external_url1');

-- Covering Constraint: Inserting data into Audiobook that covers Playlist

-- Inserting into Audiobook
INSERT INTO Audiobook (audiobook_id, description, edition, publisher, total_chapters, media_type)
VALUES (2, 'Covering', 'Edition2', 'Publisher2', 20, 'AudioBook');