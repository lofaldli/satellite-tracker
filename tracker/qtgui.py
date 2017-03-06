#!/usr/bin/env python3.5

import sys
import coords
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout
from views import MapView, SatelliteViewItem, GroundStationViewItem
from viewmodels import SatelliteViewModel, GroundStationViewModel


class GUI(QWidget):
    def __init__(self, title):
        super().__init__()
        self.setLayout(QGridLayout(self))
        self.setWindowTitle('satellite tracker')

    def addWidget(self, widget, row=0, column=0):
        self.layout().addWidget(widget, row, column)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    map = MapView()
    tle = '''ISS
1 25544U 98067A   17065.22548443  .00003954  00000-0  66917-4 0  9995
2 25544  51.6431 191.5459 0006882 256.3711 173.5923 15.54140743 45749'''
    name, line1, line2 = tle.split('\n')
    iss = SatelliteViewModel(name, line1, line2)
    trd = GroundStationViewModel('Trondheim', coords.LatLon(63, 10))
    map.addItem(SatelliteViewItem(iss))
    map.addItem(GroundStationViewItem(trd))
    map.show()
    # gui = GUI('satellite tracker')
    # gui.addWidget(map)
    # gui.show()
    sys.exit(app.exec_())
