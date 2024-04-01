# from utility import variables as var
from spotify import scraper
from argparse import ArgumentParser

from utility.auth_token import SPOTIFY_AUTH_TOKEN


def main(args):
    if args.scrape_playlists:
        # spotify doesn't scrape playlists with batchmode
        playlists_scraper = scraper.SpotifyScraper("playlists")
        playlists_scraper.scrape_items()
        pass
    if args.load_tracks_from_playlists:
        pass
    if args.scrape_tracks:
        tracks_scraper = scraper.SpotifyScraper("tracks")
        tracks_scraper.scrape_items(batchmode=True)
    if args.load_artists_from_tracks:
        pass
    if args.scrape_artists:
        artists_scraper = scraper.SpotifyScraper("artists")
        artists_scraper.scrape_items(batchmode=True)
    if args.scrape_audiobooks:
        audiobooks_scraper = scraper.SpotifyScraper("audiobooks")
        audiobooks_scraper.scrape_items(batchmode=True)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-p', '--scrape-playlists', help=f'Scrapes playlists defined in csv file', action='store_true')
    parser.add_argument('-t', '--scrape-tracks', help=f'Scrapes tracks defined in csv file', action='store_true')
    parser.add_argument('-a', '--scrape-artists', help=f'Scrapes artists defined in csv file', action='store_true')
    parser.add_argument('-b', '--scrape-audiobooks', help=f'Scrapes audiobooks defined in csv file', action='store_true')
    parser.add_argument('-l', '--load-tracks-from-playlists', help=f'Loads tracks from playlists', action='store_true')
    parser.add_argument('-g', '--load-artists-from-tracks', help=f'Loads artists from tracks', action='store_true')
    args = parser.parse_args()
    main(args)
