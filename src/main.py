# -*- coding: utf-8 -*-
import sys

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from MainWin_ui import Ui_MainWindow
from settingsWindow import SettingsWin
import sqlite3


class MainWin(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.conn = sqlite3.connect('./databases/presets.sqlite')
        cur = self.conn.cursor()
        self.setFixedSize(707, 495)
        logo_pm = QPixmap(*cur.execute("SELECT logo FROM presets WHERE id = 1").fetchone())
        logo = QLabel(self)
        logo.move(15, 0)
        logo.resize(300, 300)
        logo.setPixmap(logo_pm)
        self.Actions.buttonClicked.connect(self.actionsButt)

    def actionsButt(self, butt):
        if butt.text() == "Настройки":
            dial = SettingsWin()
            dial.exec()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MainWin()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())


# C:\Users\barst\PycharmProjects\YaLc_Project\gui\MainWin.ui