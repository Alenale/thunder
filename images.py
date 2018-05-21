import requests
import dpath
from collections import defaultdict
from database import DataStorage
from geolocation import Geolocation

img_dict = defaultdict(list)
# Аттрибут класса DataStorage

class Images(DataStorage):

    def __init__(self, location_id):
        DataStorage.__init__(self, 'images')
        self.location_id = location_id


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
        tags = ['thunder', 'lightning', 'storm','thunderbolt', 'thunderstorm', 'thunderstruck', 'thunderbirds', 'thunderclouds', 'lightning', 'thunderup', 'heatlightning']
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
                    img_dict['loc_name'].append(loc_name)
                    img_dict['image'].append(img)
                    img_dict['time_inst'].append(img_time)
            else:
                print("No text or it's video")
            ind_publication = int(ind_publication)
            ind_publication += 1
        DataStorage.__setitem__(self, img_dict)
        DataStorage.finish(self)
        print(img_dict)

if __name__ == '__main__':
    print("Input latitude and logitude")
    lat = input()
    lon = input()
    geolocation = Geolocation(lat, lon)
    loc_id = []
    loc_id = geolocation.get_location_id(lat, lon)
    img = Images(loc_id)
    for ind in loc_id:
        img.get_images(ind)