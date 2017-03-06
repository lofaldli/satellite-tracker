from coords import latlon2uv
from PyQt5.QtCore import Qt, QRectF, QTimer, QSize
from PyQt5.QtGui import QBrush, QPixmap, QPen
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView, QGraphicsItem, \
        QGraphicsTextItem, QGraphicsRectItem, QGraphicsPixmapItem


class MapViewItem(QGraphicsItem):
    def __init__(self, viewModel):
        super().__init__()
        self.viewModel = viewModel
        self.setToolTip(viewModel.name)
        self.size = 10
        self.setup()

    def setup(self):
        self.setupGraphics()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(1000)

    def brush(self, color=Qt.white, style=Qt.SolidPattern):
        return QBrush(color, style)

    def pen(self, color=Qt.black, style=Qt.SolidLine):
        pen = QPen(color)
        pen.setStyle(style)
        return pen

    def setLatlon(self, latlon, scene=None):
        if not scene:
            scene = self.scene()
        u, v = latlon2uv(latlon)
        self.setPos(u * scene.width(), v * scene.height())

    def paint(self, painter, option, widget):
        pass

    def boundingRect(self):
        return QRectF(-self.size/2, -self.size/2, self.size, self.size)

    def setupGraphics(self):
        raise NotImplementedError('must be overriden')

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemSceneChange:
            latlon = self.viewModel.latlon()
            scene = value
            self.setLatlon(latlon, scene)
        return super().itemChange(change, value)


class SatelliteViewItem(MapViewItem):
    def __init__(self, viewModel):
        super().__init__(viewModel)

    def setupGraphics(self):
        self.label = QGraphicsTextItem(self.viewModel.name, self)
        self.label.setDefaultTextColor(Qt.white)

        self.rect = QGraphicsRectItem(self.boundingRect(), self)
        self.rect.setBrush(self.brush(color=Qt.white))
        self.rect.setPen(self.pen(color=Qt.white))

    def update(self):
        latlon = self.viewModel.latlon()
        self.setToolTip(str(latlon.lat) + ' ' + str(latlon.lon))
        self.setLatlon(latlon)
        super().update()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # self.setSize(min(self.scene().width(), self.scene().height()) * 0.05)


class GroundStationViewItem(MapViewItem):
    def setupGraphics(self):
        self.rectangle = QGraphicsRectItem(self.boundingRect(), self)
        self.rectangle.setBrush(self.brush(color=Qt.green))
        self.rectangle.setPen(self.pen(color=Qt.white))


class MapView(QGraphicsView):
    def __init__(self, background='images/world_map.jpg'):
        super().__init__(QGraphicsScene())
        self.background = QGraphicsPixmapItem(QPixmap(background))
        self.addItem(self.background)
        self.satellites = []
        self.groundStations = []

    def sizeHint(self):
        return QSize(800, 400)

    def width(self):
        return self.scene().width()

    def height(self):
        return self.scene().height()

    def addSatellite(self, viewModel):
        satellite = SatelliteViewItem(viewModel)
        self.addItem(satellite)
        self.satellites.append(satellite)

    def addGroundStation(self, viewModel):
        groundStation = GroundStationViewItem(viewModel)
        self.addItem(groundStation)
        self.groundStations.append(groundStation)

    def addItem(self, item):
        self.scene().addItem(item)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.fitInView(self.sceneRect())
        # self.background.pixmap().scaled(self.width(), self.height())
