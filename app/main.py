from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from util.repeat_timer import RepeatedTimer
from controllers.word_handle import MyWord
from util.logging_custom import logging

import os
import sys
import ctypes


if hasattr(sys, '_MEIPASS'):
    logging.info('running in a PyInstaller bundle')
else:
    logging.info('running in a normal Python process')

DEFAULT_STR = '¯\_(ツ)_/¯'


class MainWindow(QMainWindow):
    trigger_update_stay_on_top = pyqtSignal(dict)
    trigger_update_word_list = pyqtSignal(dict)
    trigger_print_about = pyqtSignal(dict)
    trigger_setup_timer = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent, Qt.WindowFlags())
        self.setWindowTitle('Learn words')

        # ------------------------------------------------------------
        self.wg_my_app = MyApp(parent=self)
        self.setCentralWidget(self.wg_my_app)

        height, width = 200, 400
        center_point = QDesktopWidget().availableGeometry().center()
        self.setGeometry(int(center_point.x() - width / 2), int(center_point.y() - height / 2), width, height)

        # ------------------------------------------------------------
        self.trigger_update_stay_on_top.connect(self.update_stay_op_top_event)
        self.trigger_update_word_list.connect(self.wg_my_app.import_word_list_event)
        self.trigger_print_about.connect(self.print_about_event)
        self.trigger_setup_timer.connect(self.setup_timer_event)

        # ------------------------------------------------------------
        self.menu_bar = self.menuBar()
        mb_file = self.menu_bar.addMenu('File')
        qa_import_word_list = QAction('Import words', self)
        qa_import_word_list.triggered.connect(self.import_word_list_toggle)
        mb_file.addAction(qa_import_word_list)

        mb_edit = self.menu_bar.addMenu('Edit')
        qa_setup_timer = QAction('Adjust timer', self)
        qa_setup_timer.triggered.connect(self.setup_timer_toggle)
        mb_edit.addAction(qa_setup_timer)

        mb_window = self.menu_bar.addMenu('Window')
        qa_stay_on_top = QAction('Stay on top', self, checkable=True)
        qa_stay_on_top.setChecked(False)
        qa_stay_on_top.triggered.connect(self.stay_on_top_toggle)
        mb_window.addAction(qa_stay_on_top)

        mb_help = self.menu_bar.addMenu('Help')
        qa_print_about = QAction('About', self)
        qa_print_about.triggered.connect(self.print_about_toggle)
        mb_help.addAction(qa_print_about)

    def import_word_list_toggle(self):
        self.trigger_update_word_list.emit({})

    def stay_on_top_toggle(self, state):
        self.trigger_update_stay_on_top.emit({'state': state})

    @pyqtSlot(dict)
    def update_stay_op_top_event(self, result):
        if result['state']:
            self.setWindowFlags(Qt.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(Qt.Window)
        self.show()

    def setup_timer_toggle(self):
        self.trigger_setup_timer.emit({})

    @pyqtSlot(dict)
    def setup_timer_event(self):
        parameter = [self, 'Input Dialog', 'Enter timer (current = {}):'.format(self.wg_my_app.delay),
                     5, 1, 100, 1, Qt.WindowFlags()]
        timer_value, done = QInputDialog.getInt(*parameter)
        if done and timer_value:
            self.wg_my_app.delay = int(timer_value)
            self.wg_my_app.my_word.word_list and self.wg_my_app.start_timer()

    def print_about_toggle(self):
        self.trigger_print_about.emit({})

    @pyqtSlot(dict)
    def print_about_event(self):
        about_me = '''
        Duc Trong Pham
        pdtrong.dev@gmail.com
        '''
        parameter = [self, 'About', about_me]
        QMessageBox.about(*parameter)

    def close_app(self):
        self.wg_my_app.my_repeat_timer and self.wg_my_app.my_repeat_timer.stop()
        logging.info('Closed app ╮（╯＿╰）╭')


class MyApp(QWidget):
    # Setup Signal
    trigger_update_word = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent, Qt.WindowFlags())

        self.delay = 3

        # ------------------------------------------------------------
        self.trigger_update_word.connect(self.update_printing_word)

        # ------------------------------------------------------------
        self.lbl_print_word = QLabel()
        self.lbl_print_word.setText(DEFAULT_STR)
        self.lbl_print_word.setFont(QFont('Arial', 24, QFont.Bold))
        self.lbl_print_word.setAlignment(Qt.AlignCenter)

        self.pb_loaded_word = QProgressBar(self)
        self.pb_loaded_word.setValue(0)
        self.pb_loaded_word.setMaximum(100)

        # ------------------------------------------------------------
        layout = QGridLayout(self)
        param = [self.lbl_print_word, 0, 0, 1, 2]
        layout.addWidget(*param)
        param = [self.pb_loaded_word, 1, 0, 1, 2]
        layout.addWidget(*param)

        # ------------------------------------------------------------
        self.setLayout(layout)
        self.setWindowTitle('Words')

        # ------------------------------------------------------------
        self.my_word = MyWord()
        self.my_repeat_timer = None

    # ------------------------------------------------------------
    @pyqtSlot()
    def import_word_list_event(self):
        parameter = [self]
        file_info = QFileDialog.getOpenFileName(*parameter)
        if not file_info or not file_info[0]:
            return None

        self.my_word.set_word_list(file_info[0])
        self.pb_loaded_word.setMaximum(len(self.my_word.word_list))

        self.my_word.word_list and self.start_timer()

    def start_timer(self):
        self.my_repeat_timer and self.my_repeat_timer.stop()
        self.my_repeat_timer = RepeatedTimer(self.delay, self.fire_trigger_update_word)
        self.my_repeat_timer.start()

    def stop_timer(self):
        self.my_repeat_timer and self.my_repeat_timer.stop()
        self.my_repeat_timer = None

    # ------------------------------------------------------------
    def fire_trigger_update_word(self):
        self.trigger_update_word.emit({})

    @pyqtSlot(dict)
    def update_printing_word(self):
        word = self.my_word.get_random_word()
        if not word:
            self.lbl_print_word.setText(DEFAULT_STR)
        else:
            self.lbl_print_word.setText(word)
            self.pb_loaded_word.setValue(self.my_word.get_number_loaded())

def get_root_folder():
    root_main_path = os.path.abspath(sys.modules['__main__'].__file__)
    root_folder = os.path.dirname(root_main_path)
    return root_folder

if __name__ == '__main__':
    # ------------------------------------------------------------
    # Add app id
    my_app_id = 'Words-Learn-Application'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(my_app_id)

    # ------------------------------------------------------------
    # Create object
    path_icon = get_root_folder() + '/logo.ico'
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    app.setWindowIcon(QIcon(path_icon))

    # ------------------------------------------------------------
    # Now use a palette to switch to dark colors:
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(palette)

    # ------------------------------------------------------------
    my_app = MainWindow()
    my_app.show()

    # ------------------------------------------------------------
    # Handle event quit
    app.aboutToQuit.connect(my_app.close_app)
    sys.exit(app.exec_())