import os
import pickle
import sys
import threading
import socket
import cv2
import numpy as np
import torch
import torch.nn.functional as F
current_directory = os.path.dirname(os.path.abspath(__file__)) + '\\'
sys.path.append(current_directory)
from ..Util.Command import Command
from ..DAO.UserDAO import UserDAO


BUFF_SIZE = 65536
HEADERSIZE = 10
COMMANDSIZE = 3

class Receiver:
    def __init__(self, conn, sender,model, device):
        self.socket = conn
        self.sender = sender
        self.active = True
        self.model = model
        self.device = device
        self.annotations = {1: 'Opaque',
                       2: 'Red',
                       3: 'Green',
                       4: 'Yellow',
                       5: 'Bright',
                       6: 'Light-blue',
                       7: 'Colors',
                       8: 'Pink',
                       9: 'Women',
                       10: 'Enemy',
                       11: 'Son',
                       12: 'Man',
                       13: 'Away',
                       14: 'Drawer',
                       15: 'Born',
                       16: 'Learn',
                       17: 'Call',
                       18: 'Skimmer',
                       19: 'Bitter',
                       20: 'Sweet milk',
                       21: 'Milk',
                       22: 'Water',
                       23: 'Food',
                       24: 'Argentina',
                       25: 'Uruguay',
                       26: 'Country',
                       27: 'Last name',
                       28: 'Where',
                       29: 'Mock',
                       30: 'Birthday',
                       31: 'Breakfast',
                       32: 'Photo',
                       33: 'Hungry',
                       34: 'Map',
                       35: 'Coin',
                       36: 'Music',
                       37: 'Ship',
                       38: 'None',
                       39: 'Name',
                       40: 'Patience',
                       41: 'Perfume',
                       42: 'Deaf',
                       43: 'Trap',
                       44: 'Rice',
                       45: 'Barbecue',
                       46: 'Candy',
                       47: 'Chewing-gum',
                       48: 'Spaghetti',
                       49: 'Yogurt',
                       50: 'Accept',
                       51: 'Thanks',
                       52: 'Shut down',
                       53: 'Appear',
                       54: 'To land',
                       55: 'Catch',
                       56: 'Help',
                       57: 'Dance',
                       58: 'Bathe',
                       59: 'Buy',
                       60: 'Copy',
                       61: 'Run',
                       62: 'Realize',
                       63: 'Give',
                       64: 'Find',
                       65: 'Nothing',
                       }
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
                    main_data = pickle.loads(full_msg[HEADERSIZE+COMMANDSIZE:])
                    break

            user = UserDAO().findByUsernameAndPassword(main_data)

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
            path = '../DB/' + username + '.png'
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
            users = UserDAO().Delete_User(main_data)
            self.sender.sendUserAfterDelete(users)
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

    def getListRank(self,data):
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
            listUser = UserDAO().getListRank(main_data)
            word = UserDAO().getWord(main_data)
            self.sender.sendListRank(listUser,word)
        except Exception as e:
            print(e)

    def getAllOfWord(self,data):
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
            listWord = UserDAO().getALLWord(main_data)
            self.sender.sendAllWord(listWord)
        except Exception as e:
            print(e)



    def receiverKeyPoints(self,data):
        try:
            # Todo:
            size = self.getSize(data)
            # print(size)
            # print(data)
            main_data = None
            full_msg = b''
            new_msg = True
            while True:
                msg = self.socket.recv(1024)
                if new_msg:
                    msg = data + msg
                    new_msg = False
                full_msg += msg
                # print(full_msg)
                if len(full_msg) - HEADERSIZE - COMMANDSIZE == size:
                    main_data = pickle.loads(full_msg[HEADERSIZE + COMMANDSIZE:])
                    break

            # Chuyển kiểu dữ liệu thành mảng numpy
            keypoints = np.array(main_data['keyPoints']) # (58, 17, 2)

            # Chỉ lấy 6 điểm
            keypoints = keypoints[:, 0:13, 0:2] # (58, 13, 2)

            # Chuyển về định dạng đúng


            # In ra kết quả
            # print(f'keypoints: {main_data.shape}')

            # Chuyển tính toán vào cuda
            keypoints = torch.from_numpy(keypoints).to(device=self.device)

            keypoints = keypoints.unsqueeze(0) # (1, 58, 13, 2) => (1, 2, 58, 13)
            keypoints = keypoints.permute(0, 3, 1, 2)

            print(keypoints.shape)

            # Dự đoán kết quả:
            output = self.model(keypoints)

            output = F.softmax(output, dim=1)

            # Lấy giá trị dự đoán cao nhất
            value, predict = torch.max(output.data, 1)

            print(f'=>Hight Softmax Value: {value.item()}')

            # In ra giá trị dự đoán
            # print(f'=> output: {self.annotations[predict.item()]}')
            self.sender.sendWordPrediction(self.annotations[predict.item() + 1],value.item())
            # self.sender.sendAllWord(word)
        except Exception as e:
            print(e)

    def receiverWordAfterLearning(self,data):
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
            message = UserDAO().insertWordAfterLearning(main_data)
        except Exception as e:
            print(e)

    def receiverUpdatePoint(self,data):
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
            message = UserDAO().updatePoint(main_data)
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
                if cm == Command.SEND_SERVER_DELETE.value:
                    self.deleteUser(data)
                if cm == Command.SEND_SERVER_GET_LIST_USER.value:
                    self.getListUser(data)
                if cm == Command.SEND_SERVER_LIST_RANK.value:
                    self.getListRank(data)
                if cm == Command.SEND_SERVER_ALL_WORD.value:
                    self.getAllOfWord(data)
                if cm == Command.SEND_SERVER_KEYPOINT.value:
                    self.receiverKeyPoints(data)
                if cm == Command.SEND_SERVER_ADD_WORD_AFTER_LEARNING.value:
                    self.receiverWordAfterLearning(data)
                if cm == Command.SEND_SERVER_UPDATE_POINT.value:
                    self.receiverUpdatePoint(data)
            except socket.error as error:
                print(error)
                self.active = False
                break
            except Exception as e:
                print(str(e))
                self.active = False
                break