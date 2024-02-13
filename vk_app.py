import logging
import requests


class APIClient:
    API_BASE_URL = 'https://api.vk.com/method/'

    def __init__(self, user_id, token_vk, token_yd=None, user_albums=None, target_album=None):
        self.user_id = user_id
        self.token_vk = token_vk
        self.token_yd = token_yd
        self.user_albums = user_albums
        self.target_album = target_album

    def get_common_params(self):
        return {
            'access_token': self.token_vk,
            'v': '5.131'
        }

    # CREATE_URL
    def build_url(self, api_method):
        return f'{self.API_BASE_URL}{api_method}'

    # GET_PROFILE_PHOTOS
    def get_profile_photos(self):
        params = self.get_common_params()
        params.update({'owner_id': self.user_id, 'album_id': 'profile'})
        response = requests.get(self.build_url('photos.get'), params=params)
        logging.info(f"STATUS - {response.status_code}")

        return response.json()

    # GET_ALBUM_PHOTOS
    # def get_album_photos(self, album_id):
    #     params = self.get_common_params()
    #     params.update({'owner_id': self.user_id, 'album_id': album_id})
    #     response = requests.get(self.build_url('photos.get'), params=params)
    #     pprint(response.json())

    # GETTING PHOTO FROM ALBUM
    def get_photo_from_album(self, album):
        logging.info('GET_PHOTO_FROM_ALBUM')
        params = self.get_common_params()
        params.update({'owner_id': self.user_id, 'album_id': str(album[1]), 'extended': 1})
        response = requests.get(self.build_url('photos.get'), params=params)
        logging.info(f"STATUS - {response.status_code}")
        list_photos = []
        for element in response.json().get('response').get('items'):
            for el_2 in element.get('sizes'):
                if el_2.get('type') == 'w':
                    # print(f'____________________________________________\n'
                    #       f'{el_2}')
                    list_photos.append([element.get('likes').get('count'), element.get('date'), el_2.get('url')])
                    break
                elif el_2.get('type') == 'z':
                    # print(f'____________________________________________\n'
                    #       f'Выбран {el_2}')

                    list_photos.append([element.get('likes').get('count'), element.get('date'), el_2.get('url')])
                    break
                elif el_2.get('type') == 'y':
                    # print(f'____________________________________________\n'
                    #       f'Выбран {el_2}')

                    list_photos.append([element.get('likes').get('count'), element.get('date'), el_2.get('url')])
                    break
        # pprint(list_photos)  # Получаем список с id фото и url
        return list_photos

    # GET_USER_ALBUMS
    def get_user_albums(self):
        logging.info('GET_USER_ALBUMS')
        params = self.get_common_params()
        params.update({'owner_id': self.user_id})
        response = requests.get(self.build_url('photos.getAlbums'), params=params)
        logging.info(f"STATUS - {response.status_code}")
        albums = []
        for element in response.json().get('response').get('items'):
            title = element.get('title')
            album_id = element.get('id')
            albums.append([title, album_id])
            self.user_albums = albums
        return albums
