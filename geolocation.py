import requests

class Geolocation():

    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

    # получить файл JSON по координатам
    # вытащить из него id геолокаций
    def get_location_id(self, latitude, longitude):
        url = 'https://api.instagram.com/v1/'
        access_token = "6918512031.3449bf9.51192f57c96c446fbb2ce0780a773d85"
        distance = '5000'
        location_id = []
        request_url = (
                url + 'locations/search?lat=' + latitude + '&lng=' + longitude + '&distance=' + distance + '&access_token=' + access_token)
        print('Get request url: %s' % (request_url))
        location_info = requests.get(request_url).json()
        location_id = [element['id'] for element in location_info['data'] if element['id']!=0 ]
        print('Location id:')
        print(location_id)
        return location_id