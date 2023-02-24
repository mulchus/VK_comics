import requests
from urllib import parse
from pathlib import Path, PurePosixPath
from environs import Env
from random import randint


COMIC_LINK = 'https://xkcd.com/'
COMIC_DIR = 'Comics'


def get_comic_parametrs(comin_number):
    try:
        response = requests.get(f'{COMIC_LINK}{str(comin_number)}/info.0.json')
        response.raise_for_status()
        return response
    except requests.exceptions.HTTPError as error:
        print(f'Указан неверный номер комикса.\nОшибка {error}')
        exit()


def save_comic(comic_img_url, file_dir):
    file_path = Path.cwd() / file_dir
    file_name = PurePosixPath(parse.urlsplit(comic_img_url).path).name
    payload = None
    response = requests.get(comic_img_url, params=payload)
    response.raise_for_status()
    Path(file_path).mkdir(parents=True, exist_ok=True)
    with open(Path.joinpath(file_path, file_name), 'wb') as file:
        file.write(response.content)
    return file_name


# def format_date(str_date):
#     date_ = datetime.strptime(str_date, "%d.%m.%Y").date()
#     return date_, date_.strftime("%Y-%m-%d"), date_.strftime("%Y/%m/%d")


def get_groups(vk_access_token, vk_group_id):
    url = 'https://api.vk.com/method/groups.get'
    headers = {'Authorization': f'Bearer {vk_access_token}'}
    payload = {
        'group_id': vk_group_id,
        'v': 5.131,
    }
    response = requests.get(url, headers=headers, params=payload)
    response.raise_for_status()
    return response.json()


def get_request_to_vk(vk_access_token, url, payload):
    headers = {'Authorization': f'Bearer {vk_access_token}'}
    response = requests.get(url, headers=headers, params=payload)
    response.raise_for_status()
    return response


def post_request_to_vk(vk_access_token, url, payload):
    headers = {'Authorization': f'Bearer {vk_access_token}'}
    response = requests.post(url, headers=headers, params=payload)
    response.raise_for_status()
    return response


def get_photos_wall_upload_server(vk_access_token, vk_group_id):
    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    payload = {
        'group_id': vk_group_id,
        'v': 5.131,
    }
    response = get_request_to_vk(vk_access_token, url, payload).json()
    return response['response']['album_id'], response['response']['upload_url']


def post_wall_photo(vk_access_token, vk_group_id, upload_url, photo, comic_alt):
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
    save_file_params = get_request_to_vk(vk_access_token, url, payload).json()

    url = 'https://api.vk.com/method/wall.post'
    payload = {
        'attachments': f"photo{save_file_params['response'][0]['owner_id']}_{save_file_params['response'][0]['id']}",
        'owner_id': f'-{vk_group_id}',
        'message': comic_alt,
        'v': 5.131,
    }
    post_params = post_request_to_vk(vk_access_token, url, payload).json()
    print(post_params)


def main():
    env = Env()
    env.read_env()
    vk_access_token = env.str('VK_ACCESS_TOKEN')
    vk_group_id = env.int('VK_GROUP_ID')

    last_comic_id = get_comic_parametrs('').json()['num']
    random_comic_id = randint(1, last_comic_id)
    print(f'Публикуем комикс № {random_comic_id}')
    comic_parametrs = get_comic_parametrs(random_comic_id).json()
    comic_img_url = comic_parametrs['img']
    comic_alt = comic_parametrs['alt']

    comic_name = save_comic(comic_img_url, COMIC_DIR)

    album_id, upload_url = get_photos_wall_upload_server(vk_access_token, vk_group_id)

    file_path = Path.cwd() / COMIC_DIR
    with open(Path.joinpath(file_path, comic_name), 'rb') as photo:
        post_wall_photo(vk_access_token, vk_group_id, upload_url, photo, comic_alt)


if __name__ == "__main__":
    main()
