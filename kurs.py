import requests
from pprint import pprint
import os


class VKDownload():
    url = 'https://api.vk.com/method/'


    def likes(self):
        likes_params = {
            'type': 'photo'
        }
        req = requests.get(self.url + 'likes.getList', params={**self.params, **likes_params}).json()
        pprint(req)

    def profile_photos(self):
        profile_photos_params = {
            'album_id': 'profile'
        }
        profile_photos = requests.get(self.url + 'photos.get', params={**self.params, **profile_photos_params} ).json()
        sizes_list = profile_photos['response']['items']
        pprint(sizes_list)

        profile_photos_urls = []
        for photo in sizes_list:
            types = []
            for size in photo['sizes']:
                types.append(size['type'])
            print(types)

            for size in photo['sizes']:
                if size['type'] == 'w':
                    # print(size['type'])
                    # print(size['url'])
                    # profile_photos_urls.append(size['url'])
                    photo_data = {'album_id': photo['album_id'],
                                  'has_tags': photo['has_tags'],
                                  'owner_id': photo['owner_id'],
                                  'post_id': photo['post_id'],
                                  'date': photo['date'],
                                  'url': size['url']
                                  }
                    profile_photos_urls.append(photo_data)
                elif size['type'] == max(types):
                    # print(f'we have {max(types)}')
                    # print(size['url'])
                    # profile_photos_urls.append(size['url'])
                    photo_data = {'album_id': photo['album_id'],
                                  'has_tags': photo['has_tags'],
                                  'owner_id': photo['owner_id'],
                                  'post_id': photo['post_id'],
                                  'date': photo['date'],
                                  'url': size['url']
                                  }
                    profile_photos_urls.append(photo_data)
        print()
        return profile_photos_urls

    def wall_photos(self):
        wall_photos_params = {
            'album_id': 'wall'
        }
        wall_photos = requests.get(self.url + 'photos.get', params={**self.params, **wall_photos_params} ).json()
        sizes_list = wall_photos['response']['items']
        # pprint(sizes_list)

        wall_photos_urls = []
        for photo in sizes_list:
            types = []
            for size in photo['sizes']:
                types.append(size['type'])
            # print(types)

            for size in photo['sizes']:
                if size['type'] == 'w':
                    # print(size['type'])
                    # print(size['url'])
                    # wall_photos_urls.append(size['url'])
                    photo_data = {'album_id': photo['album_id'],
                                  'has_tags': photo['has_tags'],
                                  'owner_id': photo['owner_id'],
                                  'post_id': photo['post_id'],
                                  'date': photo['date'],
                                  'url': size['url']
                                  }
                    wall_photos_urls.append(photo_data)
                elif size['type'] == max(types):
                    # print(f'we have {max(types)}')
                    # print(size['url'])
                    # wall_photos_urls.append(size['url'])
                    photo_data = {'album_id': photo['album_id'],
                                  'has_tags': photo['has_tags'],
                                  'owner_id': photo['owner_id'],
                                  'post_id': photo['post_id'],
                                  'date': photo['date'],
                                  'url': size['url']
                                  }
                    wall_photos_urls.append(photo_data)
        print()
        return wall_photos_urls

    def saved_photos(self):
        saved_photos_params = {
            'album_id': 'saved'
        }
        saved_photos = requests.get(self.url + 'photos.get', params={**self.params, **saved_photos_params} ).json()
        sizes_list = saved_photos['response']['items']
        # pprint(sizes_list)
        # pprint(saved_photos)
        print(len(sizes_list))

        saved_photos_urls = []
        for photo in sizes_list:
            types = []
            for size in photo['sizes']:
                types.append(size['type'])
            # print(types)

            for size in photo['sizes']:
                if size['type'] == 'w':
                    # print(size['type'])
                    # print(size['url'])
                    # saved_photos.append(size['url'])
                    photo_data = {'album_id': photo['album_id'],
                                  'has_tags': photo['has_tags'],
                                  'owner_id': photo['owner_id'],
                                  'post_id': photo['id'],
                                  'date': photo['date'],
                                  'url': size['url']
                                  }
                    saved_photos_urls.append(photo_data)
                elif size['type'] == max(types):
                    # print(f'we have {max(types)}')
                    # print(size['url'])
                    # saved_photos.append(size['url'])
                    photo_data = {'album_id': photo['album_id'],
                                  'has_tags': photo['has_tags'],
                                  'owner_id': photo['owner_id'],
                                  'post_id': photo['id'],
                                  'date': photo['date'],
                                  'url': size['url']
                                  }
                    saved_photos_urls.append(photo_data)
        print()
        # pprint(saved_photos_urls)
        return saved_photos_urls

    def one_photos_list(self):
        all_urls = []
        all_urls.extend(self.profile_photos())
        all_urls.extend(self.wall_photos())
        all_urls.extend(self.saved_photos())

        return all_urls

    def downloading(self):
        os.mkdir('reserve_copy')
        photos = self.one_photos_list()
        pprint(photos)
        print(len(photos))
        global filenames
        filenames = []
        for picture in photos:
            pprint(picture)
            r = requests.get(picture['url'])
            with open(f'reserve_copy/{picture["date"]}.jpg', 'wb') as file:
                file.write(r.content)
                filename = f'{picture["date"]}.jpg'
                filenames.append(filename)

        return filenames


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
        # pprint(response.json())

    def _get_upload_link(self, disk_file_path):
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        headers = self.get_headers()
        params = {"path": disk_file_path, "overwrite": "true"}
        response = requests.get(upload_url, headers=headers, params=params)
        # pprint(response.json())
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

vk_token = ""
token = ''

a = Launcher(vk_token, token)
a.new_folder()