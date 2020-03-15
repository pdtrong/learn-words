from common.constant import ChoiceMode
from copy import deepcopy
import random


class MyWord(object):
    def __init__(self):
        self.word_list = list()
        self.choice_mode = ChoiceMode.RANDOM

        self.current_index = 0
        self.word_list_tmp = list()

    def set_word_list(self, file_path):
        with open(file_path, 'r') as file:
            self.word_list = file.readlines()
        self.word_list = [x.replace('\n', '').replace('\r', '').strip()
                          for x in self.word_list]
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
        word = ''
        if not len(self.word_list):
            return word
        if self.choice_mode == ChoiceMode.RANDOM:
            self.word_list_tmp = self.word_list_tmp or deepcopy(self.word_list)
            word = random.choice(self.word_list_tmp)
            self.word_list_tmp.remove(word)
        elif self.choice_mode == ChoiceMode.ORDER:
            self.current_index = self.current_index if self.current_index < len(self.word_list) else 0
            word = self.word_list[self.current_index]
            self.current_index += 1
        return word

    def get_number_loaded(self):
        number_loaded = 0
        if self.choice_mode == ChoiceMode.RANDOM:
            number_loaded = len(self.word_list) - len(self.word_list_tmp)
        elif self.choice_mode == ChoiceMode.ORDER:
            number_loaded = self.current_index
        return number_loaded

    def get_len_words(self):
        return len(self.word_list)
