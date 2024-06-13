import sys
import pickle
import socket
import threading
import time
from PyQt5.QtWidgets import QApplication
from Raspberry.Network.Sender import Sender
from Raspberry.Network.Receiver import Receiver
from Raspberry.Controller.Controller import Controller
import tensorflow_hub as hub
class Rashpberry():
    def __init__(self):
        self.soc = None
        self.host = "localhost"
        self.port = 9999

        self.create_socket()
        self.connect_socket()

        self.sender = Sender(self.soc)
        self.initMovenet()
        # draw gui
        app = QApplication(sys.argv)
        self.controller = Controller(self.sender,self.movenet)
        self.controller.show()
        self.receiver = Receiver(self.soc, self.sender, self.controller)
        # self.detector.load_data()
        # t1 = threading.Thread(target=self.detector.face_detection, args=[main_win])
        # t1.setDaemon = True
        # t1.start()
        sys.exit(app.exec())

    def initMovenet(self):
        model = hub.load("https://www.kaggle.com/models/google/movenet/TensorFlow2/singlepose-thunder/4")
        self.movenet = model.signatures['serving_default']
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
    c = Rashpberry()