import sys
from PyQt5.QtWidgets import QAction, QWidget, QApplication, QMainWindow
from PyQt5.QtGui import QPainter, QPainterPath, QColor, QFont, QPen
from PyQt5.QtCore import Qt, QPoint, QSize, pyqtSignal, QLine

SMALL_BRUSH = 2
MEDIUM_BRUSH = 6
BIG_BRUSH = 10
BRUSHES = [SMALL_BRUSH, MEDIUM_BRUSH, BIG_BRUSH]

class Paint(QWidget):
    newPoint = pyqtSignal(QPoint)

    def __init__(self, parent=None):
        super().__init__()
        # small, medium, big
        self.paths = []
        self.brush_size = MEDIUM_BRUSH
        self.current_brush = 1

    def set_brush(self, brush_size):
        if brush_size != self.brush_size:
            self.current_brush = BRUSHES.index(brush_size)
            self.brush_size = brush_size

    def paintEvent(self, event):
        #self.lines.append(QLine(self.last_point, self.new_point))
        qp = QPainter(self)

        for path, size in self.paths:
            pen = QPen()
            pen.setWidth(size)
            pen.setColor(QColor(size*20, size*20, size*20))
            qp.setPen(pen)

            qp.drawPath(path)

    def mousePressEvent(self, event):
        # Update only the path that is currently chosen
        self.paths.append((QPainterPath(), self.brush_size))
        self.paths[-1][0].moveTo(event.pos())
        self.update()

    def mouseMoveEvent(self, event):
        # Update only the path that is currently chosen
        self.paths[-1][0].lineTo(event.pos())
        self.newPoint.emit(event.pos())
        self.update()

    def sizeHint(self):
        return QSize(1000, 600)

class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.initUI()

    def initUI(self):
        self.paint = Paint(self)
        self.setCentralWidget(self.paint)
        self.setWindowTitle("Paint window")
        self.toolbar = self.addToolBar("Tools")

        smallBrushAction = QAction("&Small brush", self)
        smallBrushAction.setShortcut("1")
        smallBrushAction.triggered.connect(lambda: self.paint.set_brush(SMALL_BRUSH))
        mediumBrushAction = QAction("&Medium brush", self)
        mediumBrushAction.setShortcut("2")
        mediumBrushAction.triggered.connect(lambda: self.paint.set_brush(MEDIUM_BRUSH))
        bigBrushAction = QAction("&Big brush", self)
        bigBrushAction.setShortcut("3")
        bigBrushAction.triggered.connect(lambda: self.paint.set_brush(BIG_BRUSH))

        self.toolbar.addAction(smallBrushAction)
        self.toolbar.addAction(mediumBrushAction)
        self.toolbar.addAction(bigBrushAction)

        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())