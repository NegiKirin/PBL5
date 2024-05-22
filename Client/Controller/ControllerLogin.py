import sys
from PyQt5 import QtWidgets
import sys, os
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtCore, QtGui, QtWidgets

# current_directory = os.path.dirname(os.path.abspath(__file__)) + '\\'
# sys.path.append(current_directory)

from Client.View.Login import Login
class ControllerLogin(QMainWindow):
    def __init__(self):
        super().__init__()
        self.uic = Login()
        self.uic.setupUi(self)

        # setup event
        # change page register
        self.uic.btn_change_page.clicked.connect(self.show_register)
        # close window



    def show_register(self):
        self.uic.stackedWidget.setCurrentWidget(self.uic.page_2)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = ControllerLogin()
    main.show()
    sys.exit(app.exec_())