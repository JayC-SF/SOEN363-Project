from spotify.models.audio_model import AudioModel


class TrackModel(AudioModel):
    def __init__(self, spotify_id, audio_name, uri, href, external_url, explicit, track_id, popularity, type, duration_ms, is_playable, preview_url, disc_number):
        AudioModel.__init__(self, spotify_id, audio_name, uri, href, external_url, explicit)
        self.track_id = track_id
        self.popularity = popularity
        self.type = type
        self.duration_ms = duration_ms
        self.is_playable = is_playable
        self.preview_url = preview_url
        self.disc_number = disc_number
