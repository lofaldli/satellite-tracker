#!/usr/bin/env python3.5

import sys
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QGridLayout, \
        QPushButton, QLineEdit, QLabel, QFormLayout, QHBoxLayout
from views.main import MainView
from viewmodels import SatelliteViewModel


def say_hello():
    print('hello')


class AddSatelliteDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Add satellite')
        self.setLayout(QGridLayout())
        self.setupWidgets()

    def sizeHint(self):
        return QSize(400, 100)

    def setupWidgets(self):
        formLayout = QFormLayout()
        self.layout().addLayout(formLayout, 0, 0)
        buttonsLayout = QHBoxLayout()
        self.layout().addLayout(buttonsLayout, 1, 0)

        self.titleLineEdit = QLineEdit()
        self.titleLineEdit.setMaxLength(24)
        formLayout.addRow(QLabel('Title'), self.titleLineEdit)

        self.line1LineEdit = QLineEdit()
        self.line1LineEdit.setMaxLength(69)
        formLayout.addRow(QLabel('Line 1'), self.line1LineEdit)

        self.line2LineEdit = QLineEdit()
        self.line2LineEdit.setMaxLength(69)
        formLayout.addRow(QLabel('Line 2'), self.line2LineEdit)

        okButton = QPushButton('OK')
        okButton.clicked.connect(self.accept)
        buttonsLayout.addWidget(okButton)
        cancelButton = QPushButton('Cancel')
        cancelButton.clicked.connect(self.reject)
        buttonsLayout.addWidget(cancelButton)

    def title(self):
        return self.titleLineEdit.text()

    def line1(self):
        return self.line1LineEdit.text()

    def line2(self):
        return self.line2LineEdit.text()

    def data(self):
        return self.title(), self.line1(), self.line2()


class GUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('satellite tracker')
        self.setCentralWidget(MainView())
        self.setupMenuBar()

    def setupMenuBar(self):
        fileMenu = self.menuBar().addMenu('&File')
        exitAction = fileMenu.addAction('E&xit (alt+f4)')
        exitAction.triggered.connect(self.close)

        editMenu = self.menuBar().addMenu('&Edit')
        addSatelliteAction = editMenu.addAction('Add satellite')
        addSatelliteAction.triggered.connect(self.addSatellite)

    def addSatellite(self):
        dialog = AddSatelliteDialog()
        if dialog.exec_():
            title, line1, line2 = dialog.data()
            satellite = SatelliteViewModel(title, line1, line2)
            self.centralWidget().map.addSatellite(satellite)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = GUI()
    iss_tle = '''ISS (ZARYA)
1 25544U 98067A   17065.56793981  .00003800  00000-0  64586-4 0  9991
2 25544  51.6432 189.8382 0006932 257.6582 289.5802 15.54142949 45790'''
    title, line1, line2 = iss_tle.split('\n')
    satellite = SatelliteViewModel(title, line1, line2)
    gui.centralWidget().map.addSatellite(satellite)
    gui.show()
    sys.exit(app.exec_())
