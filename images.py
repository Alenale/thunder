import requests
import json
import datetime
import dpath
import transaction
from collections import defaultdict
from database import DataStorage
URL = 'https://api.instagram.com/v1/'
IMAGE_INFO_URL = 'https://www.instagram.com/explore/locations/'
ACCESS_TOKEN = "6918512031.3449bf9.51192f57c96c446fbb2ce0780a773d85"

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
    def get_location_id(self, latitude, longitude):
        latitude = '41.845300'
        longitude = '12.524698'
        distance = '5000'
        location_id = []
        request_url = (
        URL +'locations/search?lat='+latitude+'&lng='+longitude+'&distance='+distance+'&access_token='+ACCESS_TOKEN)
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
        #img_dic.fromkeys(['loc_name', 'images', 'time_inst'])
        request_url = (IMAGE_INFO_URL + location_id + '/?__a=1')
        print('Get request url: %s ' % (request_url))
        images_info = requests.get(request_url).json()
        #length_info = sum(len(v) for v in images_info.values())
        #length_items = sum(len(v) for v in images_info.items())
        i = 0
        print("Length")
        length_info = len([element['node'] for element in images_info['graphql']['location']['edge_location_to_media']['edges']])
        tags = ['rome', 'thunder', 'lightning', 'storm','thunderbolt', 'thunderstorm', 'thunderstruck', 'thunderbirds', 'thunderclouds', 'lightning', 'thunderup', 'heatlightning']

        print(length_info)
        while i < length_info:
            i = str(i)
            is_video = dpath.util.get(images_info, '/graphql/location/edge_location_to_media/edges/' + i + '/node/is_video')
            is_text = dpath.util.get(images_info,
                                     '/graphql/location/edge_location_to_media/edges/' + i + '/node/edge_media_to_caption/edges')
            path_text = '/graphql/location/edge_location_to_media/edges/' + i + '/node/edge_media_to_caption/edges/0/node/text'
            path_img = '/graphql/location/edge_location_to_media/edges/' + i + '/node/display_url'
            path_name = '/graphql/location/name'
            path_time = '/graphql/location/edge_location_to_media/edges/' + i + '/node/taken_at_timestamp'
            #print("Is video? ")
            #print(is_video)
            # добавить условие, в котором будет слов в полученной строке без добавления в лист, вытягивать ссылку на изображение по i
            if (len(is_text) != 0) and (not is_video):
                #print("i: " + i)
                text = dpath.util.get(images_info, path_text)
                img = dpath.util.get(images_info, path_img)
                # фильтровать фотографии по наличию хэштегов
                find_in_str = [x for x in tags if text.find(x) > -1]
                # сохранить названия геолокации, ссылки, времени фотографии в бд в виде списка значений
                if len(find_in_str) > 0 :
                    # получить название геолокации и дату
                    loc_name = dpath.util.get(images_info, path_name)
                    img_time = dpath.util.get(images_info, path_time)
                    time_inst = datetime.datetime.fromtimestamp(img_time).strftime('%Y-%m-%d %H:%M:%S')
                    img_dict['loc_name'].append(loc_name)
                    img_dict['image'].append(img)
                    img_dict['time_inst'].append(time_inst)


            else:
                print("No text or it's video")
            i = int(i)
            i += 1

        DataStorage.__setitem__(self, img_dict)
        # print(DataStorage.__getitem__(self, 'image'))
        DataStorage.finish(self)

# 236889077
#get_images('236889077')
# после окончания получения ссылок раскоментить
img = Images('48.139141', '-3.756411')
loc_id = []
loc_id = img.get_location_id('1', '0')
for ind in loc_id:
    img.get_images(ind)



