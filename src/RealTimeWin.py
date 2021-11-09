import sys

from PyQt5.QtWidgets import *
from RtWin_ui import Ui_Dialog


class RtWin(QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        pass


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = RtWin()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())