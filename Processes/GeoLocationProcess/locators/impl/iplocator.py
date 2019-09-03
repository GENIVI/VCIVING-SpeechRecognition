from GeoLocationProcess.locators.abstracts import Locator
import urllib.request
import json
import GeoLocationProcess.locators.utils.ipaddr as iputils


# Uses ipstack.com IP's GeoLocation API
class IPLocator(Locator):

    API_ACCESS_KEY = "8bea242eb8b9b9d5b3a310bab03110fb"

    RESPONSE_KEY_LATITUDE = "latitude"
    RESPONSE_KEY_LONGITUDE = "longitude"

    # Constructor
    def __init__(self):
        pass

    # Used to obtain the current location as a tuple: latitude(double), longitude(double)
    def get_location(self):
        req_url = "http://api.ipstack.com/" + iputils.get_ip_address() + "?access_key=" + IPLocator.API_ACCESS_KEY + "&format=1"
        result = urllib.request.urlopen(req_url).read()
        result = result.decode()
        result = json.loads(result)

        latitude = result[IPLocator.RESPONSE_KEY_LATITUDE]
        longitude = result[IPLocator.RESPONSE_KEY_LONGITUDE]
        # Since altitude cannot be provided by IP Locations, it is set to 0
        altitude = 0

        return str(latitude), str(longitude), str(altitude)
