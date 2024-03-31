# from utility import variables as var
from spotify_scraper import scraper
from argparse import ArgumentParser

from utility.variables import SPOTIFY_PLAYLIST_ENDPOINT, SPOTIFY_PLAYLISTS_PATH, SPOTIFY_TRACK_ENDPOINT, SPOTIFY_TRACKS_PATH


def main(args):
    # auth = var.SPOTIFY_AUTH_TOKEN.get_authorization()
    # print(auth)
    # print(var.SPOTIFY_AUTH_TOKEN.is_expired())
    # print(var.SPOTIFY_AUTH_TOKEN.get_authorization())
    if args.scrape_playlists:
        scraper.scrape_items(SPOTIFY_PLAYLISTS_PATH, SPOTIFY_PLAYLIST_ENDPOINT, 'Playlist')
    if args.scrape_tracks:
        scraper.scrape_items(SPOTIFY_TRACKS_PATH, SPOTIFY_TRACK_ENDPOINT, 'Track')


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-sp', '--scrape-playlists', help='Scrapes playlists defined in playlists.csv', action='store_true')
    parser.add_argument('-st', '--scrape-tracks', help='Scrapes tracks defined ', action='store_true')
    args = parser.parse_args()
    main(args)
