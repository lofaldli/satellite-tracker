import sys
from .map import MapView
from PyQt5.QtWidgets import QWidget, QGridLayout, QApplication


class MainView(QWidget):
    def __init__(self):
        super().__init__()
        self.setLayout(QGridLayout())
        self.map = MapView()
        self.addWidget(self.map)

    def addWidget(self, widget):
        self.layout().addWidget(widget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainView()
    main.show()
    sys.exit(app.exec_())
