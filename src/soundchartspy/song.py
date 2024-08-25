from types import SimpleNamespace


class Song(SimpleNamespace):

    def __repr__(self):
        return f"Song({self.get_name()} by {self.get_main_artist_name()})"

    def __dict__(self):
        return {
            "uuid": self.get_uuid(),
            "name": self.get_name(),
            "isrc": self.get_isrc_value(),
            "isrc_country_code": self.get_isrc_country_code(),
            "isrc_country_name": self.get_isrc_country_name(),
            "credit_name": self.get_credit_name(),
            "artists": self.get_artists_list(),
            "main_artist_name": self.get_main_artist_name(),
            "main_artist_uuid": self.get_main_artist_uuid(),
            "release_date": self.get_release_date(),
            "duration": self.get_duration(),
            "root_genres": self.get_root_genres(),
            "sub_genres": self.get_sub_genres(),
            "composers": self.get_comosers(),
            "producers": self.get_producers(),
            "labels": self.get_labels(),
            "audio_features": self.get_audio_features()
        }

    def get_uuid(self):
        return self.uuid

    def get_name(self):
        return self.name

    def get_isrc_value(self):
        return self.isrc.get("value")

    def get_isrc_country_code(self):
        return self.isrc.get("countryCode")

    def get_isrc_country_name(self):
        return self.isrc.get("countryName")

    def get_credit_name(self):
        return self.creditName

    def get_artists_list(self):
        return self.artists

    def get_main_artist_name(self):
        return self.get_artists_list()[0].get("name")

    def get_main_artist_uuid(self):
        return self.get_artists_list()[0].get("uuid")

    def get_main_artist_sluf(self):
        return self.get_artists_list()[0].get("slug")

    def get_main_artist_app_url(self):
        return self.get_artists_list()[0].get("appUrl")

    def get_main_artist_image_url(self):
        return self.get_artists_list()[0].get("imageUrl")

    def get_release_date(self):
        return self.releaseDate

    def get_copy_right(self):
        return self.copyright

    def get_duration(self):
        return self.duration

    def get_root_genres(self):
        genres = self.genres
        root_genres = [item.get("root") for item in genres]
        return root_genres

    def get_sub_genres(self):
        genres = self.genres
        sub_genres = [item.get("sub") for item in genres]
        sub_genres = [item for sublist in sub_genres for item in sublist]
        return sub_genres

    def get_comosers(self):
        return self.composers

    def get_producers(self):
        return self.producers

    def get_labels(self):
        return self.labels

    def get_audio_features(self):
        return self.audio
