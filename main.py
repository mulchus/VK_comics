import requests
from urllib import parse
from urllib.error import HTTPError
from pathlib import Path
from environs import Env
from random import randint


COMIC_LINK = 'https://xkcd.com/'


def check_vk_request_error(response):
    error_code = 0
    if 'error' in response:
        error_message = response['error']['error_msg']
        if response['error']['error_code']:
            error_code = response['error']['error_code']
        raise HTTPError('Ошибка сервиса ВКонтакте', error_code, error_message, error_message, None)


def get_photos_wall_upload_server(vk_access, vk_group_id):
    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    payload = {
        'group_id': vk_group_id,
        'v': 5.131,
    }
    response = requests.get(url, headers=vk_access, params=payload)
    response.raise_for_status()
    response = response.json()
    check_vk_request_error(response)
    return response['response']['album_id'], response['response']['upload_url']


def save_photo_to_wall(vk_access, vk_group_id, upload_url, file_path, comic_file_name):
    with open(Path.joinpath(file_path, comic_file_name), 'rb') as photo:
        response = requests.post(upload_url, files={'photo': photo})
    response.raise_for_status()
    transfer_file_params = response.json()

    url = 'https://api.vk.com/method/photos.saveWallPhoto'
    payload = {
        'group_id': vk_group_id,
        'server': transfer_file_params['server'],
        'photo': transfer_file_params['photo'],
        'hash': transfer_file_params['hash'],
        'v': 5.131,
    }
    response = requests.get(url, headers=vk_access, params=payload)
    response.raise_for_status()
    save_file_params = response.json()
    check_vk_request_error(save_file_params)
    return save_file_params


def post_wall_photo(vk_access, vk_group_id, comic_alt, save_file_params):
    url = 'https://api.vk.com/method/wall.post'
    payload = {
        'attachments': f"photo{save_file_params['response'][0]['owner_id']}_{save_file_params['response'][0]['id']}",
        'owner_id': f'-{vk_group_id}',
        'message': comic_alt,
        'v': 5.131,
    }
    response = requests.post(url, headers=vk_access, params=payload)
    response.raise_for_status()
    response = response.json()
    check_vk_request_error(response)


def get_random_comic():
    last_comic = requests.get(f'{COMIC_LINK}/info.0.json')
    last_comic.raise_for_status()
    last_comic_id = last_comic.json()['num']

    random_comic_id = randint(1, last_comic_id)

    comic_parameters = requests.get(f'{COMIC_LINK}{str(random_comic_id)}/info.0.json')
    comic_parameters.raise_for_status()
    comic_parameters = comic_parameters.json()

    comic = requests.get(comic_parameters['img'])
    comic.raise_for_status()

    return comic_parameters, comic, random_comic_id


def main():
    env = Env()
    env.read_env()
    vk_access_token = env.str('VK_ACCESS_TOKEN')
    vk_group_id = env.int('VK_GROUP_ID')
    vk_access = {'Authorization': f'Bearer {vk_access_token}'}

    file_path = Path.cwd()
    Path(file_path).mkdir(parents=True, exist_ok=True)

    comic_parameters, comic, random_comic_id = get_random_comic()
    comic_file_name = Path(parse.urlsplit(comic_parameters['img']).path).name

    try:
        with open(Path.joinpath(file_path, comic_file_name), 'wb') as file:
            file.write(comic.content)
        print(f'Публикуем комикс № {random_comic_id}')
        album_id, upload_url = get_photos_wall_upload_server(vk_access, vk_group_id)
        save_file_params = save_photo_to_wall(vk_access, vk_group_id, upload_url, file_path, comic_file_name)
        post_wall_photo(vk_access, vk_group_id, comic_parameters['alt'], save_file_params)
    except requests.exceptions.HTTPError as error:
        print(f'Ошибка сети.\nОшибка {error}')
    finally:
        Path(Path.joinpath(file_path, comic_file_name)).unlink()


if __name__ == "__main__":
    main()
