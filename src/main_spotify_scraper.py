# from utility import variables as var
from spotify_scraper import playlists, tracks
from argparse import ArgumentParser


def main(args):
    # auth = var.SPOTIFY_AUTH_TOKEN.get_authorization()
    # print(auth)
    # print(var.SPOTIFY_AUTH_TOKEN.is_expired())
    # print(var.SPOTIFY_AUTH_TOKEN.get_authorization())
    if args.scrape_playlists:
        playlists.scrape_playlists()
    if args.scrape_tracks:
        tracks.scrape_tracks()


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('-sp', '--scrape-playlists', help="Scrapes playlists defined in playlists.csv", action="store_true")
    parser.add_argument('-st', '--scrape-tracks', help="Scrapes tracks defined ", action="store_true")
    args = parser.parse_args()
    main(args)
