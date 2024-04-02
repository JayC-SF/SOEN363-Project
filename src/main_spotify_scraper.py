# from utility import variables as var
from musicbrainz.loader import AliasLoader
from spotify import loader, scraper
from argparse import ArgumentParser

from utility.auth_token import SPOTIFY_AUTH_TOKEN


def main(args):
    # SPOTIFY_AUTH_TOKEN.get_authorization()
    if args.scrape_playlists:
        # spotify doesn't scrape playlists with batchmode
        playlists_scraper = scraper.SpotifyScraper("playlists")
        playlists_scraper.scrape_items()
        pass
    if args.load_info_from_playlists:
        loader.load_info_from_playlists()
    if args.scrape_tracks:
        tracks_scraper = scraper.SpotifyScraper("tracks")
        tracks_scraper.scrape_items(batchmode=True)
    if args.scrape_artists:
        artists_scraper = scraper.SpotifyScraper("artists")
        artists_scraper.scrape_items(batchmode=True)
    if args.scrape_albums:
        albums_scraper = scraper.SpotifyScraper("albums")
        albums_scraper.scrape_items(batchmode=True)
    if args.scrape_audiobooks:
        audiobooks_scraper = scraper.SpotifyScraper("audiobooks")
        audiobooks_scraper.scrape_items(batchmode=True)
    if args.generate_artist_ids:
        artists_generate = scraper.SpotifyScraper("artists")
        artists_generate.generate_artists_ids()
    if args.generate_playlist_ids:
        playlists_generate = scraper.SpotifyScraper("playlists")
        playlists_generate.generate_playlist_ids()
    if args.load_musicbrainz_ids:
        loader_musicbrainz = AliasLoader("aliases")
        loader_musicbrainz.write_artist_data_to_csv()
    if args.generate_musicbrainz_aliases_json:
        generate_musicbrainz = AliasLoader("aliases")
        generate_musicbrainz.load_aliases_items()


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-p', '--scrape-playlists', help=f'Scrapes playlists defined in csv file', action='store_true')
    parser.add_argument('-t', '--scrape-tracks', help=f'Scrapes tracks defined in csv file', action='store_true')
    parser.add_argument('-a', '--scrape-artists', help=f'Scrapes artists defined in csv file', action='store_true')
    parser.add_argument('-u', '--scrape-albums', help=f'Scrapes albums defined in csv file', action='store_true')
    parser.add_argument('-b', '--scrape-audiobooks', help=f'Scrapes audiobooks defined in csv file', action='store_true')
    parser.add_argument('-l', '--load-info-from-playlists', help=f'Loads information from playlists into other entities\'s csv', action='store_true')
    parser.add_argument('-g', '--load-artists-from-tracks', help=f'Loads artists from tracks', action='store_true')
    parser.add_argument('-al', '--generate-artist-ids', help=f'Populates `ids.csv` of artists/ with list of ids', action='store_true')
    parser.add_argument('-pl', '--generate-playlist-ids', help=f'Populates `ids.csv` of playlists/ with list of playlists based on the Spotify Featured Playlists', action='store_true')
    parser.add_argument('-m', '--load-musicbrainz-ids', help=f'Populates `artist_names.csv` of "alias_ids.csv" inside the musicbrainz folder', action='store_true')
    parser.add_argument('-ml', '--generate-musicbrainz-aliases-json', help=f'Fetch MusicBrainz API for every artist name', action='store_true')


    # Run below if token expires at root dir through src/main_spotify_scraper.py
    # SPOTIFY_AUTH_TOKEN.refresh_token()
    # parser.add_argument('')
    args = parser.parse_args()
    
    main(args)
