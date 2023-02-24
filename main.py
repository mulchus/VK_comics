import requests
from urllib import parse
from datetime import datetime
from pathlib import Path, PurePosixPath


COMIC_LINK = 'https://xkcd.com/'
COMIC_DIR = 'COMICS'


def get_comic_parametrs(comin_number):
    try:
        response = requests.get(f'{COMIC_LINK}{str(comin_number)}/info.0.json')
        response.raise_for_status()
        comic = response.json()
        comic_img_url = comic['img']
        comic_alt = comic['alt']
        return comic_img_url, comic_alt
    except requests.exceptions.HTTPError as error:
        print(f'Указан неверный номер комикса.\nОшибка {error}')


def save_comic(comic_img_url, file_dir, payload=None):
    file_path = Path.cwd() / file_dir
    file_name = PurePosixPath(parse.urlsplit(comic_img_url).path).name
    response = requests.get(comic_img_url, params=payload)
    response.raise_for_status()
    Path(file_path).mkdir(parents=True, exist_ok=True)
    with open(Path.joinpath(file_path, file_name), 'wb') as file:
        file.write(response.content)


def format_date(str_date):
    date_ = datetime.strptime(str_date, "%d.%m.%Y").date()
    return date_, date_.strftime("%Y-%m-%d"), date_.strftime("%Y/%m/%d")


def main():
    comic_number = 353
    comic_img_url, comic_alt = get_comic_parametrs(comic_number)
    save_comic(comic_img_url, COMIC_DIR)


if __name__ == "__main__":
    main()
