import configparser
from urllib.parse import urlencode


config = configparser.ConfigParser()
config.read('config.ini')

APP_ID = config.get('VK_APP', 'VK_APP_ID')

OAUTH_BASE_URL = 'https://oauth.vk.com/authorize'

params = {
    'client_id': APP_ID,
    'redirect_uri': 'https://oauth.vk.com/blank.html',
    'display': 'page',
    'scope': 'photos',
    'response_type': 'token'
}

oauth_url = f'{OAUTH_BASE_URL}?{urlencode(params)}'

def get_token(url = oauth_url):
    token = input(f'Пройдите по указанной ссылке {url} \nВставьте скопированный из адресной строки токен: ')
    # config.set('user_id', 'TOKEN_VK', token)
    # with open('config.ini', 'a') as config_file:
    #     config.write(config_file)
    return token






