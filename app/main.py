from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from util.repeat_timer import RepeatedTimer
from controllers.word_handle import MyWord
from util.logging_custom import logging
from common.constant import ChoiceMode
from common.stylesheet import StyleSheetProgressBar
import os
import sys
import ctypes


if hasattr(sys, '_MEIPASS'):
    logging.info('Running in a PyInstaller bundle')
else:
    logging.info('Running in a Python process')

DEFAULT_STR = '¯\_(ツ)_/¯'


class WindowFlagsObject(object):
    def __init__(self):
        self.flags = set()

    def enable_flag(self, flag):
        self.flags.add(flag)

    def remove_flag(self, flag):
        self.flags.remove(flag)

    def get_flags(self):
        flags_value = Qt.Window
        for i in self.flags:
            flags_value |= i
        return flags_value


class MainWindow(QMainWindow):
    trigger_window_stay_on_top = pyqtSignal(dict)
    trigger_file_import_words = pyqtSignal(dict)
    trigger_help_about = pyqtSignal(dict)
    trigger_edit_adjust_timer = pyqtSignal(dict)
    trigger_choice_random = pyqtSignal(dict)
    trigger_choice_order = pyqtSignal(dict)
    trigger_view_current_section = pyqtSignal(dict)
    trigger_view_hide = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent, Qt.WindowFlags())

        # ------------------------------------------------------------
        self.submenu_choice = dict()
        self.window_flags_object = WindowFlagsObject()

        # ------------------------------------------------------------
        self.wg_my_app = MyApp(parent=self)

        height, width = 60, 250
        center_point = QDesktopWidget().availableGeometry().center()

        self.setGeometry(int(center_point.x() - width / 2), int(center_point.y() - height / 2), width, height)
        self.setCentralWidget(self.wg_my_app)
        self.setWindowTitle('Learn words')

        # ------------------------------------------------------------
        self.trigger_window_stay_on_top.connect(self.stay_op_top_event)
        self.trigger_file_import_words.connect(self.wg_my_app.import_words_event)
        self.trigger_help_about.connect(self.about_event)
        self.trigger_edit_adjust_timer.connect(self.adjust_timer_event)
        self.trigger_choice_random.connect(self.choice_word_event)
        self.trigger_choice_order.connect(self.choice_word_event)
        self.trigger_view_current_section.connect(self.current_section_event)
        self.trigger_view_hide.connect(self.view_hide_event)

        # ------------------------------------------------------------
        self.menu_bar = self.menuBar()

        # ------------------------------------------------------------
        # File
        mb_file = self.menu_bar.addMenu('File')

        # # Import words
        qa_import_word_list = QAction('Import words', self)
        qa_import_word_list.triggered.connect(lambda ign: self.trigger_file_import_words.emit({}))
        mb_file.addAction(qa_import_word_list)

        # ------------------------------------------------------------
        # Edit
        mb_edit = self.menu_bar.addMenu('Edit')

        # # Adjust timer
        qa_setup_timer = QAction('Adjust timer', self)
        qa_setup_timer.triggered.connect(lambda ign: self.trigger_edit_adjust_timer.emit({}))

        # # Choice
        mn_choice_word = QMenu('Choice', self)

        # # # Random
        qa_choice_random_name = ChoiceMode.RANDOM
        qa_choice_random = QAction(qa_choice_random_name, self, checkable=True)
        qa_choice_random.setChecked(True)
        qa_choice_random.triggered.connect(lambda ign: self.trigger_choice_random.emit({'name': qa_choice_random_name}))
        mn_choice_word.addAction(qa_choice_random)
        self.submenu_choice[qa_choice_random_name] = qa_choice_random

        # # # Order
        qa_choice_order_name = ChoiceMode.ORDER
        qa_choice_order = QAction(qa_choice_order_name, self, checkable=True)
        qa_choice_order.setChecked(False)
        qa_choice_order.triggered.connect(lambda ign: self.trigger_choice_order.emit({'name': qa_choice_order_name}))
        mn_choice_word.addAction(qa_choice_order)
        self.submenu_choice[qa_choice_order_name] = qa_choice_order

        mb_edit.addAction(qa_setup_timer)
        mb_edit.addMenu(mn_choice_word)

        # ------------------------------------------------------------
        # View
        mb_view = self.menu_bar.addMenu('View')
        qa_current_section = QAction('Current section', self)
        qa_current_section.triggered.connect(lambda ign: self.trigger_view_current_section.emit({}))
        qa_hide = QAction('Hide', self, checkable=True)
        qa_hide.setChecked(False)
        qa_hide.triggered.connect(lambda state: self.trigger_view_hide.emit({'state': state}))
        mb_view.addAction(qa_current_section)
        mb_view.addAction(qa_hide)

        # ------------------------------------------------------------
        # Window
        mb_window = self.menu_bar.addMenu('Window')

        # # Stay on top
        qa_stay_on_top = QAction('Stay on top', self, checkable=True)
        qa_stay_on_top.setChecked(False)
        qa_stay_on_top.triggered.connect(lambda state: self.trigger_window_stay_on_top.emit({'state': state}))
        mb_window.addAction(qa_stay_on_top)

        # ------------------------------------------------------------
        # Help
        mb_help = self.menu_bar.addMenu('Help')

        # # About
        qa_print_about = QAction('About', self)
        qa_print_about.triggered.connect(lambda ign: self.trigger_help_about.emit({}))
        mb_help.addAction(qa_print_about)

    @pyqtSlot(dict)
    def stay_op_top_event(self, result):
        if result['state']:
            self.window_flags_object.enable_flag(Qt.WindowStaysOnTopHint)
        else:
            self.window_flags_object.remove_flag(Qt.WindowStaysOnTopHint)
        self.setWindowFlags(self.window_flags_object.get_flags())
        self.show()

    @pyqtSlot(dict)
    def adjust_timer_event(self):
        parameter = [self, 'Input Dialog', 'Enter timer (current = {}):'.format(self.wg_my_app.delay),
                     3, 1, 100, 1, Qt.WindowFlags()]
        timer_value, done = QInputDialog.getInt(*parameter)
        if done and timer_value:
            self.wg_my_app.delay = int(timer_value)
            self.wg_my_app.my_word.get_len_words() and self.wg_my_app.start_timer()

    @pyqtSlot(dict)
    def about_event(self):
        about_me = '''
        Duc Trong Pham
        pdtrong.dev@gmail.com
        '''
        parameter = [self, 'About', about_me]
        QMessageBox.about(*parameter)

    @pyqtSlot(dict)
    def choice_word_event(self, result):
        [self.submenu_choice[x].setChecked(result['name'] == x) for x in self.submenu_choice.keys()]
        self.wg_my_app.my_word.set_choice_mode(result['name'])

    @pyqtSlot(dict)
    def current_section_event(self):
        current_section_info = '{}\n{} word(s)\n{} loaded\n{}(s) delay\n{} mode'
        current_section_info = current_section_info.format(self.wg_my_app.current_file,
                                                           self.wg_my_app.my_word.get_len_words(),
                                                           self.wg_my_app.my_word.get_number_loaded(),
                                                           self.wg_my_app.delay,
                                                           self.wg_my_app.my_word.get_choice_mode())
        parameter = [self, 'Current section', current_section_info]
        QMessageBox.about(*parameter)

    @pyqtSlot(dict)
    def view_hide_event(self, result):
        if result['state']:
            self.window_flags_object.enable_flag(Qt.FramelessWindowHint)
        else:
            self.window_flags_object.remove_flag(Qt.FramelessWindowHint)
        self.wg_my_app.pb_loaded_word.setTextVisible(not result['state'])
        self.setWindowFlags(self.window_flags_object.get_flags())
        self.show()

    def enterEvent(self, event):
        self.menu_bar.show()
        return super(MainWindow, self).enterEvent(event)

    def leaveEvent(self, event):
        self.menu_bar.hide()
        return super(MainWindow, self).leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.offset = event.pos()
        else:
            super(MainWindow).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.offset is not None and event.buttons() == Qt.LeftButton:
            self.move(self.pos() + event.pos() - self.offset)
        else:
            super(MainWindow).mouseMoveEvent(event)

    def close_app(self):
        self.wg_my_app.my_repeat_timer and self.wg_my_app.my_repeat_timer.stop()
        logging.info('Closed app ╮（╯＿╰）╭')


class MyApp(QWidget):
    # Setup Signal
    trigger_update_word = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent, Qt.WindowFlags())
        self.delay = 3
        self.current_file = 'Unknown'

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
    path_icon = get_root_folder() + '/store/logo.ico'
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