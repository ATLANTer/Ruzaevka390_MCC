import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from MainWin_ui import Ui_MainWindow


class MainWin(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        logo_pm = QPixmap("SatLogo.png")
        logo = QLabel(self)
        logo.move(15, 0)
        logo.resize(300, 300)
        logo.setPixmap(logo_pm)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MainWin()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
