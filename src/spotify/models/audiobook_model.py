class AudiobookModel:
    def __init__(self, audiobook_id: int, description: str, external_url: str, edition: str, explicit: bool, uri: str,
                 publisher: str, total_chapters: int, media_type: str, href: str, name: str):
        self.audiobook_id = audiobook_id
        self.description = description
        self.external_url = external_url
        self.edition = edition
        self.explicit = explicit
        self.uri = uri
        self.publisher = publisher
        self.total_chapters = total_chapters
        self.media_type = media_type
        self.href = href
        self.name = name
