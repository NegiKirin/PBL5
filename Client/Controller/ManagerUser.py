import logging

from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import Qt, QEvent
from PBL5.Client.Model.User import User
from PBL5.Client.View.Home import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow, QWidget, QDialog, QFileDialog
from PBL5.Client.View.change_password import window

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


class ManagerUser(QMainWindow):
    def __init__(self, sender=None):
        super().__init__()
        self.sender = sender
        self.ui = Ui_MainWindow()
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
        self.ui.pushButton_3.clicked.connect(self.back_to_manangement)

        self.ui.btn_substract.clicked.connect(self.window().showMinimized)

        self.ui.btn_pile_stack.clicked.connect(self.window().showNormal)

        self.ui.btn_maximize.clicked.connect(self.window().showMaximized)

        self.ui.btn_back_2.clicked.connect(self.back_to_learning)




        self.username = None
        self.phone = None
        self.email = None
        self.avatar = None

        # self.ui.btn_profile.clicked.connect(self.read_user)
        self.ui.pushButton_13.clicked.connect(self.show_change_password)
        self.ui.pushButton_14.clicked.connect(self.show_page)

    def back_to_manange(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page)

    def show_page(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page)

    def show_change_password(self):
        w = window()
        w.show()

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

   
