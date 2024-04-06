-- Active: 1712072836115@@walidoow.com@3306@project

-- Query Implementation
-- You need to provide demonstrate the following query types:

-- 1. Basic select with simple where clause.
SELECT * FROM Track
WHERE duration_ms > 300000;

-- 2. Basic select with simple group by clause (with and without having clause).

-- Retrieve the total number of tracks for each album
SELECT album_id, album_name, release_date, COUNT(track_id) AS total_tracks
FROM Album 
INNER JOIN Tracks_Albums USING(album_id)
GROUP BY album_id;

-- Retrieve albums that have more than 10 tracks
SELECT album_id, album_name, release_date, COUNT(track_id) AS total_tracks
FROM Album 
INNER JOIN Tracks_Albums USING(album_id)
GROUP BY album_id
HAVING COUNT(track_id) > 10;

-- 3. A simple join select query using cartesian product and where clause vs. a join query using on.

-- Cartesian product with WHERE clause. 
-- Listing Artists and all of their aliases for all artists. 
-- If an artist does not have an alias, it will not be shown as a record in the result
SELECT Artist.artist_id, Artist.artist_name, Alias.alias_name FROM Artist, Alias
WHERE Artist.artist_id = Alias.artist_id;

-- Join query using ON keyword.
-- Same query as the one right above.
SELECT artist_id, artist_name, alias_name FROM Artist
INNER JOIN Alias ON Artist.artist_id = Alias.artist_id;

-- 4. A few queries to demonstrate various join types on the same tables: inner vs. outer (left and right) vs. full join. Use of null values in the database to show the differences is required.

-- INNER JOIN: Shows Track and Album records relationship. If no relationship then the record is not shown.
SELECT track_id, album_id FROM Album
INNER JOIN Tracks_Albums USING(album_id)
INNER JOIN Track USING(track_id);

-- LEFT JOIN (OUTER)
-- Select all columns joining Albums and Tracks where album_id is NULL.
-- This query shows all Albums that do not have tracks using LEFT JOIN.
SELECT album_id, album_name, track_id FROM Album
LEFT JOIN Tracks_Albums USING(album_id)
LEFT JOIN Track USING(track_id)
WHERE track_id IS NULL;

-- RIGHT JOIN (OUTER)
-- Select all track_ids that do not have an album using a RIGHT JOIN.
SELECT track_id, album_id FROM Album
RIGHT JOIN Tracks_Albums USING(album_id)
RIGHT JOIN Track USING(track_id)
WHERE album_id is NULL;

-- FULL JOIN
-- Combines the left join and right join results from the relationship of albums and tracks.
-- Combine queries above to get the full outer join between Track and Album
SELECT track_id, album_id FROM Album
LEFT JOIN Tracks_Albums USING(album_id)
LEFT JOIN Track USING(track_id)
UNION
SELECT track_id, album_id FROM Album
RIGHT JOIN Tracks_Albums USING(album_id)
RIGHT JOIN Track USING(track_id);

-- 5. A couple of examples to demonstrate correlated queries.

-- Correlated Subquery to Find Artists with More Than a Certain Number of Tracks:
SELECT artist_name FROM Artist a
WHERE (
    SELECT COUNT(*) FROM Tracks_Artists ta
    JOIN Track t ON ta.track_id = t.track_id
    WHERE ta.artist_id = a.artist_id
) > 5;

-- Finding Artists with More Than 10 Tracks
SELECT playlist_id, playlist_name
FROM Playlist p
WHERE (SELECT COUNT(*)
       FROM Playlists_Tracks pt
       WHERE pt.playlist_id = p.playlist_id) > 10;

-- 6. One example per set operations: intersect, union, and difference vs. their equivalences without using set operations.

-- Using Set Operation (Intersect)
-- Get all artists that did release an album named `UTOPIA`
SELECT artist_name FROM Artist
INTERSECT
SELECT artist_name FROM Tracks_Artists ta
INNER JOIN Artist a ON ta.artist_id = a.artist_id
INNER JOIN Track t ON ta.track_id = t.track_id
INNER JOIN Tracks_Albums tra ON t.track_id = tra.track_id
INNER JOIN Album al ON tra.album_id = al.album_id
WHERE al.album_name = 'UTOPIA';

-- Equivalent without Set Operation
SELECT DISTINCT a.artist_name FROM Artist a
INNER JOIN Tracks_Artists ta ON a.artist_id = ta.artist_id
INNER JOIN Track t ON ta.track_id = t.track_id
INNER JOIN Tracks_Albums tra ON t.track_id = tra.track_id
INNER JOIN Album al ON tra.album_id = al.album_id
WHERE al.album_name = 'UTOPIA';

-- Using Set Operation (Union)
SELECT artist_name FROM Artist
WHERE nb_followers > 1000
UNION 
SELECT artist_name FROM Artist
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
WHERE al.album_name = 'HEROES & VILLAINS';

-- Equivalent without Set Operation
SELECT DISTINCT a.artist_name FROM Artist a
LEFT JOIN Tracks_Artists ta ON a.artist_id = ta.artist_id
LEFT JOIN Track t ON ta.track_id = t.track_id
LEFT JOIN Tracks_Albums tra ON t.track_id = tra.track_id
LEFT JOIN Album al ON tra.album_id = al.album_id
WHERE al.album_name != 'HEROES & VILLAINS'
OR al.album_name IS NULL;


-- 7. An example of a view that has a hard-coded criteria, by which the content of the view may change upon changing the hard-coded value (see L09 slide 24).
-- Create a view to display detailed information about popular tracks by genre
-- Popular Tracks by genre, querying all tracks with popularity of more than 80. 80 is the hardcoded value.
CREATE OR REPLACE VIEW PopularTracksByGenre AS
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

CREATE TRIGGER enforce_playlist_market_constraint
BEFORE INSERT ON Playlists_Tracks
FOR EACH ROW
BEGIN
    DECLARE album_market INT;
    DECLARE playlist_market INT;
    -- Fetch the market of the album associated with the track being inserted
    SELECT market_id INTO album_market FROM Available_Markets_Albums WHERE album_id = NEW.album_id;
    -- Fetch the market of the playlist being inserted
    SELECT market_id INTO playlist_market FROM Playlist WHERE playlist_id = NEW.playlist_id;
    
    -- Check if the album market matches the playlist market
    IF album_market IS NULL OR playlist_market IS NULL OR album_market != playlist_market THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Cannot insert track into playlist. Album not available in the playlist market.';
    END IF;
END;