"""Задание на дипломный проект «Резервное копирование» первого блока «Основы языка программирования Python».
Возможна такая ситуация, что мы хотим показать друзьям фотографии из социальных сетей, но соц.
сети могут быть недоступны по каким-либо причинам. Давайте защитимся от такого.
Нужно написать программу для резервного копирования фотографий с профиля(аватарок)
пользователя vk в облачное хранилище Яндекс.Диск.
Для названий фотографий использовать количество лайков, если количество лайков одинаково,
то добавить дату загрузки.
Информацию по сохраненным фотографиям сохранить в json-файл.

Задание:
Нужно написать программу, которая будет:

Получать фотографии с профиля. Для этого нужно использовать метод photos.get.
Сохранять фотографии максимального размера(ширина/высота в пикселях) на Я.Диске.
Для имени фотографий использовать количество лайков.
Сохранять информацию по фотографиям в json-файл с результатами.

Входные данные:
Пользователь вводит:
id пользователя vk;
токен с Полигона Яндекс.Диска. Важно: Токен публиковать в github не нужно!
Выходные данные:
json-файл с информацией по файлу:
    [{
    "file_name": "34.jpg",
    "size": "z"
    }]
Измененный Я.диск, куда добавились фотографии.

Обязательные требования к программе:
Использовать REST API Я.Диска и ключ, полученный с полигона.
Для загруженных фотографий нужно создать свою папку.
Сохранять указанное количество фотографий(по умолчанию 5) наибольшего размера (ширина/высота в пикселях) на Я.Диске
Сделать прогресс-бар или логирование для отслеживания процесса программы.
Код программы должен удовлетворять PEP8.

Необязательные требования к программе:
Сохранять фотографии и из других альбомов.
Сохранять фотографии из других социальных сетей. Одноклассники и Инстаграмм
Сохранять фотографии на Google.Drive.
"""

import requests
from urllib.parse import urlencode, urljoin
import os
import tqdm
import json
from pprint import pprint
TOKEN_VK = ''
ID_VK = 1111111
TOKEN_YA = ''
API_BASE_URL = "https://api.vk.com/method/"
V = '5.124'
PHOTO_FOLDER = 'photo'


def receiving_photos(id = ID_VK):
    photo_get_url = urljoin(API_BASE_URL, 'photos.get')
    res = requests.get(photo_get_url, params = {
        'access_token': TOKEN_VK,
        "v": V,
        'owner_id': id,
        'album_id': 'profile',
        'extended': 1
    })
    return res.json()['response']['items']


def inquiry_url_yandex(token,way):
    HEADERS = {"Authorization": f"OAuth {token}"}
    response = requests.get('https://cloud-api.yandex.net/v1/disk/resources/upload',
                            params={"path": way, 'overwrite': True},
                            headers=HEADERS
                            )
    return response.json()['href']

def upload_photo_to_disk(photos):
    for pfoto in tqdm.tqdm(photos):
        like = pfoto['likes']['count']
        # print(like)
        size = pfoto['sizes']
        list_json = []
        for title in size:
            if 'w' in title['type']:
              foto_url = title['url']
              foto_size = title['type']
              response = requests.get(foto_url)
              with open(os.path.join(PHOTO_FOLDER, str(like) + '.jpg'), 'wb') as f:
                  f.write(response.content)
              list_json.append({'file_name': str(like) + '.jpg', 'size': foto_size})
    data_json = os.path.join(os.getcwd(), 'data.json')
    with open("file_path", "w", encoding="cp1251") as f:
        json.dump(list_json, f, ensure_ascii=False, indent=2)
    for photo in tqdm.tqdm(os.listdir(os.path.join(os.getcwd(), PHOTO_FOLDER))):
        yd_photo_path = f"/photo_vk/{photo}"
        with open(os.path.join(os.getcwd(), PHOTO_FOLDER, photo), 'rb') as f:
            resp = requests.put(inquiry_url_yandex(TOKEN_YA,yd_photo_path),
                                          files={'file': f})

    return data_json



print(upload_photo_to_disk(receiving_photos()))


