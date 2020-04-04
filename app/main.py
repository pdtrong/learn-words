from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from util.logging_custom import logging
from builders.my_widget import MyWidget
from builders.my_menu_bar import MyMenuBar
import os
import sys
import ctypes


if hasattr(sys, '_MEIPASS'):
    logging.info('Running in a PyInstaller bundle')
else:
    logging.info('Running in a Python process')


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent, Qt.WindowFlags())

        self.is_hide_menu_bar = False
        self.path_root = get_root_folder()

        # ------------------------------------------------------------
        height, width = 60, 250
        center_point = QDesktopWidget().availableGeometry().center()
        self.setGeometry(int(center_point.x() - width / 2), int(center_point.y() - height / 2), width, height)
        self.setWindowTitle('Learn words')

        # ------------------------------------------------------------
        self.wg_my_app = MyWidget(parent=self)
        self.setCentralWidget(self.wg_my_app)

        # ------------------------------------------------------------
        self.menu_bar = MyMenuBar(self)
        self.setMenuWidget(self.menu_bar)

    def enterEvent(self, event):
        self.is_hide_menu_bar and self.menu_bar.setVisible(True)
        return super(MainWindow, self).enterEvent(event)

    def leaveEvent(self, event):
        self.is_hide_menu_bar and self.menu_bar.setVisible(False)
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