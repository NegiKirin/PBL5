import logging

from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import Qt, QEvent
from Client.Model.User import User
from Client.View.Home import Home
from PyQt5.QtWidgets import QMainWindow, QWidget, QDialog, QFileDialog

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
       '''''


class ManagerUser(QMainWindow):
    def __init__(self, sender=None):
        super().__init__()
        self.sender = sender
        self.ui = Home()
        self.ui.setupUi(self)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.ui.btn_edit.clicked.connect(self.Edit_Infor_User)
        self.ui.btn_home.clicked.connect(self.move_to_page_home)
        self.ui.btn_learning.clicked.connect(self.move_to_page_learning)
        self.ui.btn_profile.clicked.connect(self.move_to_page_profile)
        self.ui.btn_avatar.clicked.connect(self.upload_image)
        self.ui.btn_exit.clicked.connect(self.exit)
        self.ui.pushButton_6.clicked.connect(self.back_to_home)
        self.ui.btn_back.clicked.connect(self.back_to_profile)
        self.ui.pushButton_3.clicked.connect(self.back_to_learning)
        self.ui.btn_edit.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.ui.btn_substract.clicked.connect(self.window().showMinimized)
        self.ui.btn_substract.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(
            "../Client/View/Image/icons8-reduce-50.png"),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ui.btn_substract.setIcon(icon)
        self.ui.btn_substract.setIconSize(QtCore.QSize(23, 29))

        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("../Client/View/Image/icons8-restore-window-50.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)

        self.ui.btn_pile_stack.setIcon(icon1)
        self.ui.btn_pile_stack.setIconSize(QtCore.QSize(23, 27))
        self.ui.btn_pile_stack.clicked.connect(self.window().showNormal)
        self.ui.btn_pile_stack.setVisible(False)
        self.ui.btn_pile_stack.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.ui.btn_pile_stack.setVisible(False)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("../Client/View/Image/icons8-maximize-window-50.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ui.btn_maximize.setIcon(icon1)
        self.ui.btn_maximize.setIconSize(QtCore.QSize(23, 27))

        self.ui.btn_maximize.clicked.connect(self.window().showMaximized)
        self.ui.btn_maximize.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("../Client/View/Image/icons8-video-camera-50.png"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        self.ui.btn_learning.setIcon(icon5)
        self.ui.btn_learning.setIconSize(QtCore.QSize(25, 25))
        self.ui.btn_learning.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.ui.btn_exit.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        icon2 = QtGui.QIcon()
        icon2.addPixmap(
            QtGui.QPixmap(
                "../Client/View/Image/icons8-close-window-50.png"),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ui.btn_exit.setIcon(icon2)
        self.ui.btn_exit.setIconSize(QtCore.QSize(23, 28))
        self.ui.btn_substract.clicked.connect(self.window().showMinimized)
        self.ui.btn_substract.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("../Client/View/Image/icons8-home-30.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ui.btn_home.setIcon(icon3)
        self.ui.btn_home.setIconSize(QtCore.QSize(25, 25))

        self.ui.btn_home.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.ui.pushButton_3.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.ui.pushButton_6.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.ui.btn_back.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("../Client/View/Image/Group 4.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ui.btn_back.setIcon(icon6)
        self.ui.btn_back.setIconSize(QtCore.QSize(30, 30))
        self.ui.label_Screen1.setPixmap(
            QtGui.QPixmap("../Client/View/Image/z5461290588979_692bf1a21a79b202b016a475ef95d80d.jpg"))
        self.ui.label_Screen1.setScaledContents(True)
        self.ui.label_Screen1.setAlignment(QtCore.Qt.AlignCenter)
        self.ui.label_Screen2.setPixmap(
            QtGui.QPixmap("../Client/View/Image/z5461290588979_692bf1a21a79b202b016a475ef95d80d.jpg"))
        self.ui.label_Screen2.setScaledContents(True)
        self.ui.label_Screen2.setAlignment(QtCore.Qt.AlignCenter)
        self.ui.label_avatar.setPixmap(QtGui.QPixmap("../Client/View/Image/Ellipse_10.jpg"))
        self.ui.label_avatar.setScaledContents(True)
        self.ui.label_avatar.setAlignment(QtCore.Qt.AlignCenter)
        self.ui.label_66.setPixmap(QtGui.QPixmap("../Client/View/Image/bi_volume-down-fill.png"))
        self.ui.label_55.setPixmap(QtGui.QPixmap("../Client/View/Image/startup--shop-rocket-launch-startup.png"))
        self.ui.label_55.setAlignment(QtCore.Qt.AlignCenter)
        self.ui.label_icon.setPixmap(QtGui.QPixmap("../Client/View/Image/Group 37.png"))
        self.ui.label_50.setPixmap(QtGui.QPixmap("../Client/View/Image/Vector_2.png"))
        self.ui.label_50.setAlignment(QtCore.Qt.AlignCenter)
        self.ui.label_20.setPixmap(QtGui.QPixmap("../Client/View/Image/image 1.png"))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("../Client/View/Image/icons8-account-50.png"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        self.ui.btn_profile.setIcon(icon4)
        self.ui.btn_profile.setIconSize(QtCore.QSize(25, 25))
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("../Client/View/Image/Ellipse_11.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ui.btn_avatar.setIcon(icon7)
        self.ui.btn_avatar.setIconSize(QtCore.QSize(60, 66))
        self.ui.btn_profile.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.ui.pushButton_3.setIcon(icon6)
        self.ui.pushButton_3.setIconSize(QtCore.QSize(30, 30))
        self.ui.pushButton_6.setIcon(icon6)
        self.ui.pushButton_6.setIconSize(QtCore.QSize(30, 30))
        self.ui.label.setPixmap(QtGui.QPixmap("../Client/View/Image/Fox.png"))
        self.ui.label.setAlignment(QtCore.Qt.AlignCenter)
        self.ui.btn_Next.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        self.button = [self.ui.pushButton_4, self.ui.pushButton_2, self.ui.pushButton, self.ui.pushButton_8,
                       self.ui.pushButton_7, self.ui.pushButton_5, self.ui.pushButton_9, self.ui.pushButton_10,
                       self.ui.pushButton_11]
        for i in self.button:
            i.clicked.connect(self.show_video)
        self.username = None
        self.phone = None
        # self.ui.btn_profile.clicked.connect(self.read_user)

    def back_to_profile(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_home)

    def back_to_learning(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_learning)

    def Edit_Infor_User(self):
        edit_fullname = self.ui.lineEdit.text()
        edit_nickname = self.ui.lineEdit_2.text()
        edit_gender = self.ui.lineEdit_3.text()
        edit_firstname = self.ui.lineEdit_10.text()
        edit_phone = self.ui.lineEdit_11.text()
        edit_email = self.ui.lineEdit_12.text()
        self.sender.sendInforToEdit(edit_fullname, edit_phone)
    def back_to_home(self):
        user = User("minhvulqd2003@gmail.com", "12345")
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_profile)
        lst = user.get_stack_word()

        for i in range(len(lst)):
            self.button[i].setText(lst[i])

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
        user = User('minhvulqd2003@gmail.com', '12345')

        filename, _ = QFileDialog.getOpenFileName(self, "Open Image")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(filename), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ui.btn_avatar.setIcon(icon7)
        self.ui.btn_avatar.setIconSize(QtCore.QSize(60, 66))
        user.set_image(filename)


    def move_to_page_home(self):
        try:
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_profile)
            # self.ui.stackedWidget.setCurrentWidget(self.ui.page_home)
        except Exception as e:
            logging.error("An error occurred", exc_info=True)
            print(e)

    def move_to_page_learning(self):
        try:
            # self.ui.lineEdit.setText(str(self.username))
            # self.ui.lineEdit_11.setText(str(self.phone))
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_learning)
        except Exception as e:
            print(f"An error occurred: {e}")

    def move_to_page_profile(self):
         try:
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
        self.username = data['user'].username
        self.phone = data['user'].phone
        # self.username = data['user'][0][2]
        # self.phone = data['user'][0][4]
        # self.test()
    def mouseReleaseEvent(self, event):
        self.initial_pos = None
        super().mouseReleaseEvent(event)
        event.accept()

   
