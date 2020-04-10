from common.constant import TRANSLATE_URL
import requests
import os


def get_sound_of_word(path_root, my_word):
    path_file = ''
    try:
        headers = {'user-agent': 'Mozilla'}
        resp = requests.get(TRANSLATE_URL.format(word=my_word.upper()), headers=headers)
        temporary_folder = path_root + '/' + 'temporary'
        not os.path.isdir(temporary_folder) and os.makedirs(temporary_folder)
        path_file = temporary_folder + '/' + 'file.mp3'
        with open(path_file, 'wb+') as file:
            file.write(resp.content)
    except (Exception,):
        pass

    return path_file
