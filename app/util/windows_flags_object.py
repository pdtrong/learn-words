from PyQt5.QtCore import *


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
