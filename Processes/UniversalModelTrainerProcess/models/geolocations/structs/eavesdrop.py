from commons.universalmodel.geolocations.preferredgeolocations import PreferredGeoLocation


class EavesdropDataGeoLocation:

    def __init__(self, transcription: str, location_code: str, latitude: float, longitude: float):
        self._transcription = transcription
        self._location_code = location_code
        self._latitude = latitude
        self._longitude = longitude

    def get_transcription(self):
        return self._transcription

    def get_location_code(self):
        return self._location_code

    def get_latitude(self):
        return self._latitude

    def get_longitude(self):
        return self._longitude

    def get_preferred_geo_location(self):
        return PreferredGeoLocation(self._location_code, self._latitude, self._longitude)
