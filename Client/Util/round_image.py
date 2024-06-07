from IPython.external.qt_for_kernel import QtCore
from pyqt5_plugins.examplebuttonplugin import QtGui


def round_image_url(url_image):
    # url_image = "Image/z5461290588979_692bf1a21a79b202b016a475ef95d80d.jpg"
    source = QtGui.QImage(url_image)
    # self.resize(source.width(), source.height())

    output = QtGui.QPixmap(source.width(), source.height())
    output.fill(QtCore.Qt.transparent)

    qp = QtGui.QPainter(output)
    clipPath = QtGui.QPainterPath()
    clipPath.addRoundedRect(QtCore.QRectF(source.rect()), source.height() // 2, source.height() // 2)
    qp.setClipPath(clipPath)
    qp.drawPixmap(0, 0, QtGui.QPixmap(source))
    qp.end()
    return output

def round_image(source):

    # h, w, _ = img.shape
    # source = QtGui.QImage(img.data, w, h, 3 * w, QtGui.QImage.Format_RGB888)

    output = QtGui.QPixmap(source.width(), source.height())
    output.fill(QtCore.Qt.transparent)

    qp = QtGui.QPainter(output)
    clipPath = QtGui.QPainterPath()
    clipPath.addRoundedRect(QtCore.QRectF(source.rect()), source.height() // 2, source.height() // 2)
    qp.setClipPath(clipPath)
    qp.drawPixmap(0, 0, QtGui.QPixmap(source))
    qp.end()
    return output

def round_image_icon(source):

    # h, w, _ = img.shape
    # source = QtGui.QImage(img.data, w, h, 3 * w, QtGui.QImage.Format_RGB888)

    output = QtGui.QPixmap(source.width(), source.height())
    output.fill(QtCore.Qt.transparent)

    qp = QtGui.QPainter(output)
    clipPath = QtGui.QPainterPath()
    clipPath.addRoundedRect(QtCore.QRectF(source.rect()), source.height() // 2, source.height() // 2)
    qp.setClipPath(clipPath)
    qp.drawPixmap(0, 0, QtGui.QIcon(source))
    qp.end()
    return output