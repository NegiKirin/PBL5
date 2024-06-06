import os
import pickle
import sys
import threading
import socket
import cv2
import numpy as np


current_directory = os.path.dirname(os.path.abspath(__file__)) + '\\'
sys.path.append(current_directory)
from ..Util.Command import Command
from ..DAO.UserDAO import UserDAO

BUFF_SIZE = 65536
HEADERSIZE = 10
COMMANDSIZE = 3

class Receiver:
    def __init__(self, conn, sender):
        self.socket = conn
        self.sender = sender
        self.active = True

        t = threading.Thread(target=self.run, args=())
        # t.setDaemon = True
        t.start()

    def getCommand(self, data):
        command = int(data[:COMMANDSIZE])
        return command
    def getSize(self, data):
        size = int(data[COMMANDSIZE:HEADERSIZE])
        return size

    def receiveUsernameAndPassword(self, data):
        try:
            # Todo:
            size = self.getSize(data)
            print(size)
            print(data)
            main_data = None
            full_msg = b''
            new_msg = True
            while True:
                msg = self.socket.recv(1024)
                if new_msg:
                    msg = data + msg
                    new_msg = False
                full_msg += msg
                print(full_msg)
                if len(full_msg) - HEADERSIZE - COMMANDSIZE == size:
                    main_data = pickle.loads(full_msg[HEADERSIZE+COMMANDSIZE:])
                    print(main_data)
                    break
            user = UserDAO().findByUsernameAndPassword(main_data)
            print(user)
            self.sender.sendUser(user)
        except Exception as e:
            print(e)

    def receiverInforRegister(self, data):
        try:
            # Todo:
            size = self.getSize(data)
            print(size)
            print(data)
            main_data = None
            full_msg = b''
            new_msg = True
            while True:
                msg = self.socket.recv(1024)
                if new_msg:
                    msg = data + msg
                    new_msg = False
                full_msg += msg
                print(full_msg)
                if len(full_msg) - HEADERSIZE - COMMANDSIZE == size:
                    main_data = pickle.loads(full_msg[HEADERSIZE+COMMANDSIZE:])
                    print(main_data)
                    break
            user = UserDAO().insertNewUser(main_data)
            print(user)
            self.sender.sendInforRegister(user)
        except Exception as e:
            print(e)


    def receiverInforEdit(self, data):
        try:
            # Todo:
            size = self.getSize(data)
            print(size)
            print(data)
            main_data = None
            full_msg = b''
            new_msg = True
            while True:
                msg = self.socket.recv(1024)
                if new_msg:
                    msg = data + msg
                    new_msg = False
                full_msg += msg
                print(full_msg)
                if len(full_msg) - HEADERSIZE - COMMANDSIZE == size:
                    main_data = pickle.loads(full_msg[HEADERSIZE+COMMANDSIZE:])
                    print(main_data)
                    break
            dataImage = bytearray()
            dataImage.extend(main_data['dataImage'])
            nparr = np.frombuffer(dataImage, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            username = main_data['username']
            path = 'E:/PBL_2/PBL5/Server/DB/' + username + '.png'
            cv2.imwrite(path, img)
            main_data['dataImage'] = path
            user = UserDAO().UpdateUser(main_data)
            self.sender.sendInforEdit(user)
        except Exception as e:
            print(e)

    def Change_Password(self, data):
        try:
            # Todo:
            size = self.getSize(data)
            print(size)
            print(data)
            main_data = None
            full_msg = b''
            new_msg = True
            while True:
                msg = self.socket.recv(1024)
                if new_msg:
                    msg = data + msg
                    new_msg = False
                full_msg += msg
                print(full_msg)
                if len(full_msg) - HEADERSIZE - COMMANDSIZE == size:
                    main_data = pickle.loads(full_msg[HEADERSIZE+COMMANDSIZE:])
                    print(main_data)
                    break
            user = UserDAO().Change_Password(main_data)
        except Exception as e:
            print(e)
    def deleteUser(self, data):
        try:
            # Todo:
            size = self.getSize(data)
            print(size)
            print(data)
            main_data = None
            full_msg = b''
            new_msg = True
            while True:
                msg = self.socket.recv(1024)
                if new_msg:
                    msg = data + msg
                    new_msg = False
                full_msg += msg
                print(full_msg)
                if len(full_msg) - HEADERSIZE - COMMANDSIZE == size:
                    main_data = pickle.loads(full_msg[HEADERSIZE+COMMANDSIZE:])
                    print(main_data)
                    break
            user = UserDAO().Change_Password(main_data)
        except Exception as e:
            print(e)

    def getListUser(self, data):
        try:
            # Todo:
            size = self.getSize(data)
            print(size)
            print(data)
            main_data = None
            full_msg = b''
            new_msg = True
            while True:
                msg = self.socket.recv(1024)
                if new_msg:
                    msg = data + msg
                    new_msg = False
                full_msg += msg
                print(full_msg)
                if len(full_msg) - HEADERSIZE - COMMANDSIZE == size:
                    main_data = pickle.loads(full_msg[HEADERSIZE + COMMANDSIZE:])
                    print(main_data)
                    break
            print("check")
            listUser = UserDAO().getAllUser()
            self.sender.sendAllUser(listUser)
        except Exception as e:
            print(e)
    def run(self):
        while True:
            try:
                print('wait command')
                data = self.socket.recv(13)
                cm = self.getCommand(data)
                print('new command', cm)
                if cm == Command.USERNAME_AND_PASSWORD.value:
                    self.receiveUsernameAndPassword(data)
                if cm == Command.SEND_SERVER_REGISTER.value:
                    self.receiverInforRegister(data)
                if cm == Command.SEND_SERVER_EDIT.value:
                    self.receiverInforEdit(data)
                if cm == Command.SEND_CHANGE_PASSWORD.value:
                    self.Change_Password(data)
                if cm == Command.SEND_DELETE.value:
                    self.deleteUser(data)
                if cm == Command.SEND_SERVER_GET_LIST_USER.value:
                    self.getListUser(data)
            except socket.error as error:
                print(error)
                self.active = False
                break
            except Exception as e:
                print(str(e))
                self.active = False
                break