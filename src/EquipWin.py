import sys

from PyQt5.QtWidgets import *
from EquipWin_ui import Ui_Dialog
from serial import Serial
import sqlite3


class EquipWin(QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.ch_freq.clicked.connect(self.send_ch_freq)
        self.conn_p = sqlite3.connect('./databases/presets.sqlite')
        self.conn_d = sqlite3.connect('./databases/raw_data.sqlite')
        self.dates = self.conn_d.execute('SELECT time FROM time_moments').fetchall()
        self.dates = list(map(lambda x: x[0], self.dates))
        self.time_moment_select.addItems(self.dates)
        self.show_data()
        self.time_moment_select.currentTextChanged.connect(self.show_data)

    def send_ch_freq(self):
        freq = self.freq_select.text().replace(',', '.')
        pack = 'ch_freq:' + freq + '\n'
        pack = pack.encode("utf-8")
        ser = Serial(*self.conn_p.execute("SELECT com FROM presets WHERE id = 1").fetchone(), 9600)
        ser.write(pack)
        check = (ser.readline().decode("utf-8"), ser.readline().decode("utf-8"), ser.readline().decode("utf-8"))
        print(check)
        if "Succesful\r\n" in check:
            msb = QMessageBox()
            msb.setText("Successful")
            msb.exec()
        else:
            msb = QMessageBox()
            msb.setText("Something wrong. Try again.")
            msb.exec()
        ser.close()

    def show_data(self):
        try:
            data = self.conn_d.execute(f"""SELECT batteryT, BatteryV, obsT, freq, okrT FROM data
                                                WHERE id = (SELECT id FROM time_moments
                                                WHERE time = '{self.time_moment_select.currentText()}')""").fetchone()
            data_str = f"Battery temperature: {data[0]}\n" +\
                       f"Battery Voltage: {data[1]}\n" +\
                       f"Plate temperature: {data[2]}\n" +\
                       f"Scanning frequency: {data[3]}\n" +\
                       f"Outside temperature: {data[4]}\n"
            self.data_view.setPlainText(data_str)
        except Exception as exc:
            self.data_view.setPlainText("No data")
""
def closeEvent(self, QCloseEvent):
        self.conn_p.close()
        self.conn_d.close()
        self.accept()



def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = EquipWin()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())