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

    def sendInforRegister(self, username, password, phone):
        # Todo:
        try:
            command = Command.SEND_SERVER_REGISTER.value
            data = {
                'username': username,
                'password': password,
                'phone': phone,
            }
            data = pickle.dumps(data)
            data = bytes(f'{command:<{COMMANDSIZE}}', 'utf-8') + bytes(f"{len(data):<{HEADERSIZE}}", 'utf-8') + data
            self.socket.sendall(data)
            print("send succeed")
            return True
        except Exception as e:
            print(e)
            return False

    def sendInforToEdit(self, username, lastname, firstname, email, gender, phone, fileNameImage):
        try:
            img = cv2.imread(fileNameImage)
            _, img_encoded = cv2.imencode('.jpg', img)
            dataImage = img_encoded.tobytes()
            print(dataImage)
            command = Command.SEND_SERVER_EDIT.value
            data = {
                'username': username,
                'lastname': lastname,
                'firstname': firstname,
                'email': email,
                'gender': gender,
                'phone': phone,
                'dataImage': dataImage,
            }
            data = pickle.dumps(data)
            data = bytes(f'{command:<{COMMANDSIZE}}', 'utf-8') + bytes(f"{len(data):<{HEADERSIZE}}", 'utf-8') + data
            self.socket.sendall(data)
            print("send succeed")
            return True
        except Exception as e:
            print(e)
            return False

    def change_password(self, username, password):
        try:
            command = Command.SEND_CHANGE_PASSWORD.value
            data = {
                'username': username,
                'password': password,
            }
            data = pickle.dumps(data)
            data = bytes(f'{command:<{COMMANDSIZE}}', 'utf-8') + bytes(f"{len(data):<{HEADERSIZE}}", 'utf-8') + data
            self.socket.sendall(data)
            print("send succeed")
            return True
        except Exception as e:
            print(e)
            return False


    def deleteUser(self,username):
        try:
            command = Command.SEND_DELETE.value
            data = {
                'username': username,
            }
            data = pickle.dumps(data)
            data = bytes(f'{command:<{COMMANDSIZE}}', 'utf-8') + bytes(f"{len(data):<{HEADERSIZE}}", 'utf-8') + data
            self.socket.sendall(data)
            print("send succeed")
            return True
        except Exception as e:
            print(e)
            return False

    def getListUser(self,username):
        try:
            command = Command.SEND_SERVER_GET_LIST_USER.value
            data = {
                'username': username,
            }
            data = pickle.dumps(data)
            data = bytes(f'{command:<{COMMANDSIZE}}', 'utf-8') + bytes(f"{len(data):<{HEADERSIZE}}", 'utf-8') + data
            self.socket.sendall(data)
            print("send succeed")
            return True
        except Exception as e:
            print(e)
            return False

