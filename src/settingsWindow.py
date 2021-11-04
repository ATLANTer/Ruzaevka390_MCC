# -*- coding: utf-8 -*-
import sys
from help_objs import *
import sqlite3

from PyQt5.QtWidgets import *
from SettingsWin_ui import Ui_Dialog


class SettingsWin(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super().__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.conn = sqlite3.connect("./databases/presets.sqlite")
        self.setFixedSize(520, 439)
        self.SaveButtons.buttonClicked.connect(self.SButts)
        self.com_select.addItems(serial_ports())
        self.modified = dict()
        self.titles = list()
        self.upload_table()
        self.dataView.itemChanged.connect(self.change_item)


    def SButts(self, butt):
        if butt.text() == "Применить":
            self.save_all()
            print("Applied")  # DEBUG
        elif butt.text() == "Ок":
            self.SButts(self.apply)
            self.conn.close()
            self.accept()
        elif "пресет" in butt.text():
            print("Saved")  # DEBUG

    def upload_table(self):
        cur = self.conn.cursor()
        tbl = cur.execute("SELECT * FROM presets").fetchall()
        self.titles = [description[0] for description in cur.description]
        self.dataView.setRowCount(len(tbl) - 1)
        self.dataView.setColumnCount(len(tbl[0]) - 1)
        for i, element in enumerate(tbl[1:]):
            for j, value in enumerate(element[1:]):
                self.dataView.setItem(i, j, QTableWidgetItem(str(value)))

    def change_item(self, item):
        self.modified[(self.titles[item.column() + 1], item.row() + 1)] = item.text()

    def save_all(self):
        if self.modified:
            print("OK")
            cur = self.conn.cursor()
            for key in self.modified.keys():
                cur.execute(f"UPDATE presets SET {key[0]}='{self.modified.get(key)}' WHERE id = {key[1]}")
            self.conn.commit()
            self.modified.clear()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = SettingsWin()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())