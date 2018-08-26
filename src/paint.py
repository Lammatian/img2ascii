import sys
from PyQt5.QtWidgets import QAction, QWidget, QApplication, QMainWindow, QToolButton, QWidgetAction
from PyQt5.QtGui import QPainter, QPainterPath, QColor, QFont, QPen, QIcon, QPalette
from PyQt5.QtCore import Qt, QPoint, QSize, pyqtSignal, QLine

SMALL_BRUSH = 2
MEDIUM_BRUSH = 8
BIG_BRUSH = 14
BRUSHES = [SMALL_BRUSH, MEDIUM_BRUSH, BIG_BRUSH]

class PushButtonAction(QWidgetAction):
    def __init__(self, icon, text, parent=None):
        super(PushButtonAction, self).__init__(parent)
        self.setIcon(icon)
        self.setObjectName(text)
        self.setCheckable(True)

class BrushButtonAction(PushButtonAction):
    def __init__(self, icon, text, brush, parent=None):
        super(BrushButtonAction, self).__init__(icon, text, parent)
        self.brush_size = brush

class Paint(QWidget):
    newPoint = pyqtSignal(QPoint)

    def __init__(self, parent=None):
        super().__init__()
        self.paths = []
        self.palette = QPalette()
        self.palette.setColor(QPalette.Background, QColor(255, 255, 255))
        self.setAutoFillBackground(True)
        self.setPalette(self.palette)
        self.brush_size = MEDIUM_BRUSH
        self.is_erasing = False
        self.current_brush = 1

    def set_brush(self, brush_size):
        if brush_size != self.brush_size:
            self.current_brush = BRUSHES.index(brush_size)
            self.brush_size = brush_size

    def undo(self):
        if self.paths:
            self.paths.pop()
            self.update()

    def toggle_erase(self):
        self.is_erasing = not self.is_erasing

    def paintEvent(self, event):
        qp = QPainter(self)

        for path, size, erase in self.paths:
            pen = QPen()
            pen.setWidth(size)
            pen.setColor(QColor(255, 255, 255) if erase else QColor(0, 0, 0))
            qp.setPen(pen)

            qp.drawPath(path)

    def mousePressEvent(self, event):
        # Update only the path that is currently chosen
        self.paths.append((QPainterPath(), self.brush_size, self.is_erasing))
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
        self.addToolBar(Qt.BottomToolBarArea, self.toolbar)

        self.smallBrushAction = BrushButtonAction(QIcon("../img/draw_button_small.png"), "&Small brush", SMALL_BRUSH, self)
        self.smallBrushAction.setShortcut("1")
        self.smallBrushAction.triggered.connect(lambda: self.change_brush(self.smallBrushAction))
        self.mediumBrushAction = BrushButtonAction(QIcon("../img/draw_button_medium.png"), "&Medium brush", MEDIUM_BRUSH, self)
        self.mediumBrushAction.setShortcut("2")
        self.mediumBrushAction.setChecked(True)
        self.mediumBrushAction.triggered.connect(lambda: self.change_brush(self.mediumBrushAction))
        self.bigBrushAction = BrushButtonAction(QIcon("../img/draw_button_big.png"), "&Big brush", BIG_BRUSH, self)
        self.bigBrushAction.setShortcut("3")
        self.bigBrushAction.triggered.connect(lambda: self.change_brush(self.bigBrushAction))

        self.eraseBrushAction = PushButtonAction(QIcon("../img/erase_button.png"), "&Erase", self)
        self.eraseBrushAction.setShortcut("4")
        self.eraseBrushAction.triggered.connect(self.paint.toggle_erase)
        
        self.undoAction = QAction("Undo", self)
        self.undoAction.setShortcut("Ctrl+Z")
        self.undoAction.triggered.connect(self.paint.undo)

        self.toolbar.addAction(self.smallBrushAction)
        self.toolbar.addAction(self.mediumBrushAction)
        self.toolbar.addAction(self.bigBrushAction)
        self.toolbar.addAction(self.eraseBrushAction)
        self.toolbar.addAction(self.undoAction)

        self.show()

    def change_brush(self, brush):
        # We just checked this brush
        if brush.isChecked():
            self.smallBrushAction.setChecked(False)
            self.mediumBrushAction.setChecked(False)
            self.bigBrushAction.setChecked(False)
            brush.setChecked(True)
            self.paint.set_brush(brush.brush_size)
        # We clicked the one already checked
        else:
            brush.setChecked(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())