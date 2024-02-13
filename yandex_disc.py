import datetime
import requests
import time
from alive_progress import alive_bar
import logging

base_url = 'https://cloud-api.yandex.net'


def get_time():
    date = datetime.datetime.now()
    return f"{date.hour}-{date.minute}-{date.second}"


def check_photo(token_yd, folder, name=None):
    logging.info('CHECK_PHOTO')
    url = base_url + '/v1/disk/resources'
    params = {
        'path': folder
    }
    headers_dict = {
        'Authorization': token_yd
    }
    response = requests.get(url, params=params, headers=headers_dict)
    logging.info(f"STATUS - {response.status_code}")
    data_album = response.json().get('_embedded').get('items')

    for element in data_album:
        # print(f'Проверяю файл - {element.get("name")}')
        if element.get('name') == str(name) + '.jpg':

            return True
        else:
            continue
    return False



def get_folder(name, token_yd):
    url_create_folder = base_url + '/v1/disk/resources'
    params = {
        'path': name
    }
    headers_dict = {
        'Authorization': token_yd
    }
    response = requests.put(url_create_folder, params=params, headers=headers_dict)
    # print(response.status_code)
    # print(response.json())


# ADD_PHOTO
def add_photo(token_yd, album, list_photo: list):
    logging.info('ADD_PHOTO_FROM_YANDEX_DISC')
    url_create_folder = base_url + '/v1/disk/resources/upload'
    headers_dict = {
        'Authorization': token_yd
    }
    with alive_bar(len(list_photo), force_tty=True) as bar:
        for element in list_photo:


            if check_photo(token_yd, album, element[0]) == True:
                params = {
                    'url': element[2],
                    'path': album + '/' + str(element[0]) + '-' + get_time() + '.jpg'
                }
                response = requests.post(url_create_folder, params=params, headers=headers_dict)
                logging.info(f"STATUS - {response.status_code}")
                # print(response.json())

                bar()
                time.sleep(3)
            else:
                params = {
                    'url': element[2],
                    'path': album + '/' + str(element[0]) + '.jpg'
                }
                response = requests.post(url_create_folder, params=params, headers=headers_dict)
                logging.info(f"STATUS - {response.status_code}")
                # print(response.json())
                bar()
                time.sleep(3)
