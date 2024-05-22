import sys

from PyQt5.QtWidgets import QApplication

from Controller.ControllerLogin import ControllerLogin

class Client():
    def __init__(self):
        # socket


        # draw ui
        app = QApplication(sys.argv)
        controller = ControllerLogin()
        controller.show()
        sys.exit(app.exec_())



if __name__ == "__main__":
    Client()