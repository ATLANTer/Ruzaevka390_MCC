# -*- coding: utf-8 -*-
import sqlite3

import keyboard
from PyQt5.QtWidgets import *
from serial import Serial

from ReqstWin_ui import Ui_Dialog
from help_objs import *


class ReqstWin(QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.conn_presets = sqlite3.connect('./databases/presets.sqlite')
        self.conn_data = sqlite3.connect('./databases/raw_data.sqlite')
        self.begin.clicked.connect(self.begin_butt)
        self.save2csv.clicked.connect(self.s2scv_butt)

    def begin_butt(self):
        cur_p = self.conn_presets.cursor()
        cur_d = self.conn_data.cursor()
        try:
            self.data_receive = list()
            ser = Serial(*cur_p.execute("SELECT com FROM presets WHERE id = 1").fetchone(), 9600)
            ser.write("cdr\n")
            print("Begin")  # DEBUG
            pack = ''
            self.info.setText("Идёт передача, подождите! (Для остановки зажмите C)")
            self.update()
            while pack != ";;;;;\n":
                if not ser.inWaiting():
                    if keyboard.is_pressed('c'):
                        break
                else:
                    if not keyboard.is_pressed('c'):
                        pack = ser.readline().decode("utf-8")
                        self.data_receive.append(pack)
                    else:
                        break

            self.info.setText("")
            self.data.setPlainText("".join(self.data_receive))
            for pck in self.data_receive:
                pck = pck.split(';')
                if len(pck) == 12:
                    if pck[8] == '':
                        pck[8] = '0'
                    que = f"INSERT INTO time_moments(time) VALUES('{' '.join(pck[:2])}')"
                    cur_d.execute(que)
                    que = f"""INSERT INTO data
                            (batteryV, BatteryT, obsT, latitude, longitude, altitude, rssi, freq, okrT) 
                            VALUES({', '.join(pck[2:-1])})"""
                    cur_d.execute(que)
                    self.conn_data.commit()
            ser.write('cdw\n')
        except Exception as exc:
            print(exc)  # DEBUG

    def s2scv_butt(self):
        head = "batteryV;BatteryT;obsT;latitude;longitude;altitude;rssi;freq;okrT"
        path = QFileDialog.getExistingDirectory(self, "Выбрать папку", ".") + "/data.csv"
        csv_writer(self.delim.text(), head, path, self.data_receive)

    def closeEvent(self, QCloseEvent):
        self.conn_presets.close()
        self.conn_data.close()
        self.accept()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = ReqstWin()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())

'''
if not ser.inWaiting():
    pass
'''
