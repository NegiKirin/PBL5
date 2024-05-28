import logging

from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import Qt, QEvent
from Client.Model.User import User
from Client.View.Home import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow, QWidget, QDialog, QFileDialog
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
        self.ui.btn_maximize.clicked.connect(self.window().showMaximized)

        self.username = None
        self.lastname = None
        self.firstname = None
        self.gender = None
        self.phone = None
        self.email = None
        self.password = None
        self.fileNameImage = None

        # self.ui.btn_profile.clicked.connect(self.read_user)
        self.ui.pushButton_13.clicked.connect(self.show_change_password)


    def back_to_manangement(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page)

    def show_page(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page)

    def show_change_password(self):
        self.w = window()
        self.w.show()
        self.w.ui.btn_change.clicked.connect(self.change_password)

    def change_password(self):
        if (self.password == self.w.ui.LEdit_email_register.text()):
            if (self.w.ui.LEdit_password_register.text() == self.w.ui.LEdit_confirm.text()):
                password = self.w.ui.LEdit_password_register.text()
                self.sender.change_password(self.username,password)
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
        self.sender.sendInforToEdit(self.username,edit_lastname,edit_firstname,edit_email,edit_gender,edit_phone)

    def back_to_home(self):
        #user = User("minhvulqd2003@gmail.com", "12345")
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

        filename, _ = QFileDialog.getOpenFileName(self, "Open Image")
        icon7 = QtGui.QIcon()
        print(filename)
        icon7.addPixmap(QtGui.QPixmap(filename), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ui.btn_avatar.setIcon(icon7)
        self.ui.btn_avatar.setIconSize(QtCore.QSize(60, 66))


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
            self.ui.lineEdit.setText(str(self.lastname))
            self.ui.lineEdit_2.setText(str(self.firstname))
            self.ui.lineEdit_3.setText(str(self.gender))
            self.ui.lineEdit_10.setText(str(self.phone))
            self.ui.lineEdit_11.setText(str(self.email))
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
        self.lastname = data['user'].lastname
        self.firstname = data['user'].firstname
        self.phone = data['user'].phone
        self.email = data['user'].email
        self.gender = data['user'].gender
        self.password = data['user'].password

    def mouseReleaseEvent(self, event):
        self.initial_pos = None
        super().mouseReleaseEvent(event)
        event.accept()

   
