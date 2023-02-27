import requests
from urllib import parse
from pathlib import Path, PurePosixPath
from environs import Env
from random import randint


COMIC_LINK = 'https://xkcd.com/'


def get_photos_wall_upload_server(vk_access_token, vk_group_id):
    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    headers = {'Authorization': f'Bearer {vk_access_token}'}
    payload = {
        'group_id': vk_group_id,
        'v': 5.131,
    }
    response = requests.get(url, headers=headers, params=payload)
    response.raise_for_status()
    response = response.json()
    return response['response']['album_id'], response['response']['upload_url']


def post_wall_photo(vk_access_token, vk_group_id, upload_url, comic_alt, file_path, comic_file_name):
    with open(Path.joinpath(file_path, comic_file_name), 'rb') as photo:
        response = requests.post(upload_url, files={'photo': photo})
    response.raise_for_status()
    transfer_file_params = response.json()

    url = 'https://api.vk.com/method/photos.saveWallPhoto'
    headers = {'Authorization': f'Bearer {vk_access_token}'}
    payload = {
        'group_id': vk_group_id,
        'server': transfer_file_params['server'],
        'photo': transfer_file_params['photo'],
        'hash': transfer_file_params['hash'],
        'v': 5.131,
    }
    response = requests.get(url, headers=headers, params=payload)
    response.raise_for_status()
    save_file_params = response.json()

    url = 'https://api.vk.com/method/wall.post'
    payload = {
        'attachments': f"photo{save_file_params['response'][0]['owner_id']}_{save_file_params['response'][0]['id']}",
        'owner_id': f'-{vk_group_id}',
        'message': comic_alt,
        'v': 5.131,
    }
    response = requests.post(url, headers=headers, params=payload)
    response.raise_for_status()


def get_random_comic():
    last_comic = requests.get(f'{COMIC_LINK}/info.0.json')
    last_comic.raise_for_status()
    last_comic_id = last_comic.json()['num']

    random_comic_id = randint(1, last_comic_id)

    comic_parametrs = requests.get(f'{COMIC_LINK}{str(random_comic_id)}/info.0.json')
    comic_parametrs.raise_for_status()
    comic_parametrs = comic_parametrs.json()

    comic = requests.get(comic_parametrs['img'])
    comic.raise_for_status()

    return comic_parametrs, comic, random_comic_id


def delete_comic(file_path, comic_file_name):
    Path(Path.joinpath(file_path, comic_file_name)).unlink()


def main():
    env = Env()
    env.read_env()
    vk_access_token = env.str('VK_ACCESS_TOKEN')
    vk_group_id = env.int('VK_GROUP_ID')

    file_path = Path.cwd()
    Path(file_path).mkdir(parents=True, exist_ok=True)

    comic_parametrs, comic, random_comic_id = get_random_comic()
    comic_file_name = PurePosixPath(parse.urlsplit(comic_parametrs['img']).path).name

    try:
        with open(Path.joinpath(file_path, comic_file_name), 'wb') as file:
            file.write(comic.content)
        print(f'Публикуем комикс № {random_comic_id}')
        album_id, upload_url = get_photos_wall_upload_server(vk_access_token, vk_group_id)
        post_wall_photo(vk_access_token, vk_group_id, upload_url, comic_parametrs['alt'], file_path, comic_file_name)
    except requests.exceptions.HTTPError as error:
        print(f'Ошибка сети.\nОшибка {error}')
    finally:
        delete_comic(file_path, comic_file_name)


if __name__ == "__main__":
    main()
