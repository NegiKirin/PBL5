#TODO : clear login user error
import logging
import sys
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

from Client.View.change_password import window

# them label vao duoi confirm password trong change_password
# set padding trong cac line edit o Profile
# doi username@gmail.com trong change_password
# btn_max
''''
       self.btn_maximize = QtWidgets.QPushButton(self.widget_4)
       self.btn_maximize.setMinimumSize(QtCore.QSize(50, 50))
       self.btn_maximize.setStyleSheet("background-color: rgba(255, 255, 255, 0);\n"
                                          "background-color:rgba(255,255,255,0);box-shadow:0,0,0,0}\n"
                                          "#btn_maximize:hover{\n"
                                          "background-color:rgb(0,160,255);\n"
                                          "")
       self.btn_maximize.setText("")

       self.btn_maximize.setObjectName("btn_maximize")

       self.horizontalLayout_3.addWidget(self.btn_maximize)
       icon1 = QtGui.QIcon()
       icon1.addPixmap(QtGui.QPixmap("../Client/View/Image/icons8-maximize-window-50.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
       self.btn_maximize.setIcon(icon1)
       self.btn_maximize.setIconSize(QtCore.QSize(23, 27))
       self.btn_maximize.setVisible(False)
    '''''


# def mask_image(imgdata, imgtype='png', size=64):
#     # Load image
#     image = QImage.fromData(imgdata, imgtype)
#
#     # convert image to 32-bit ARGB (adds an alpha
#     # channel ie transparency factor):
#     image.convertToFormat(QImage.Format_ARGB32)
#
#     # Crop image to a square:
#     imgsize = min(image.width(), image.height())
#     rect = QRect(
#         (image.width() - imgsize) / 2,
#         (image.height() - imgsize) / 2,
#         imgsize,
#         imgsize,
#     )
#
#     image = image.copy(rect)
#
#     # Create the output image with the same dimensions
#     # and an alpha channel and make it completely transparent:
#     out_img = QImage(imgsize, imgsize, QImage.Format_ARGB32)
#     out_img.fill(Qt.transparent)
#
#     # Create a texture brush and paint a circle
#     # with the original image onto the output image:
#     brush = QBrush(image)
#
#     # Paint the output image
#     painter = QPainter(out_img)
#     painter.setBrush(brush)
#
#     # Don't draw an outline
#     painter.setPen(Qt.NoPen)
#
#     # drawing circle
#     painter.drawEllipse(0, 0, imgsize, imgsize)
#
#     # closing painter event
#     painter.end()
#
#     # Convert the image to a pixmap and rescale it.
#     pr = QWindow().devicePixelRatio()
#     pm = QPixmap.fromImage(out_img)
#     pm.setDevicePixelRatio(pr)
#     size *= pr
#     pm = pm.scaled(size, size, Qt.KeepAspectRatio,
#                    Qt.SmoothTransformation)
#
#     # return back the pixmap data
#     return pm

class ManagerUser(QMainWindow):
    def __init__(self, sender=None):
        super().__init__()
        self.w = None
        self.sender = sender
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
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
        # self.ui.btn_avatar.clicked.connect(self.openImageDialog)
        # self.ui.btn_maximize.clicked.connect(self.window().showMaximized)

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

        self.list_user_in_user_widget = []
        self.list_user_in_rank_widget = []
        self.selected_user_id = None

        # self.ui.btn_profile.clicked.connect(self.read_user)
        self.ui.pushButton_13.clicked.connect(self.show_change_password)
        #open camera
        self.ui.btn_openCamera.clicked.connect(self.viewCameraToLearning)
        #close camera
        self.ui.btn_closeCamera.clicked.connect(self.closeCamera)

        imgpath = "../Client/View/Image/Ellipse 10.png"
        imgdata = open(imgpath, 'rb').read()
        self.cap = None
        self.timer = None

        #open page learning and this word

    def insertListRank(self, data):
        count = 1
        print(len(data))
        for i in data:

            dataImg = bytearray()
            dataImg.extend(i.dataImage)
            nparr = np.frombuffer(dataImg, np.uint8)
            self.img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            pixmap = self.display_image(cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB))

            newItem = QListWidgetItem()
            newItem.setSizeHint(QSize(1, 80))
            self.ui.listWidget.addItem(newItem)
            print('before add row')
            self.ui.addRow_bxh(str(count), i.username, str(i.point), pixmap, self.list_user_in_rank_widget)
            print('after add row')
            print(self.list_user_in_rank_widget[-1])
            self.ui.listWidget.setItemWidget(newItem, self.list_user_in_rank_widget[-1][0])
            if count != 1:
                self.list_user_in_rank_widget[-1][1].hide()
            count += 1
            print('add row succe')

    def closeCamera(self):
        pass
    def eventFilter(self, obj, event):
        if event.type() == QEvent.Leave:
            for i in self.list_user_in_user_widget:
                i[1].hide()

        elif event.type() == QEvent.Enter:
            pointer_to_widget = obj
            for list_item in self.list_user_in_user_widget:
                if list_item[0] == pointer_to_widget:
                    list_item[1].show()
                    self.selected_user_id = list_item[-1]
                    print(list_item[-1])

        return super(ManagerUser, self).eventFilter(obj, event)

    def viewCameraToLearning(self):

        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Error: Camera không thể mở")
            return

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(20)  # Cập nhật mỗi 20ms

    def update_frame(self):
        if self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                height, width, channel = frame.shape
                step = channel * width
                qImg = QImage(frame.data, width, height, step, QImage.Format_RGB888)
                self.ui.label_Screen2.setPixmap(QPixmap.fromImage(qImg))
            else:
                print("Error: Không thể đọc frame từ camera")
        else:
            print("Error: Camera không hoạt động")

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

    def insertWord(self, data):
        count = 1
        for i in data:
            if count <= len(data):
                button_name = f"btn_word{count}"
                button = self.findChild(QtWidgets.QPushButton, button_name)
                button.setText(i[0])
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
