import sys
import pickle
import socket
import threading
import time
from PyQt5.QtWidgets import QApplication

from Client.Network.Receiver import Receiver
from Client.Network.Sender import Sender
from Controller.Controller import Controller

class Client():
    # def __init__(self,host="192.168.220.1",port=9999):
    #     # socket
    #     self.host = host
    #     self.port = port
    #     self.soc = None
    #     # draw ui
    #
    #     app = QApplication(sys.argv)
    #     self.controller = ControllerLogin(self.soc)
    #     self.controller.show()
    #     self.create_TCP()
    #     sys.exit(app.exec_())
    #
    #
    #
    # def create_TCP(self):
    #     self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     print("Socket created")
    #     server_address = (self.host, self.port)
    #     print('connecting to %s port ' + str(server_address))
    #     self.soc.connect(server_address)
    def __init__(self):
        self.soc = None
        self.host = "localhost"
        self.port = 9999

        self.create_socket()
        self.connect_socket()

        self.sender = Sender(self.soc)

        # self.detector = checkin.face_detector(cam=0)

        # draw gui
        app = QApplication(sys.argv)
        self.controller = Controller(self.sender)
        self.controller.controllerLogin.show()
        self.controller.managerUser.show()
        #self.controller.managerUser.hide()
        self.receiver = Receiver(self.soc, self.sender, self.controller)
        # self.detector.load_data()
        # t1 = threading.Thread(target=self.detector.face_detection, args=[main_win])
        # t1.setDaemon = True
        # t1.start()

        self.arduino = None
        sys.exit(app.exec())

    def create_socket(self):
        try:
            self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print('Has been created a socket server')
        except socket.error as msg:
            print(str(msg) + ' .Trying to connecting again...')
            self.create_socket()


    def connect_socket(self):
        try:
            self.soc.connect((self.host, self.port))
            print('Established connection with PORT = ' + str(self.port))
        except socket.error as msg:
            print(str(msg) + ' Trying to connect...')
            self.connect_socket()


    def close_socket(self):
        if self.soc is not None:
            try:
                self.soc.close()
                print('Close socket')
            except socket.error as msg:
                print(str(msg) + ' Trying to close')
                self.close_socket()


if __name__ == "__main__":
    c = Client()