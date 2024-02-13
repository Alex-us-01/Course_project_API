
import logging
from vk_auth import get_token
from vk_app import APIClient
from yandex_disc import get_folder, add_photo

logging.basicConfig(level=logging.INFO, encoding='utf-8', format="%(asctime)s %(levelname)s %(message)s",
                    filename='log(INFO).log', filemode='a')



def start():
    print('Привет. Я помогу тебе сделать резервные копии твоих фотографий из "ВК"')
    user_id = input('Введите числовой ID своей страницы в "ВК": ')
    logging.info('VK_USER_ID - received')
    if user_id.isdigit():
        token = get_token()
        logging.info('VK_API_TOKEN - received')
        user = APIClient(user_id=user_id, token_vk=token)
        token_yd = input('Введите токен Яндекс Диска: ')
        user.token_yd = 'OAuth ' + token_yd
        logging.info('YANDEX_DISK_TOKEN - received')

    else:
        print('Вы ввели не числовой ID пользователя VK')
        logging.info('INCORRECT_VK_USER_ID')
        return start()

    list_albums = user.get_user_albums()
    for element in enumerate(list_albums):
        print(f'{element[0]} - {element[1][0]}')
    album = input('Выберите номер альбома из списка: ')
    if album.isdigit():

        if int(album) <= len(user.user_albums) - 1:
            logging.info('ALBUM - received')
            print(f'Вы выбрали альбом: {user.user_albums[int(album)][0]}')
            user.target_album = user.user_albums[int(album)]
            get_folder(user.target_album[0], user.token_yd)  # Создаем папку для выбранного альбома
            list_photos = user.get_photo_from_album(user.target_album)
            add_photo(user.token_yd, user.target_album[0], list_photos)


        else:
            print('Указанный номер альбома отсутствует в списке.')
            logging.info('INCORRECT_ALBUM')
            start()
    else:
        print('Введите порядковый номер альбома')
        logging.info('INCORRECT_ALBUM:(isdigit - False')


if __name__ == '__main__':
    start()

