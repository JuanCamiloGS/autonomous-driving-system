# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Design.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1305, 758)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.S2 = QtGui.QLCDNumber(self.centralwidget)
        self.S2.setGeometry(QtCore.QRect(180, 90, 64, 23))
        self.S2.setObjectName(_fromUtf8("S2"))
        self.S1 = QtGui.QLCDNumber(self.centralwidget)
        self.S1.setGeometry(QtCore.QRect(60, 180, 64, 23))
        self.S1.setObjectName(_fromUtf8("S1"))
        self.S3 = QtGui.QLCDNumber(self.centralwidget)
        self.S3.setGeometry(QtCore.QRect(290, 180, 64, 23))
        self.S3.setObjectName(_fromUtf8("S3"))
        self.S4 = QtGui.QLCDNumber(self.centralwidget)
        self.S4.setGeometry(QtCore.QRect(80, 340, 64, 23))
        self.S4.setObjectName(_fromUtf8("S4"))
        self.S5 = QtGui.QLCDNumber(self.centralwidget)
        self.S5.setGeometry(QtCore.QRect(280, 340, 64, 23))
        self.S5.setObjectName(_fromUtf8("S5"))
        self.ATView = PlotWidget(self.centralwidget)
        self.ATView.setGeometry(QtCore.QRect(410, 30, 341, 201))
        self.ATView.setStyleSheet(_fromUtf8("background-color: transparent;"))
        self.ATView.setObjectName(_fromUtf8("ATView"))
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(50, 70, 321, 331))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_4 = QtGui.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(50, 40, 171, 17))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.ATView_2 = PlotWidget(self.centralwidget)
        self.ATView_2.setGeometry(QtCore.QRect(410, 230, 341, 201))
        self.ATView_2.setStyleSheet(_fromUtf8("background-color: transparent;"))
        self.ATView_2.setObjectName(_fromUtf8("ATView_2"))
        self.groupBox = QtGui.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(20, 450, 341, 281))
        self.groupBox.setStyleSheet(_fromUtf8("QGroupBox { \n"
"     border: 2px solid gold; \n"
"     border-radius: 10px;\n"
"    margin-top: 6px;\n"
" } \n"
"QGroupBox::title { \n"
"    subcontrol-origin: margin;\n"
"    subcontrol-position:top center;\n"
" }"))
        self.groupBox.setFlat(True)
        self.groupBox.setCheckable(False)
        self.groupBox.setChecked(False)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.VelView = PlotWidget(self.groupBox)
        self.VelView.setGeometry(QtCore.QRect(10, 60, 311, 211))
        self.VelView.setStyleSheet(_fromUtf8("background-color: transparent;"))
        self.VelView.setObjectName(_fromUtf8("VelView"))
        self.label_5 = QtGui.QLabel(self.groupBox)
        self.label_5.setGeometry(QtCore.QRect(10, 30, 191, 17))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.ST = QtGui.QLCDNumber(self.groupBox)
        self.ST.setGeometry(QtCore.QRect(220, 20, 101, 31))
        self.ST.setObjectName(_fromUtf8("ST"))
        self.groupBox_2 = QtGui.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(20, 20, 751, 421))
        self.groupBox_2.setStyleSheet(_fromUtf8("QGroupBox { \n"
"     border: 2px solid silver; \n"
"     border-radius: 10px;\n"
"    margin-top: 6px;\n"
" } \n"
"QGroupBox::title { \n"
"    subcontrol-origin: margin;\n"
"    subcontrol-position:top center;\n"
" }"))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.groupBox_4 = QtGui.QGroupBox(self.centralwidget)
        self.groupBox_4.setGeometry(QtCore.QRect(380, 450, 541, 281))
        self.groupBox_4.setStyleSheet(_fromUtf8("QGroupBox { \n"
"     border: 2px solid gold; \n"
"     border-radius: 10px;\n"
"    margin-top: 6px;\n"
" } \n"
"QGroupBox::title { \n"
"    subcontrol-origin: margin;\n"
"    subcontrol-position:top center;\n"
" }"))
        self.groupBox_4.setFlat(True)
        self.groupBox_4.setCheckable(False)
        self.groupBox_4.setChecked(False)
        self.groupBox_4.setObjectName(_fromUtf8("groupBox_4"))
        self.FuzzyDet = PlotWidget(self.groupBox_4)
        self.FuzzyDet.setGeometry(QtCore.QRect(0, 10, 291, 281))
        self.FuzzyDet.setStyleSheet(_fromUtf8("background-color: transparent;"))
        self.FuzzyDet.setObjectName(_fromUtf8("FuzzyDet"))
        self.FuzzyDet_2 = PlotWidget(self.groupBox_4)
        self.FuzzyDet_2.setGeometry(QtCore.QRect(250, 10, 291, 281))
        self.FuzzyDet_2.setStyleSheet(_fromUtf8("background-color: transparent;"))
        self.FuzzyDet_2.setObjectName(_fromUtf8("FuzzyDet_2"))
        self.label = QtGui.QLabel(self.groupBox_4)
        self.label.setGeometry(QtCore.QRect(140, 260, 31, 17))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(self.groupBox_4)
        self.label_2.setGeometry(QtCore.QRect(360, 260, 31, 17))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.FuzzyDet_2.raise_()
        self.FuzzyDet.raise_()
        self.label.raise_()
        self.label_2.raise_()
        self.groupBox_6 = QtGui.QGroupBox(self.centralwidget)
        self.groupBox_6.setGeometry(QtCore.QRect(940, 20, 351, 351))
        self.groupBox_6.setStyleSheet(_fromUtf8("QGroupBox { \n"
"     border: 2px solid silver;\n"
"    border-radius: 10px;\n"
"    margin-top: 6px;\n"
" } \n"
"QGroupBox::title { \n"
"    left: 30px;\n"
"    subcontrol-position:top left;\n"
"    subcontrol-origin: margin;\n"
" }"))
        self.groupBox_6.setObjectName(_fromUtf8("groupBox_6"))
        self.Steering = PlotWidget(self.groupBox_6)
        self.Steering.setGeometry(QtCore.QRect(10, 30, 321, 301))
        self.Steering.setStyleSheet(_fromUtf8("background-color: transparent;"))
        self.Steering.setObjectName(_fromUtf8("Steering"))
        self.groupBox_5 = QtGui.QGroupBox(self.centralwidget)
        self.groupBox_5.setGeometry(QtCore.QRect(940, 380, 351, 351))
        self.groupBox_5.setStyleSheet(_fromUtf8("QGroupBox { \n"
"     border: 2px solid gold;\n"
"    border-radius: 10px;\n"
"    margin-top: 6px;\n"
" } \n"
"QGroupBox::title { \n"
"    left: 30px;\n"
"    subcontrol-position:top left;\n"
"    subcontrol-origin: margin;\n"
" }"))
        self.groupBox_5.setObjectName(_fromUtf8("groupBox_5"))
        self.BAView = PlotWidget(self.groupBox_5)
        self.BAView.setGeometry(QtCore.QRect(10, 30, 321, 301))
        self.BAView.setStyleSheet(_fromUtf8("background-color: transparent;"))
        self.BAView.setObjectName(_fromUtf8("BAView"))
        self.label_6 = QtGui.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(780, 30, 151, 411))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.groupBox_2.raise_()
        self.groupBox.raise_()
        self.ATView.raise_()
        self.label_3.raise_()
        self.label_4.raise_()
        self.S2.raise_()
        self.S1.raise_()
        self.S3.raise_()
        self.S4.raise_()
        self.S5.raise_()
        self.ATView_2.raise_()
        self.groupBox_4.raise_()
        self.groupBox_6.raise_()
        self.groupBox_5.raise_()
        self.label_6.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menuBar = QtGui.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1305, 25))
        self.menuBar.setObjectName(_fromUtf8("menuBar"))
        MainWindow.setMenuBar(self.menuBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Intelligent Autonomous Control System Interface (IACSI)", None))
        self.label_3.setText(_translate("MainWindow", "<html><head/><body><p><img src=\":/Carro/car_mini.png\"/></p></body></html>", None))
        self.label_4.setText(_translate("MainWindow", "Obstacles Distance (m):", None))
        self.groupBox.setTitle(_translate("MainWindow", "Inputs for Fuzzy Logic", None))
        self.label_5.setText(_translate("MainWindow", "Frontal Track Distance (m):", None))
        self.groupBox_2.setTitle(_translate("MainWindow", "Inputs for Neural Network", None))
        self.groupBox_4.setTitle(_translate("MainWindow", "Fuzzy Determination", None))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:8pt;\">Accel</span></p></body></html>", None))
        self.label_2.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:8pt;\">Brake</span></p></body></html>", None))
        self.groupBox_6.setTitle(_translate("MainWindow", "Neural Network Output", None))
        self.groupBox_5.setTitle(_translate("MainWindow", "Fuzzy Logic Output", None))
        self.label_6.setText(_translate("MainWindow", "<html><head/><body><p><img src=\":/Red/neuralcol.png\"/></p></body></html>", None))

from pyqtgraph import PlotWidget
import Carro_rc
import Logo_rc
import Red_rc
