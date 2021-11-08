import sys

from PyQt5.QtWidgets import *
from  ReqstWin_ui import Ui_Dialog
from serial import Serial
import sqlite3


class MainWin(QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.conn_presets = sqlite3.connect('./databases/presets.sqlite')
        self.conn_data = sqlite3.connect('./databases/raw_data.sqlite')
        self.begin.clicked.connect(self.begin_butt)

    def begin_butt(self):
        cur = self.conn_presets.cursor()
        try:
            ser = Serial(cur.execute("SELECT com FROM presets WHERE id = 1").fetchone(), 9600)
            self.data.setPlainText(self.data.toPlainText() + ser.readline())
        except:
            print("Something wrong")  # DEBUG

    def stop_butt(self):
        pass


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MainWin()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())