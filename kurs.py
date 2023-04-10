import requests
from pprint import pprint
import os


class VKDownload():
    url = 'https://api.vk.com/method/'
    filenames = []

    def profile_photos(self):
        profile_photos_params = {
            'album_id': 'profile'
        }
        profile_photos = requests.get(self.url + 'photos.get', params={**self.params, **profile_photos_params} ).json()
        sizes_list = profile_photos['response']['items']

        profile_photos_urls = []
        for photo in sizes_list:
            types = []

            for size in photo['sizes']:
                types.append(size['type'])

            for size in photo['sizes']:
                types.append(size['type'])
                if size['type'] == 'w' or size['type'] == 'z' or size['type'] == max(types):
                    photo_data = {
                                  'date': photo['date'],
                                  'url': size['url']
                                  }
                    profile_photos_urls.append(photo_data)
        return profile_photos_urls

    def one_photos_list(self):
        all_urls = []
        all_urls.extend(self.profile_photos())
        return all_urls

    def downloading(self):
        os.mkdir('reserve_copy')
        photos = self.one_photos_list()
        for picture in photos:
            r = requests.get(picture['url'])
            with open(f'reserve_copy/{picture["date"]}.jpg', 'wb') as file:
                file.write(r.content)
                filename = f'{picture["date"]}.jpg'
                self.filenames.append(filename)
                print(f'file {picture["date"]}.jpg downloaded')

        return self.filenames


class YandexDisk():

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def get_files_list(self):
        files_url = 'https://cloud-api.yandex.net/v1/disk/resources/files'
        headers = self.get_headers()
        response = requests.get(files_url, headers=headers)
        return response.json()

    def _get_upload_link(self, disk_file_path):
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        headers = self.get_headers()
        params = {"path": disk_file_path, "overwrite": "true"}
        response = requests.get(upload_url, headers=headers, params=params)
        return response.json()

    def upload_file_to_disk(self, disk_file_path, filename):
        href = self._get_upload_link(disk_file_path=disk_file_path).get("href", "")
        response = requests.put(href, data=open(filename, 'rb'))
        response.raise_for_status()
        if response.status_code == 201:
            print("Success")

    def new_folder(self):
        url_folder = "https://cloud-api.yandex.net/v1/disk/resources/"
        params = {
            'path': '/VKPHOTO'
        }
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(token)
        }

        r = requests.put(url_folder, params=params, headers=headers)
        for item in VKDownload.downloading(self):
            self.upload_file_to_disk(f'VKPHOTO/{item}', f'reserve_copy/{item}')

class Launcher(VKDownload, YandexDisk):
    def __init__(self, vk_token, token, owner_id=None):
        self.token = token
        self.params = {
            'owner_id': owner_id,
            'access_token': vk_token,
            'v': '5.131',
        }

vk_token = ''
token = ''

a = Launcher(vk_token, token)
a.new_folder()