import sys
from PyQt5.QtCore    import Qt
from PyQt5.QtGui     import QPixmap, QPainter, QPainterPath
from PyQt5.QtWidgets import QLabel, QWidget, QHBoxLayout, QApplication

class Label(QLabel):
    def __init__(self, *args, antialiasing=True, **kwargs):
        super(Label, self).__init__(*args, **kwargs)
        self.Antialiasing = antialiasing
        self.setMaximumSize(50, 50)
        self.setMinimumSize(50, 50)
        self.radius = 25 

        self.target = QPixmap(self.size())  
        self.target.fill(Qt.transparent)   

        p = QPixmap("E:\PBL_2\PBL5\Server\DB\images.jpg").scaled(
            50, 50, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)

        painter = QPainter(self.target)
        if self.Antialiasing:
            painter.setRenderHint(QPainter.Antialiasing, True)
            painter.setRenderHint(QPainter.HighQualityAntialiasing, True)
            painter.setRenderHint(QPainter.SmoothPixmapTransform, True)

        path = QPainterPath()
        path.addRoundedRect(
            0, 0, self.width(), self.height(), self.radius, self.radius)

        painter.setClipPath(path)
        painter.drawPixmap(0, 0, p)
        self.setPixmap(self.target)

class Window(QWidget):
    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        layout = QHBoxLayout(self)
        layout.addWidget(Label(self))
        layout.addWidget(Label(self, antialiasing=False))  
        self.setStyleSheet("background: blue;")           

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())