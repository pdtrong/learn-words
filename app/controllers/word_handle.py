from common.constant import ChoiceMode
from copy import deepcopy
from api.google_translate import get_sound_of_word
import random


class MyWord(object):
    def __init__(self, parent):
        self.parent = parent
        self.word_list = list()
        self.choice_mode = ChoiceMode.RANDOM

        self.current_index = 0
        self.word_list_tmp = list()

    def set_word_list(self, file_path):
        with open(file_path, 'r') as file:
            tmp_word_list = file.readlines()
        tmp_word_list = [x.replace('\n', '').replace('\r', '').strip() for x in tmp_word_list]
        tmp_word_list = [x for x in tmp_word_list if x]

        for word in tmp_word_list:
            file_sound_path = get_sound_of_word(self.parent.path_root, word.split(' ')[0])
            self.word_list.append({
                'word': word,
                'file_sound_path': file_sound_path
            })

        self.reset_word_list()

    def reset_word_list(self):
        if self.choice_mode == ChoiceMode.RANDOM:
            self.word_list_tmp = deepcopy(self.word_list)
        elif self.choice_mode == ChoiceMode.ORDER:
            self.current_index = 0

    def set_choice_mode(self, mode):
        self.choice_mode = mode
        self.reset_word_list()

    def get_choice_mode(self):
        return self.choice_mode

    def get_word(self):
        data = {'word': ''}
        if not len(self.word_list):
            return data
        if self.choice_mode == ChoiceMode.RANDOM:
            self.word_list_tmp = self.word_list_tmp or deepcopy(self.word_list)
            data = random.choice(self.word_list_tmp)
            self.word_list_tmp.remove(data)
        elif self.choice_mode == ChoiceMode.ORDER:
            self.current_index = self.current_index if self.current_index < len(self.word_list) else 0
            data = self.word_list[self.current_index]
            self.current_index += 1
        return data

    def get_number_loaded(self):
        number_loaded = 0
        if self.choice_mode == ChoiceMode.RANDOM:
            number_loaded = len(self.word_list) - len(self.word_list_tmp)
        elif self.choice_mode == ChoiceMode.ORDER:
            number_loaded = self.current_index
        return number_loaded

    def get_len_words(self):
        return len(self.word_list)
