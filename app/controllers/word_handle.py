from copy import deepcopy
import random


class MyWord(object):
    def __init__(self):
        self.word_list = list()
        self.word_list_tmp = list()

    def set_word_list(self, file_path):
        with open(file_path, 'r') as file:
            self.word_list = file.readlines()

        self.word_list = [x.replace('\n', '').replace('\r', '').strip()
                          for x in self.word_list]
        self.reset_word_list()

    def reset_word_list(self):
        self.word_list_tmp = deepcopy(self.word_list)

    def get_random_word(self):
        if not len(self.word_list):
            return ''

        if not self.word_list_tmp:
            self.word_list_tmp = deepcopy(self.word_list)

        word = random.choice(self.word_list_tmp)
        self.word_list_tmp.remove(word)
        return word

    def get_number_loaded(self):
        return len(self.word_list) - len(self.word_list_tmp)