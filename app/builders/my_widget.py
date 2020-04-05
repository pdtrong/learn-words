from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from util.repeat_timer import RepeatedTimer
from controllers.word_handle import MyWord
from common.constant import DEFAULT_STR
from common.stylesheet import StyleSheetProgressBar
from workers.worker import Worker
from api.google_translate import get_sound_of_word
from controllers.vlc_app import media_player

import os


class MyWidget(QWidget):
    # Setup Signal
    trigger_update_word = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent, Qt.WindowFlags())
        self.parent = parent
        self.delay = 3
        self.current_file = 'Unknown'
        self.thread_pool = QThreadPool()

        # ------------------------------------------------------------
        self.trigger_update_word.connect(self.update_printing_word)

        # ------------------------------------------------------------
        self.lbl_print_word = QLabel()
        self.lbl_print_word.setText(DEFAULT_STR)
        self.lbl_print_word.setFont(QFont('Arial', 10, QFont.Bold))
        self.lbl_print_word.setAlignment(Qt.AlignCenter)

        self.pb_loaded_word = QProgressBar(self)
        self.pb_loaded_word.setValue(0)
        self.pb_loaded_word.setMaximum(100)
        self.pb_loaded_word.setStyleSheet(StyleSheetProgressBar)

        # ------------------------------------------------------------
        layout = QGridLayout(self)
        param = [self.lbl_print_word, 0, 0, 1, 4]
        layout.addWidget(*param)
        param = [self.pb_loaded_word, 1, 0, 1, 4]
        layout.addWidget(*param)
        # ------------------------------------------------------------
        self.setLayout(layout)
        self.setWindowTitle('Words')

        # ------------------------------------------------------------
        self.my_word = MyWord()
        self.my_repeat_timer = None

    # ------------------------------------------------------------
    @pyqtSlot()
    def import_words_event(self):
        parameter = [self]
        file_info = QFileDialog.getOpenFileName(*parameter)
        if not file_info or not file_info[0]:
            return None
        file_path = file_info[0]
        self.current_file = os.path.basename(file_path)
        self.my_word.set_word_list(file_path)
        self.pb_loaded_word.setMaximum(self.my_word.get_len_words())

        self.my_word.get_len_words() and self.start_timer()

    def start_timer(self):
        self.my_repeat_timer and self.my_repeat_timer.stop()
        self.my_repeat_timer = RepeatedTimer(self.delay, self.trigger_update_word.emit, {})
        self.my_repeat_timer.start()

    def stop_timer(self):
        self.my_repeat_timer and self.my_repeat_timer.stop()
        self.my_repeat_timer = None

    # ------------------------------------------------------------
    @pyqtSlot(dict)
    def update_printing_word(self):
        word = self.my_word.get_word()
        if not word:
            self.lbl_print_word.setText(DEFAULT_STR)
        else:
            self.lbl_print_word.setText(word)
            self.pb_loaded_word.setValue(self.my_word.get_number_loaded())

            # play sound of word
            worker = Worker(self.play_sound_of_word, word.split(' ')[0])
            self.thread_pool.start(worker)

    # ------------------------------------------------------------
    def play_sound_of_word(self, word):
        file_path = get_sound_of_word(self.parent.path_root, word)
        if not file_path:
            return None
        media_player(file_path)
