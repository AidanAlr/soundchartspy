from types import SimpleNamespace


class Playlist(SimpleNamespace):

    def __str__(self):
        return f"{self.get_name()} by {self.get_owner_name()} on {self.get_platform()}"

    def get_name(self):
        return self.name

    def get_platform(self):
        return self.platform

    def get_uuid(self):
        return self.uuid

    def get_identifier(self):
        return self.identifier

    def get_country_code(self):
        return self.countryCode

    def get_owner_name(self):
        return self.owner.get("name")

    def get_owner_identifier(self):
        return self.owner.get("identifier")

    def get_latest_crawl_date(self):
        return self.latestCrawlDate

    def get_latest_track_count(self):
        return self.latestTrackCount

    def get_latest_subscriber_count(self):
        return self.latestSubscriberCount

    def get_type(self):
        return self.type

    def get_refreshed(self):
        return self.refreshed

    def get_available_country_codes(self):
        return self.availableCountryCodes

    def get_app_url(self):
        return self.appUrl

    def get_image_url(self):
        return self.imageUrl



