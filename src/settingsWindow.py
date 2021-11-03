# -*- coding: utf-8 -*-
import sys

from PyQt5.QtWidgets import *
from SettingsWin_ui import Ui_Dialog


class SettingsWin(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super().__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.setFixedSize(520, 439)
        self.SaveButtons.buttonClicked.connect(self.SButts)
        # self.ok_exit.clicked.connect(self.accept)

    def SButts(self, butt):
        if butt.text() == "Применить":
            print("Applied")  # DEBUG
        elif butt.text() == "Ок":
            self.SButts(self.apply)
            self.accept()
        elif "пресет" in butt.text():
            print("Saved")  # DEBUG


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = SettingsWin()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())