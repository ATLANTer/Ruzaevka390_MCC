# -*- coding: utf-8 -*-
import sys

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from MainWin_ui import Ui_MainWindow
from settingsWindow import SettingsWin
from EquipWin import EquipWin
from reqst import ReqstWin
from RealTimeWin import RtWin
import sqlite3


class MainWin(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.conn_p = sqlite3.connect('./databases/presets.sqlite')
        self.conn_d = sqlite3.connect('./databases/raw_data.sqlite')
        cur = self.conn_p.cursor()
        self.setFixedSize(707, 495)
        logo_pm = QPixmap(*cur.execute("SELECT logo FROM presets WHERE id = 1").fetchone())
        self.logo = QLabel(self)
        self.logo.move(15, 0)
        self.logo.resize(300, 300)
        self.logo.setPixmap(logo_pm)
        self.Actions.buttonClicked.connect(self.actionsButt)
        self.dates = self.conn_d.execute('SELECT time FROM time_moments').fetchall()
        self.dates = list(map(lambda x: x[0], self.dates))
        self.time_select.addItems(self.dates)
        self.show_data()
        self.time_select.currentTextChanged.connect(self.show_data)

    def actionsButt(self, butt):
        cur = self.conn_p.cursor()
        if butt.text() == "Настройки":
            dial = SettingsWin()
            dial.exec()
            logo_pm = QPixmap(*cur.execute("SELECT logo FROM presets WHERE id = 1").fetchone())
            self.logo.setPixmap(logo_pm)
        elif "на отправку" in butt.text():
            dial = ReqstWin()
            dial.exec()
        elif 'Контроль' in butt.text():
            dial = EquipWin()
            dial.exec()
        elif "time" in butt.text():
            dial = RtWin()
            dial.exec()

    def show_data(self):
        try:
            data = self.conn_d.execute(f"""SELECT latitude, longitude, altitude, rssi FROM data
                                                       WHERE id = (SELECT id FROM time_moments
                                                       WHERE time = '{self.time_select.currentText()}')""").fetchone()
            data_str = f"Latitude: {data[0]}\n" + \
                       f"Longitude: {data[1]}\n" + \
                       f"Altitude: {data[2]}\n" + \
                       f"RSSI: {data[3]}\n"
            self.moment_data.setPlainText(data_str)
        except Exception as exc:
            self.moment_data.setPlainText("No data")


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MainWin()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())



# C:\Users\barst\PycharmProjects\YaLc_Project\gui\MainWin.ui
