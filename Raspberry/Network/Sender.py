import pickle
import threading
import socket

import cv2

from Client.Util.Command import Command

BUFF_SIZE = 65536
HEADERSIZE = 10
COMMANDSIZE = 3


class Sender:
    def __init__(self, conn):
        self.socket = conn
        # t = threading.Thread(target=self.run, args=())
        # t.setDaemon = True
        # t.start()

    def sendUsernameAndPassword(self, username, password):
        # Todo:
        try:
            command = Command.USERNAME_AND_PASSWORD.value
            data = {
                'username': username,
                'password': password,
            }
            data = pickle.dumps(data)
            data = bytes(f'{command:<{COMMANDSIZE}}', 'utf-8') + bytes(f"{len(data):<{HEADERSIZE}}", 'utf-8') + data
            self.socket.sendall(data)
            return True
        except Exception as e:
            print(e)
            return False

    def sendKeyPoint(self,list):
        try:
            command = Command.SEND_SERVER_KEYPOINT.value
            print("sended")
            data = {
                'keyPoints': list,
            }
            data = pickle.dumps(data)
            data = bytes(f'{command:<{COMMANDSIZE}}', 'utf-8') + bytes(f"{len(data):<{HEADERSIZE}}", 'utf-8') + data
            self.socket.sendall(data)
            print("send succeed")
            return True
        except Exception as e:
            print(e)
            return False
