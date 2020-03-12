from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from util.repeat_timer import RepeatedTimer
from controllers.word_handle import MyWord
import os
import sys
import ctypes


class MainWindow(QMainWindow):
    trigger_update_stay_on_top = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.trigger_update_stay_on_top.connect(self.update_stay_op_top)

        self.wg_my_app = MyApp(parent=self)
        self.setCentralWidget(self.wg_my_app)

        self.menu_bar = self.menuBar()
        option = self.menu_bar.addMenu('Option')

        qa_stay_on_top = QAction('Stay on top', self, checkable=True)
        qa_stay_on_top.setChecked(True)
        qa_stay_on_top.triggered.connect(self.stay_on_top_toggle)

        option.addAction(qa_stay_on_top)

    def stay_on_top_toggle(self, state):
        self.trigger_update_stay_on_top.emit({'state': state})

    @pyqtSlot(dict)
    def update_stay_op_top(self, result):
        if result['state']:
            self.setWindowFlags(Qt.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(Qt.Window)
        self.show()

    def close_app(self):
        self.wg_my_app.my_repeat_timer and self.wg_my_app.my_repeat_timer.stop()
        print('closed app')


class MyApp(QWidget):

    # Setup Signal
    trigger_update_word = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        # ------------------------------------------------------------
        self.trigger_update_word.connect(self.update_printing_word)

        # ------------------------------------------------------------
        self.lbl_print_word = QLabel()
        self.lbl_print_word.setText('Hello World!!!')
        self.lbl_print_word.setFont(QFont('Arial', 24, QFont.Bold))
        self.lbl_print_word.setAlignment(Qt.AlignCenter)

        self.btn_import_word = QPushButton()
        self.btn_import_word.setText('Import')
        self.btn_import_word.clicked.connect(self.import_word_list)

        self.btn_print_word = QPushButton()
        self.btn_print_word.setText('Print')

        self.pb_loaded_word = QProgressBar(self)
        self.pb_loaded_word.setValue(0)
        self.pb_loaded_word.setMaximum(100)

        # ------------------------------------------------------------
        layout = QGridLayout(self)
        param = [self.lbl_print_word, 0, 0, 1, 2]
        layout.addWidget(*param)
        param = [self.btn_import_word, 1, 0, 1, 2]
        layout.addWidget(*param)
        # param = [self.btn_print_word, 1, 1]
        # layout.addWidget(*param)
        param = [self.pb_loaded_word, 2, 0, 1, 2]
        layout.addWidget(*param)

        # ------------------------------------------------------------
        self.setLayout(layout)
        self.setWindowTitle('Words')

        # ------------------------------------------------------------
        self.my_word = MyWord()
        self.my_repeat_timer = None
        self.start_timer()

    # ------------------------------------------------------------
    @pyqtSlot()
    def import_word_list(self):
        file_info = QFileDialog.getOpenFileName()
        if not file_info[0]:
            return
        self.my_word.set_word_list(file_info[0])
        self.pb_loaded_word.setMaximum(len(self.my_word.word_list))

    def start_timer(self):
        self.my_repeat_timer = RepeatedTimer(1, self.fire_trigger_update_word)
        self.my_repeat_timer.start()

    # ------------------------------------------------------------
    def fire_trigger_update_word(self):
        self.trigger_update_word.emit({})

    @pyqtSlot(dict)
    def update_printing_word(self, ignore_input):
        word = self.my_word.get_random_word()
        if not word:
            self.lbl_print_word.setText('Import word list')
        else:
            self.lbl_print_word.setText(word)
            self.pb_loaded_word.setValue(self.my_word.get_number_loaded())


if __name__ == '__main__':
    # ------------------------------------------------------------
    # Add app id
    my_app_id = 'Words-Learn-Application'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(my_app_id)

    # ------------------------------------------------------------
    # Create object
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    app.setWindowIcon(QIcon(os.getcwd() + '/logo.ico'))

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
