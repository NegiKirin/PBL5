#TODO : delete manager User
import logging
import os
import sys
import threading

import tensorflow as tf
import tensorflow_hub as hub
import os
import cv2
import numpy as np
from PyQt5.QtMultimedia import QMediaPlayer
from tqdm.notebook import tqdm
import cv2
import imutils
import numpy as np
from PyQt5 import QtGui, QtCore, QtWidgets

from PyQt5.QtCore import Qt, QEvent, QSize, QRect, QTimer
from PyQt5.QtGui import QPixmap, QImage, QBrush, QPainter, QWindow, QIcon
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QListWidgetItem

from Client.Util.round_image import round_image, round_image_icon
from Client.View.Home import Ui_MainWindow
from Client.View.Home import mask_image
from gtts import gTTS
import pygame
from io import BytesIO

from Client.View.change_password import window
current_directory = os.path.dirname(os.path.abspath(__file__)) + '\\'

EDGES = {
    (0, 1): 'm',
    (0, 2): 'c',
    (1, 3): 'm',
    (2, 4): 'c',
    (0, 5): 'm',
    (0, 6): 'c',
    (5, 7): 'm',
    (7, 9): 'm',
    (6, 8): 'c',
    (8, 10): 'c',
    (5, 6): 'y',
    (5, 11): 'm',
    (6, 12): 'c',
    (11, 12): 'y'
}

class ManagerUser(QMainWindow):
    def __init__(self, sender=None,movenet = None):
        super().__init__()
        self.text = None
        self.status = None
        self.timer_video = None
        self.cap_vid = None
        self.w = None
        self.sender = sender
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.movenet = movenet
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.ui.btn_edit.clicked.connect(self.Edit_Infor_User)
        self.ui.btn_home.clicked.connect(self.move_to_page_home)
        self.ui.btn_learning.clicked.connect(self.move_to_page_learning)
        self.ui.btn_profile.clicked.connect(self.move_to_page_profile)
        self.ui.pushButton_6.clicked.connect(self.show_page)

        self.ui.btn_avatar.clicked.connect(self.upload_image)
        self.ui.btn_exit.clicked.connect(self.exit)
        self.ui.pushButton_14.clicked.connect(self.back_to_home)
        self.ui.btn_back.clicked.connect(self.back_to_profile)
        self.ui.pushButton_3.clicked.connect(self.back_to_manangement)
        self.ui.pushButton_12.clicked.connect(self.back_to_learning)

        self.ui.btn_substract.clicked.connect(self.window().showMinimized)

        self.ui.btn_pile_stack.clicked.connect(self.window().showNormal)

        self.username = None
        self.lastname = None
        self.firstname = None
        self.gender = None
        self.phone = None
        self.email = None
        self.password = None
        self.fileNameImage = None
        self.img = None
        self.listUser = []
        self.listRank = []
        self.listWord = []
        self.id = None
        self.listAllWord = []
        self.listKeyPoints = []
        self.pointLearning = None
        self.mediaPlayer = QMediaPlayer()

        self.list_user_in_user_widget = []
        self.list_user_in_rank_widget = []
        self.list_word_in_list_widget = []
        self. list_word_in_widget_home = []
        self.selected_user_id = None
        self.selected_word = None
        self.selected_id_word = None
        self.ui.label_correct.hide()
        # self.ui.btn_profile.clicked.connect(self.read_user)
        self.ui.pushButton_13.clicked.connect(self.show_change_password)
        #open camera
        self.ui.btn_openCamera.clicked.connect(self.viewCameraToLearning)
        #close camera
        self.ui.btn_closeCamera.clicked.connect(self.closeCamera)
        #open page chosse word
        self.ui.btn_chosseWord.clicked.connect(self.move_page_chosse_word)
        #replay video
        self.ui.btn_rePlay.clicked.connect(self.replayVideo)
        imgpath = "../Client/View/Image/Ellipse 10.png"
        imgdata = open(imgpath, 'rb').read()
        self.cap = None
        self.timer = None

        # selected item in student list
        self.ui.list_word_widget.itemDoubleClicked.connect(self.openVideoToLearning)
        #change volume
        self.ui.horizontalSlider.valueChanged.connect(self.setVolume)
        # t = threading.Thread(target=self.update_frame, args=())
        # # t.setDaemon = True
        # t.start()
        #open page learning and this word

    def insertListRank(self, data):
        count = 1
        check = 0
        print(len(data))
        for i in data:
            if i.username == self.username:
                dataImg = bytearray()
                dataImg.extend(i.dataImage)
                nparr = np.frombuffer(dataImg, np.uint8)
                self.img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                pixmap = self.display_image(cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB))
                output = round_image(pixmap)
                self.ui.label_49.setPixmap(output)
                self.ui.label_48.setText(str(count))
                self.ui.label_46.setText(i.username)
                self.ui.label_47.setText(str(i.point))
                check += 1
            dataImg = bytearray()
            dataImg.extend(i.dataImage)
            nparr = np.frombuffer(dataImg, np.uint8)
            self.img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            pixmap = self.display_image(cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB))

            newItem = QListWidgetItem()
            newItem.setSizeHint(QSize(1, 80))
            self.ui.listWidget.addItem(newItem)
            self.ui.addRow_bxh(str(count), i.username, str(i.point), pixmap, self.list_user_in_rank_widget)
            print(self.list_user_in_rank_widget[-1])
            self.ui.listWidget.setItemWidget(newItem, self.list_user_in_rank_widget[-1][0])
            if count != 1:
                self.list_user_in_rank_widget[-1][1].hide()
            count += 1
        if check == 0:
            dataImg = bytearray()
            dataImg.extend(i.dataImage)
            nparr = np.frombuffer(dataImg, np.uint8)
            self.img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            pixmap = self.display_image(cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB))
            output = round_image(pixmap)
            self.ui.label_49.setPixmap(output)
            self.ui.label_48.setText("")
            self.ui.label_46.setText(self.username)
            self.ui.label_47.setText(str(0))

    # Text to speech
    def text_to_speech(self,text):
        print(text)
        # Tạo đối tượng gTTS với ngôn ngữ là tiếng Việt
        tts = gTTS(text=text, lang='en')

        # Tạo bộ đệm để lưu trữ âm thanh
        buffer = BytesIO()
        tts.write_to_fp(buffer)
        buffer.seek(0)
        # Khởi tạo pygame
        pygame.mixer.init()
        pygame.mixer.music.load(buffer)
        pygame.mixer.music.play()

        # Chờ phát xong âm thanh
        while pygame.mixer.music.get_busy():
            continue

    def closeCamera(self):
        # Giải phóng camera khi đóng ứng dụng
        self.cap.release()
        self.ui.label_Screen2.setPixmap(QtGui.QPixmap(current_directory + "../Image/z5461290588979_692bf1a21a79b202b016a475ef95d80d.jpg"))

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Leave:
            for i in self.list_user_in_user_widget:
                i[1].hide()

        elif event.type() == QEvent.Enter:
            if event.type() == QEvent.Enter:
                pointer_to_widget = obj
                for list_item in self.list_user_in_user_widget:
                    if list_item[0] == pointer_to_widget:
                        list_item[1].show()
                        self.selected_user_id = list_item[-1]
                        # print(list_item[-1])

                for list_item in self.list_word_in_list_widget:
                    if list_item[0] == pointer_to_widget:
                        self.selected_word = list_item[-2]
                        self.selected_id_word = list_item[-1]

                for list_item in self.list_word_in_widget_home:
                    if list_item[0] == pointer_to_widget:
                        # print("check")
                        self.text = list_item[0].text()
                        # print(self.text)
        return super(ManagerUser, self).eventFilter(obj, event)

    def move_page_chosse_word(self):
        self.sender.sendAllOfWord(self.id)
        while True:
            if self.listAllWord != []:
                break
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_score)
        self.insertWordOnPageChosseWord(self.listAllWord)
    def receiverAllWord(self,data):
        self.listAllWord = data

    def extractKeypoints(self, img, movenet):
        # Load the input image.
        # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        X = tf.expand_dims(img, axis=0)
        X = tf.cast(tf.image.resize_with_pad(X, 256, 256), dtype=tf.int32)
        # X = tf.cast(tf.image.resize_with_pad(X, 192, 192), dtype=tf.int32)
        outputs = movenet(X)
        keypoints = outputs['output_0'].numpy()
        # print(keypoints.shape)
        # max_key,key_val = keypoints[0,:,55].argmax(),keypoints[0,:,55].max()
        # max_points = keypoints[0,max_key,:]
        # max_points = max_points.astype(float)

        # keypoint = []
        #
        # for i in range(0,len(max_points)-5,3):
        #     keypoint.append([max_points[i],max_points[i+1],max_points[i+2]])

        return np.array(keypoints[0][0])

    def viewCameraToLearning(self):

        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            return

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(20)  # Cập nhật mỗi 20ms

    def draw_keypoints(self, frame, keypoints):
        for kp in keypoints:
            ky, kx = kp
            x, y = int(kx * frame.shape[1]), int(ky * frame.shape[0])
            # print('paint: x={}, y={}'.format(x, y))
            cv2.circle(frame, (x, y), 4, (0, 255, 0), -1)

    def draw_connections(self, frame, keypoints, edges):
        # y, x, c = frame.shape
        # shaped = np.squeeze(np.multiply(keypoints, [y,x,1]))

        for edge, color in edges.items():
            p1, p2 = edge
            y1, x1 = keypoints[p1]
            y2, x2 = keypoints[p2]
            y1 *= frame.shape[0]
            x1 *= frame.shape[1]
            y2 *= frame.shape[0]
            x2 *= frame.shape[1]

            cv2.line(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 2)

    def move_to_center(self, keypoints, center):
        center_temp = self.find_center(keypoints)
        # move = center - find_center(keypoints)
        move = [center[0] - center_temp[0], center[1] - center_temp[1]]
        for keypoint in keypoints:
            keypoint[0] += move[0]
            keypoint[1] += move[1]
        return keypoints

    def find_center(self, keypoints):
        return [(keypoints[5][0] + keypoints[6][0]) / 2, (keypoints[5][1] + keypoints[6][1]) / 2]

    def find_x(self, A, B, mean):
        c = np.sqrt((A[0] - B[0]) ** 2 + (A[1] - B[1]) ** 2)
        # print(f'c={c}')
        x = (c - mean) / (c + 1e-1)
        return x

    def scale_keypoint(self, keypoints, mean):
        x = self.find_x(keypoints[0], keypoints[1], mean)
        print(x)
        for i in range(1, len(keypoints)):
            if i == 0:
                continue
            # print(i)
            # kx = x * (keypoints[0][0]- keypoints[i][0])
            # ky = x * (keypoints[0][1]- keypoints[i][1])

            kx = x * (keypoints[i][0] - keypoints[0][0])
            ky = x * (keypoints[i][1] - keypoints[0][1])

            # print(f'kx={kx}, ky={ky}')
            keypoints[i] = [keypoints[i][0] - kx, keypoints[i][1] - ky]
        return keypoints

    def normKeypoint(self, keypoints, dis_mean, center):
        keypoints = self.scale_keypoint(keypoints, dis_mean)
        keypoints = self.move_to_center(keypoints, center)
        return keypoints
    def update_frame(self):
        if self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                keypoints = self.extractKeypoints(frame, self.movenet)
                keypoints = keypoints[:13, :2]
                print(keypoints.shape)

                keypoints = self.normKeypoint(keypoints, dis_mean=0.10192956195594993, center=(0.4803588539361954, 0.4331198185682297))

                self.draw_keypoints(frame, keypoints)
                self.draw_connections(frame, keypoints, EDGES)


                self.listKeyPoints.append(keypoints)
                # print(keypoints.shape ,len(self.listKeyPoints))
                if len(self.listKeyPoints) == 58:
                    self.sender.sendKeyPoint(self.listKeyPoints)
                    self.listKeyPoints = []
                height, width, channel = frame.shape
                step = channel * width
                qImg = QImage(frame.data, width, height, step, QImage.Format_RGB888)
                self.ui.label_Screen2.setPixmap(QPixmap.fromImage(qImg))

    def back_to_manangement(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page)

    def deleteUser(self):
        self.sender.deleteUser(self.selected_user_id)
        # print("delete" + self.selected_user_id)

    def receiverListUser(self, data):
        self.listUser = data

    def insertListUser(self, data):
        # print(data)
        self.ui.listWidget_2.clear()
        self.list_user_in_user_widget.clear()
        for i, user in enumerate(data):
            dataImg = bytearray()
            dataImg.extend(user.dataImage)
            nparr = np.frombuffer(dataImg, np.uint8)
            self.img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            pixmap = self.display_image(cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB))
            newItem = QListWidgetItem()
            newItem.setSizeHint(QSize(1, 80))
            self.ui.listWidget_2.addItem(newItem)
            self.row_widget = self.ui.addRow(str(user.id), user.username, user.email,
                                             str(user.phone), pixmap, self.list_user_in_user_widget)
            self.ui.listWidget_2.setItemWidget(newItem, self.row_widget)
            self.list_user_in_user_widget[i][0].installEventFilter(self)
            # event delete button
            self.list_user_in_user_widget[i][1].clicked.connect(self.deleteUser)
            # self.ui.pushButton__.clicked.connect(self.remove_item)

    def setVolume(self, value):
        # Cập nhật âm lượng của pygame
        pygame.mixer.music.set_volume(value / 100.0)
    def display_Word_Predict(self,data,point):
        count = 0
        self.ui.LEdit_Predict.setText(data)
        self.pointLearning = int(float(point) * 100)
        self.text_to_speech(data)
        print(self.selected_id_word)
        print(self.pointLearning)
        print(self.id)
        self.ui.label_Screen2.setPixmap(QtGui.QPixmap("E:/PBL_2/PBL5/Client/View/Image/z5461290588979_692bf1a21a79b202b016a475ef95d80d.jpg"))
        if data == self.selected_word:
            self.ui.label_correct.show()
            print("check")
            for i in self.listWord:
                print("hello")
                print(i[0])
                if self.selected_word == i[0]:
                    count += 1
            if count == 0:
                print('send word')
                self.sender.sendWordAfterLearning(self.id, self.selected_id_word, self.pointLearning)
            if count != 0:
                print("update")
                self.sender.updatePoint(self.id, self.selected_id_word, self.pointLearning)
            self.closeCamera()
    def insertWordOnPageChosseWord(self, data):
        # print(data)
        self.ui.list_word_widget.clear()
        self.list_word_in_list_widget.clear()

        for i, user in enumerate(data):
            if self.listWord == []:
                newItem = QListWidgetItem()
                newItem.setSizeHint(QSize(1, 80))
                self.ui.list_word_widget.addItem(newItem)
                self.row_word_widget = self.ui.addRow_word(str(user.id), user.word, str(user.point), 'new word',
                                                           self.list_word_in_list_widget)
                self.ui.list_word_widget.setItemWidget(newItem, self.row_word_widget)
                self.list_word_in_list_widget[i][0].installEventFilter(self)
            else:

                for j in self.listWord:
                    if user.word == j[0]:
                        self.status = True
                        break
                    else:
                        self.status = False
                if self.status == False:
                    newItem = QListWidgetItem()
                    newItem.setSizeHint(QSize(1, 80))
                    self.ui.list_word_widget.addItem(newItem)
                    self.row_word_widget = self.ui.addRow_word(str(user.id), user.word, str(user.point), 'new word', self.list_word_in_list_widget)
                    self.ui.list_word_widget.setItemWidget(newItem, self.row_word_widget)
                    self.list_word_in_list_widget[i][0].installEventFilter(self)
                if self.status == True:
                    newItem = QListWidgetItem()
                    newItem.setSizeHint(QSize(1, 80))
                    self.ui.list_word_widget.addItem(newItem)
                    self.row_word_widget = self.ui.addRow_word(str(user.id), user.word, str(user.point), 'review',
                                                               self.list_word_in_list_widget)
                    self.ui.list_word_widget.setItemWidget(newItem, self.row_word_widget)
                    self.list_word_in_list_widget[i][0].installEventFilter(self)
            # event delete button
    def replayVideo(self):
        print(self.selected_word)
        self.openPathVideoToLearning(self.selected_word)

    def openVideoToLearning(self):
        try:
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_learning)
            self.openPathVideoToLearning(self.selected_word)
            self.ui.LEdit_Word.setText(self.selected_word)
        except Exception as e:
            print(e)
    def openPathVideoToLearning(self,word):
        try:
            path = f'E:/PBL_2/PBL5/Client/DB/{word}.mp4'
            print(path)
            self.selected_word = word
            self.cap_vid = cv2.VideoCapture(path)
            if not self.cap_vid.isOpened():
                return

            self.timer_video = QTimer()
            self.timer_video.timeout.connect(self.update_frame_Screen1)
            self.timer_video.start(20)
        except Exception as e:
            print(e)
    def update_frame_Screen1(self):
        try:
            if self.cap_vid.isOpened():
                ret, frame = self.cap_vid.read()
                if ret:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    height, width, channel = frame.shape
                    step = channel * width
                    qImg = QImage(frame.data, width, height, step, QImage.Format_RGB888)
                    self.ui.label_Screen1.setPixmap(QPixmap.fromImage(qImg))
        except Exception as e:
            print(e)

    def insertRankAndWordAfterLogin(self):
        while True:
            if self.listRank != []:
                print('insertRankAndWordAfterLogin', self.listRank)
                break
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_profile)
        self.insertListRank(self.listRank)
        self.insertWord(self.listWord)

    def sendRequestToOpenVideo(self,text):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_learning)

    def remove_item(self):
        try:
            item = self.ui.listWidget_2.itemClicked()
            row = self.ui.listWidget_2.row(item)
            self.ui.listWidget_2.takeItem(row)
        except Exception as e:
            print(e)

    # def insertAccountToListWidget(self):
    #     self.newItem.setSizeHint(QSize(1, 80))
    #     self.ui.listWidget_2.addItem(self.newItem)
    #     self.ui.listWidget_2.setItemWidget(self.newItem,
    #                                        self.ui.addRow(str(1), "Pham Doan Minh Hieu", "hieuprobanh@gmail.com",
    #                                                       "0762649422"))
    def show_page(self):
        try:
            self.sender.getListUser(self.username)
            while True:
                if self.listUser != []:
                    break

            self.ui.stackedWidget.setCurrentWidget(self.ui.page)
            self.insertListUser(self.listUser)
        except Exception as e:
            print(e)

    # def clearListWidet(self,data):
    #     self.ui.listWidget_2.clear()
    #     self.insertListUser(data)
    def show_change_password(self):
        self.w = window()
        self.w.show()
        self.w.ui.btn_change.clicked.connect(self.change_password)

    def change_password(self):
        if self.password == self.w.ui.LEdit_email_register.text():
            if self.w.ui.LEdit_password_register.text() == self.w.ui.LEdit_confirm.text():
                password = self.w.ui.LEdit_password_register.text()
                self.sender.change_password(self.username, password)
                self.w.hide()

    def back_to_profile(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_home)

    def back_to_learning(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_learning)

    def Edit_Infor_User(self):
        edit_lastname = self.ui.lineEdit.text()
        edit_firstname = self.ui.lineEdit_2.text()
        edit_gender = self.ui.lineEdit_3.text()
        edit_phone = self.ui.lineEdit_10.text()
        edit_email = self.ui.lineEdit_11.text()
        print(self.fileNameImage)
        self.sender.sendInforToEdit(self.username, edit_lastname, edit_firstname, edit_email, edit_gender, edit_phone,
                                    self.fileNameImage)

    def back_to_home(self):

        self.ui.stackedWidget.setCurrentWidget(self.ui.page_profile)

    def exit(self):
        # os.system(cmd)
        QtCore.QCoreApplication.instance().quit()

    def window_state_changed(self, state):
        if state == Qt.WindowState.WindowMaximized:
            self.ui.btn_pile_stack.setVisible(True)
            self.ui.btn_maximize.setVisible(False)
        else:
            self.ui.btn_maximize.setVisible(True)
            self.ui.btn_pile_stack.setVisible(False)

    def upload_image(self):

        self.fileNameImage, _ = QFileDialog.getOpenFileName(self, "Open Image")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(self.fileNameImage), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ui.btn_avatar.setIcon(icon7)
        self.ui.btn_avatar.setIconSize(QtCore.QSize(60, 66))

    def move_to_page_home(self):
        try:
            self.sender.sendListRank(self.id)
            self.ui.listWidget.clear()
            while True:
                if self.listRank != []:
                    break
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_profile)
            self.insertListRank(self.listRank)
            self.insertWord(self.listWord)
        except Exception as e:
            logging.error("An error occurred", exc_info=True)
            print(e)
    def click_Word_To_Learning(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_learning)
        self.openPathVideoToLearning(self.text)
    def insertWord(self, data):
        count = 1
        if data == []:
            for i in range(1,10):
                button_name = f"btn_word{i}"
                button = self.findChild(QtWidgets.QPushButton, button_name)
                button.hide()
        for i in data:
            if count <= len(data):
                button_name = f"btn_word{count}"
                button = self.findChild(QtWidgets.QPushButton, button_name)
                button.setText(i[0])
                button.installEventFilter(self)
                self.list_word_in_widget_home.append([button])
                button.clicked.connect(self.click_Word_To_Learning)
                count += 1
            if count > len(data):
                for j in range(count, 10):
                    button_name = f"btn_word{j}"
                    button = self.findChild(QtWidgets.QPushButton, button_name)
                    button.hide()


    def move_to_page_learning(self):
        try:
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_learning)
        except Exception as e:
            print(f"An error occurred: {e}")

    def move_to_page_profile(self):
        try:
            self.ui.lineEdit.setText(str(self.lastname))
            self.ui.lineEdit_2.setText(str(self.firstname))
            self.ui.lineEdit_3.setText(str(self.gender))
            self.ui.lineEdit_10.setText(str(self.phone))
            self.ui.lineEdit_11.setText(str(self.email))
            pixmap = self.display_image(cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB))
            self.ui.lbl_name.setText(str(self.username))
            self.ui.lbl_email.setText(str(self.email))

            # output = round_image(pixmap)
            icon = QIcon(pixmap)
            self.ui.btn_avatar.setIcon(icon)
            # self.ui.btn_avatar.setIconSize(pixmap.rect().size())
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_home)

        except Exception as e:
            print(e)

    def changeEvent(self, event):
        if event.type() == QEvent.Type.WindowStateChange:
            self.window_state_changed(self.windowState())
        super().changeEvent(event)
        event.accept()

    # def window_state_changed(self, state):
    # self.ui.btn_pile_stack.setVisible(state == Qt.WindowState.WindowMaximized)
    # self.ui.btn_maximize.setVisible(state != Qt.WindowState.WindowMaximized)
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.initial_pos = event.pos()
        super().mousePressEvent(event)
        event.accept()

    def listRankUser(self, data):
        self.listRank = data

    def receiverlistWord(self, data):
        self.listWord = data

    def mouseMoveEvent(self, event):
        if self.initial_pos is not None:
            delta = event.pos() - self.initial_pos
            self.window().move(
                self.window().x() + delta.x(),
                self.window().y() + delta.y(),
            )
        super().mouseMoveEvent(event)
        event.accept()

    def receiveDataUser(self, data):
        dataImg = bytearray()
        dataImg.extend(data['user'].dataImage)
        nparr = np.frombuffer(dataImg, np.uint8)
        self.img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        self.id = data['user'].id
        self.username = data['user'].username
        self.lastname = data['user'].lastname
        self.firstname = data['user'].firstname
        self.phone = data['user'].phone
        self.email = data['user'].email
        self.gender = data['user'].gender
        self.password = data['user'].password
        pixmap = self.display_image(cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB))
        output = round_image(pixmap)
        self.ui.label_avatar.setPixmap(output)
        icon = QIcon(pixmap)
        self.ui.btn_avatar.setIcon(icon)

    def mouseReleaseEvent(self, event):
        self.initial_pos = None
        super().mouseReleaseEvent(event)
        event.accept()

    def display_image(self, img):
        height, width, channel = img.shape
        bytes_per_line = 3 * width
        q_img = QImage(img.data, width, height, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_img)
        return pixmap
