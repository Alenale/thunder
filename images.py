import requests
import datetime
import dpath
from collections import defaultdict
from database import DataStorage

img_dict = defaultdict(list)
# Аттрибут класса DataStorage

class Images(DataStorage):
    # преобразовать долготу и ширину в строку перед вставкой в url
    def __init__(self, lat, lon):
        DataStorage.__init__(self, 'images')
        self.lat = lat
        self.lon = lon

    # получить данные по координатам
    # вытащить из них id'ники локаций
    # latitude = '41.845300'
    # longitude = '12.524698'
    def get_location_id(self, lat, lon):
        url = 'https://api.instagram.com/v1/'
        access_token = "6918512031.3449bf9.51192f57c96c446fbb2ce0780a773d85"
        distance = '5000'
        location_id = []
        request_url = (
        url +'locations/search?lat='+lat+'&lng='+lon+'&distance='+distance+'&access_token='+access_token)
        print('Get request url: %s' % (request_url))
        location_info = requests.get(request_url).json()
        location_id = [element['id'] for element in location_info['data']]
        print('Location id:')
        print(location_id)
        return location_id

    # по полученным локациям получить фотографии
    # для примера https://www.instagram.com/explore/locations/236889077/?__a=1
    # https://www.instagram.com/explore/locations/{location_id}/?__a=1
    # path /graphql/location/edge_location_to_media/edges/0/node/edge_media_to_caption/edges/0/node/text
    # обращение к тексту картинки images_info['graphql']['location']['edge_location_to_media']['edges'][i]['node']['edge_media_to_caption']['edges'][0]['node']
    def get_images(self, location_id):
        text_list = []
        image_info_url = 'https://www.instagram.com/explore/locations/'
        request_url = (image_info_url + location_id + '/?__a=1')
        print('Get request url: %s ' % (request_url))
        images_info = requests.get(request_url).json()
        ind_publication = 0
        length_info = len([element['node'] for element in images_info['graphql']['location']['edge_location_to_media']['edges']])
        tags = ['rome', 'thunder', 'lightning', 'storm','thunderbolt', 'thunderstorm', 'thunderstruck', 'thunderbirds', 'thunderclouds', 'lightning', 'thunderup', 'heatlightning']
        while ind_publication < length_info:
            ind_publication = str(ind_publication)
            is_video = dpath.util.get(images_info, '/graphql/location/edge_location_to_media/edges/' + ind_publication + '/node/is_video')
            is_text = dpath.util.get(images_info,
                                     '/graphql/location/edge_location_to_media/edges/' + ind_publication + '/node/edge_media_to_caption/edges')
            path_text = '/graphql/location/edge_location_to_media/edges/' + ind_publication + '/node/edge_media_to_caption/edges/0/node/text'
            path_img = '/graphql/location/edge_location_to_media/edges/' + ind_publication + '/node/display_url'
            path_name = '/graphql/location/name'
            path_time = '/graphql/location/edge_location_to_media/edges/' + ind_publication + '/node/taken_at_timestamp'
            if (len(is_text) != 0) and (not is_video):
                text = dpath.util.get(images_info, path_text)
                img = dpath.util.get(images_info, path_img)
                # поиск вхождения ключевых слов в описание
                find_in_str = [x for x in tags if text.find(x) > -1]
                # сохранить названия геолокации, ссылки, времени фотографии в бд в виде списка значений ключей
                if len(find_in_str) > 0 :
                    # получить название геолокации и дату
                    print("Have found!")
                    loc_name = dpath.util.get(images_info, path_name)
                    img_time = dpath.util.get(images_info, path_time)
                    time_inst = datetime.datetime.fromtimestamp(img_time).strftime('%Y-%m-%d %H:%M:%S')
                    img_dict['loc_name'].append(loc_name)
                    img_dict['image'].append(img)
                    img_dict['time_inst'].append(time_inst)
            else:
                print("No text or it's video")
            ind_publication = int(ind_publication)
            ind_publication += 1
        DataStorage.__setitem__(self, img_dict)
        DataStorage.finish(self)

if __name__ == '__main__':
    print("Input latitude and logitude")
    lat = input()
    lon = input()
    img = Images(lat, lon)
    loc_id = []
    loc_id = img.get_location_id(lat, lon)
    for ind in loc_id:
        img.get_images(ind)



