import os
import pickle
import socket
import sys

current_directory = os.path.dirname(os.path.abspath(__file__)) + '\\'
sys.path.append(current_directory)
from ..Util.Command import Command

HEADERSIZE = 10
COMMANDSIZE = 3
class Sender:
    def __init__(self, conn):
        self.socket = conn
        self.active = True

    def sendUser(self, user):
        try:
            command = Command.USER.value
            data = {
                'user': user,
            }
            data = pickle.dumps(data)
            data = bytes(f'{command:<{COMMANDSIZE}}', 'utf-8') + bytes(f"{len(data):<{HEADERSIZE}}", 'utf-8') + data
            self.socket.sendall(data)
            return True
        except Exception as e:
            print(e)
            return False

    def sendInforRegister(self, user):
        try:
            command = Command.SEND_CLIENT_REGISTER.value
            data = {
                'user': user,
            }
            data = pickle.dumps(data)
            data = bytes(f'{command:<{COMMANDSIZE}}', 'utf-8') + bytes(f"{len(data):<{HEADERSIZE}}", 'utf-8') + data
            self.socket.sendall(data)
            return True
        except Exception as e:
            print(e)
            return False
    def sendInforEdit(self, user):
        try:
            command = Command.SEND_CLIENT_EDIT.value
            data = {
                'user': user,
            }
            data = pickle.dumps(data)
            data = bytes(f'{command:<{COMMANDSIZE}}', 'utf-8') + bytes(f"{len(data):<{HEADERSIZE}}", 'utf-8') + data
            self.socket.sendall(data)
            return True
        except Exception as e:
            print(e)
            return False
    def sendAllUser(self,user):
        try:
            command = Command.SEND_CLIENT_GET_LIST_USER.value
            data = pickle.dumps(user)
            data = bytes(f'{command:<{COMMANDSIZE}}', 'utf-8') + bytes(f"{len(data):<{HEADERSIZE}}", 'utf-8') + data
            self.socket.sendall(data)
            return True
        except Exception as e:
            print(e)
            return False

    def sendUserAfterDelete(self,users):
        try:
            command = Command.SEND_CLIENT_AFTER_DELETE.value
            data = pickle.dumps(users)
            data = bytes(f'{command:<{COMMANDSIZE}}', 'utf-8') + bytes(f"{len(data):<{HEADERSIZE}}", 'utf-8') + data
            self.socket.sendall(data)
            return True
        except Exception as e:
            print(e)
            return False