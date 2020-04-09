from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from common.constant import ChoiceMode, HideMode
from util.windows_flags_object import WindowFlagsObject


class MyMenuBar(QMenuBar):
    trigger_window_stay_on_top = pyqtSignal(dict)
    trigger_file_import_words = pyqtSignal(dict)
    trigger_help_about = pyqtSignal(dict)
    trigger_edit_size_text = pyqtSignal(dict)
    trigger_edit_adjust_timer = pyqtSignal(dict)
    trigger_choice_random = pyqtSignal(dict)
    trigger_choice_order = pyqtSignal(dict)
    trigger_view_current_section = pyqtSignal(dict)
    trigger_view_hide = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

        self.submenu_choice = dict()
        self.window_flags_object = WindowFlagsObject()

        self.trigger_window_stay_on_top.connect(self.stay_op_top_event)
        self.trigger_file_import_words.connect(self.parent.wg_my_app.import_words_event)
        self.trigger_help_about.connect(self.about_event)
        self.trigger_edit_size_text.connect(self.change_size_text)
        self.trigger_edit_adjust_timer.connect(self.adjust_timer_event)
        self.trigger_choice_random.connect(self.choice_word_event)
        self.trigger_choice_order.connect(self.choice_word_event)
        self.trigger_view_current_section.connect(self.current_section_event)
        self.trigger_view_hide.connect(self.view_hide_event)

        # ------------------------------------------------------------
        # File
        mb_file = self.addMenu('File')

        # # Import words
        qa_import_word_list = QAction('Import words', self)
        qa_import_word_list.triggered.connect(lambda ign: self.trigger_file_import_words.emit({}))
        mb_file.addAction(qa_import_word_list)

        # ------------------------------------------------------------
        # Edit
        mb_edit = self.addMenu('Edit')

        # # Adjust timer
        qa_change_size_text = QAction('Change size text', self)
        qa_change_size_text.triggered.connect(lambda ign: self.trigger_edit_size_text.emit({}))

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

        mb_edit.addAction(qa_change_size_text)
        mb_edit.addAction(qa_setup_timer)
        mb_edit.addMenu(mn_choice_word)

        # ------------------------------------------------------------
        # View
        mb_view = self.addMenu('View')
        qa_current_section = QAction('Current section', self)
        qa_current_section.triggered.connect(lambda ign: self.trigger_view_current_section.emit({}))

        mn_hide = QMenu('Hide', self)

        qa_hide_title_name = HideMode.TITLE_BAR
        qa_hide_title = QAction(qa_hide_title_name, self, checkable=True)
        qa_hide_title.setChecked(False)
        qa_hide_title.triggered.connect(lambda state: self.trigger_view_hide.emit({'name': qa_hide_title_name,
                                                                                   'state': state}))
        mn_hide.addAction(qa_hide_title)

        qa_hide_menu_name = HideMode.MENU_BAR
        qa_hide_menu = QAction(qa_hide_menu_name, self, checkable=True)
        qa_hide_menu.setChecked(False)
        qa_hide_menu.triggered.connect(lambda state: self.trigger_view_hide.emit({'name': qa_hide_menu_name,
                                                                                  'state': state}))
        mn_hide.addAction(qa_hide_menu)

        qa_hide_ipa_name = HideMode.IPA_WORD
        qa_hide_ipa = QAction(qa_hide_ipa_name, self, checkable=True)
        qa_hide_ipa.setChecked(False)
        qa_hide_ipa.triggered.connect(lambda state: self.trigger_view_hide.emit({'name': qa_hide_ipa_name,
                                                                                 'state': state}))
        mn_hide.addAction(qa_hide_ipa)

        mb_view.addAction(qa_current_section)
        mb_view.addMenu(mn_hide)

        # ------------------------------------------------------------
        # Window
        mb_window = self.addMenu('Window')

        # # Stay on top
        qa_stay_on_top = QAction('Stay on top', self, checkable=True)
        qa_stay_on_top.setChecked(False)
        qa_stay_on_top.triggered.connect(lambda state: self.trigger_window_stay_on_top.emit({'state': state}))
        mb_window.addAction(qa_stay_on_top)

        # ------------------------------------------------------------
        # Help
        mb_help = self.addMenu('Help')

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
        self.parent.setWindowFlags(self.window_flags_object.get_flags())
        self.parent.show()

    @pyqtSlot(dict)
    def adjust_timer_event(self):
        parameter = [self.parent, 'Input Dialog', 'Enter timer (current = {}):'.format(self.parent.wg_my_app.delay),
                     3, 1, 100, 1, Qt.WindowFlags()]
        timer_value, done = QInputDialog.getInt(*parameter)
        if done and timer_value:
            self.parent.wg_my_app.delay = int(timer_value)
            self.parent.wg_my_app.my_word.get_len_words() and self.parent.wg_my_app.start_timer()

    @pyqtSlot(dict)
    def change_size_text(self):
        parameter = [self.parent, 'Input Dialog', 'Enter size text :',
                     20, 1, 100, 1, Qt.WindowFlags()]
        size_value, done = QInputDialog.getInt(*parameter)
        if done and size_value:
            self.parent.wg_my_app.lbl_print_word.setFont(QFont('Arial', int(size_value), QFont.Bold))
            self.parent.wg_my_app.lbl_print_ipa.setFont(QFont('Arial', int(size_value / 2), QFont.Bold))

    @pyqtSlot(dict)
    def about_event(self):
        about_me = '''
        Duc Trong Pham
        pdtrong.dev@gmail.com
        '''
        parameter = [self.parent, 'About', about_me]
        QMessageBox.about(*parameter)

    @pyqtSlot(dict)
    def choice_word_event(self, result):
        [self.submenu_choice[x].setChecked(result['name'] == x) for x in self.submenu_choice.keys()]
        self.parent.wg_my_app.my_word.set_choice_mode(result['name'])

    @pyqtSlot(dict)
    def current_section_event(self):
        current_section_info = '{}\n{} word(s)\n{} loaded\n{}(s) delay\n{} mode'
        current_section_info = current_section_info.format(self.parent.wg_my_app.current_file,
                                                           self.parent.wg_my_app.my_word.get_len_words(),
                                                           self.parent.wg_my_app.my_word.get_number_loaded(),
                                                           self.parent.wg_my_app.delay,
                                                           self.parent.wg_my_app.my_word.get_choice_mode())
        parameter = [self.parent, 'Current section', current_section_info]
        QMessageBox.about(*parameter)

    @pyqtSlot(dict)
    def view_hide_event(self, result):
        if result['name'] == HideMode.TITLE_BAR:
            if result['state']:
                self.window_flags_object.enable_flag(Qt.FramelessWindowHint)
            else:
                self.window_flags_object.remove_flag(Qt.FramelessWindowHint)
            self.parent.wg_my_app.pb_loaded_word.setTextVisible(not result['state'])
            self.parent.setWindowFlags(self.window_flags_object.get_flags())
            self.parent.show()
        elif result['name'] == HideMode.MENU_BAR:
            self.parent.is_hide_menu_bar = result['state']
            self.setVisible(not result['state'])
        elif result['name'] == HideMode.IPA_WORD:
            self.parent.wg_my_app.lbl_print_ipa.setVisible(not result['state'])
        else:
            pass
