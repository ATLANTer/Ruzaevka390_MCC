# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src\gui\ReqstWin.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(524, 325)
        self.stop = QtWidgets.QPushButton(Dialog)
        self.stop.setGeometry(QtCore.QRect(10, 270, 241, 41))
        self.stop.setObjectName("stop")
        self.begin = QtWidgets.QPushButton(Dialog)
        self.begin.setGeometry(QtCore.QRect(260, 270, 251, 41))
        self.begin.setObjectName("begin")
        self.data = QtWidgets.QTextEdit(Dialog)
        self.data.setGeometry(QtCore.QRect(10, 10, 501, 241))
        self.data.setReadOnly(True)
        self.data.setObjectName("data")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.stop.setText(_translate("Dialog", "Стоп"))
        self.begin.setText(_translate("Dialog", "Начать"))
