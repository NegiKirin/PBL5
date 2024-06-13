import pickle
import sys
import threading
import socket

import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication

from Client.Model.User import User
from Raspberry.Util.Command import Command

BUFF_SIZE = 65536
HEADERSIZE = 10
COMMANDSIZE = 3
class Receiver:
    def __init__(self, conn, sender, controller):
        self.socket = conn
        self.sender = sender
        self.controller = controller
        self.frame_shape = False
        t = threading.Thread(target=self.run, args=())
        # t.setDaemon = True
        t.start()

    def getCommand(self, data):
        command = int(data[:COMMANDSIZE])
        return command
    def getSize(self, data):
        size = int(data[COMMANDSIZE:HEADERSIZE])
        return size

    def receiverWordPredict(self, data):
        try:
            size = self.getSize(data)
            main_data = None
            full_msg = b''
            new_msg = True
            while True:
                msg = self.socket.recv(1024)
                if new_msg:
                    msg = data + msg
                    new_msg = False
                full_msg += msg
                if len(full_msg) - HEADERSIZE - COMMANDSIZE == size:
                    main_data = pickle.loads(full_msg[HEADERSIZE + COMMANDSIZE:])
                    break

            self.controller.display_Word_Predict(main_data['word'])
        except Exception as e:
            print(e)

    def run(self):
        while True:
            try:
                print('wait command')
                data = self.socket.recv(13)
                cm = self.getCommand(data)
                print('new command', data)
                if cm == Command.SEND_CLIENT_WORD_PREDICTION.value:
                    self.receiverWordPredict(data)
            except socket.error as error:
                print(error)
                print("Receiver error")
            except Exception as e:
                print(e)