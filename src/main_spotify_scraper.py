from utility import variables as var
from spotify_scraper import playlists


def main():
    auth = var.SPOTIFY_AUTH_TOKEN.get_authorization()
    # print(auth)
    # print(var.SPOTIFY_AUTH_TOKEN.get_authorization())
    playlists.scrape_playlists()


if __name__ == "__main__":
    main()
