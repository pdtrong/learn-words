from app.common.constant import TRANSLATE_URL
import requests
import os


def get_sound_of_word(path_root, my_word):
    headers = {'user-agent': 'Mozilla'}
    resp = requests.get(TRANSLATE_URL.format(word=my_word), headers=headers)
    temporary_folder = path_root + '/' + 'temporary'
    not os.path.isdir(temporary_folder) and os.makedirs(temporary_folder)
    with open(temporary_folder + '/' + 'file.mp3', 'wb+') as file:
        file.write(resp.content)
