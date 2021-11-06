# -*- coding: utf-8 -*-
import sys
from help_objs import *
import sqlite3
import shutil

from PyQt5.QtWidgets import *
from SettingsWin_ui import Ui_Dialog


class SettingsWin(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super().__init__()
        self.setupUi(self)
        self.initUI()
        self.db_columns = ["id", "com", "logo"]

    def initUI(self):
        self.conn = sqlite3.connect("./databases/presets.sqlite")
        cur = self.conn.cursor()
        self.setFixedSize(520, 439)
        self.SaveButtons.buttonClicked.connect(self.SButts)
        self.com_select.addItems(serial_ports())
        self.modified = dict()
        self.upload_table()
        self.dataView.itemChanged.connect(self.change_item)
        self.db_buttons.buttonClicked.connect(self.db_butts)
        self.path2logo.setText(*cur.execute("SELECT logo FROM presets WHERE id = 1").fetchone())
        self.last_id = len(cur.execute("SELECT * FROM presets").fetchall())
        self.logo_imp.clicked.connect(self.import_logo_path)

    def SButts(self, butt):
        if butt.text() == "Применить":
            self.save_all()
            self.conn.commit()
            self.upload_table()
            print("Applied")  # DEBUG
        elif butt.text() == "Ок":
            self.conn.close()
            self.accept()
        elif "пресет" in butt.text():
            cur = self.conn.cursor()
            cur.execute(f"""INSERT INTO presets(id,com,logo) VALUES 
                        ({self.last_id}, '{self.com_select.currentText()}', '{self.path2logo.text()}')""")
            self.last_id += 1
            self.conn.commit()
            self.upload_table()

    def db_butts(self, butt):
        if butt.text() == "Удалить":
            ind = int(self.p_id.text())
            if ind not in (0, 1):
                cur = self.conn.cursor()
                cur.execute(f"DELETE FROM presets WHERE id = {ind}")
                cur.execute("UPDATE presets SET id = id - 1 WHERE id > ?", (ind,))
                self.last_id -= 1
                self.conn.commit()
                self.upload_table()
        if butt.text() == "Загрузить":
            ind = int(self.p_id.text())
            self.copy_row_db(ind, 1)
        if "умолч" in butt.text():
            self.copy_row_db(0, 1)
        if "Экспорт" in butt.text():
            dirlist = QFileDialog.getExistingDirectory(self, "Выбрать папку", ".")
            shutil.copyfile("databases/raw_data.sqlite", f"{dirlist}/exported_data.sqlite")
        if "Очистить" in butt.text():
            mb = QMessageBox.question(self, 'Подтверждение', "Вы действительно желаете очистить базу данных?",
                                      QMessageBox.Yes | QMessageBox.No,
                                      QMessageBox.No)
            if mb == QMessageBox.Yes:
                conn = sqlite3.connect("./databases/raw_data.sqlite")
                cur = conn.cursor()
                cur.execute("DELETE FROM data")
                cur.execute("DELETE FROM time_moments")
                conn.close()

    def import_logo_path(self):
        self.path2logo.setText(QFileDialog.getOpenFileName(
                                self, 'Выбрать картинку', '',
                                'logo (*.png)')[0])

    def copy_row_db(self, ind_src, ind_ins):
        cur = self.conn.cursor()
        src = cur.execute(f"SELECT * FROM presets WHERE id = {ind_src}").fetchone()
        que = "UPDATE presets SET\n"
        que += ", ".join([f"{self.db_columns[i]}='{src[i]}'" for i in range(1, len(src))])
        que += " WHERE id = ?"
        cur.execute(que, (ind_ins,))
        self.conn.commit()
        self.upload_table()

    def upload_table(self):
        cur = self.conn.cursor()
        tbl = cur.execute("SELECT * FROM presets").fetchall()
        self.dataView.setRowCount(len(tbl) - 1)
        self.dataView.setColumnCount(len(tbl[0]) - 1)
        for i, element in enumerate(tbl[1:]):
            for j, value in enumerate(element[1:]):
                self.dataView.setItem(i, j, QTableWidgetItem(str(value)))

    def change_item(self, item):
        self.modified[(self.db_columns[item.column() + 1], item.row() + 1)] = item.text()

    def save_all(self):
        if self.modified:
            print("OK")
            cur = self.conn.cursor()
            for key in self.modified.keys():
                cur.execute(f"UPDATE presets SET {key[0]}='{self.modified.get(key)}' WHERE id = {key[1]}")
            self.conn.commit()
            self.modified.clear()
        cur = self.conn.cursor()
        cur.execute(f"""UPDATE presets SET 
                    {self.db_columns[1]}='{self.com_select.currentText()}',
                    {self.db_columns[2]}='{self.path2logo.text()}' WHERE id = 1""")

    def closeEvent(self, QCloseEvent):
        self.conn.close()
        self.reject()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = SettingsWin()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())