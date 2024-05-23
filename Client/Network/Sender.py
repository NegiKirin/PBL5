<<<<<<< HEAD
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
=======
import socket

host = ''  # ip of server
port = 1234
from Client.Model import User

class Sender:
    def __init__(self):
        sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sender_socket.bind((host, port))
        sender_socket.listen(1100)
    def send(self,user:User):
        pass
>>>>>>> d40f260d798dedcaeb6eb52611c1e47372bac8fe
