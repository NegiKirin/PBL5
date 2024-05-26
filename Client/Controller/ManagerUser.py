import logging
logging.basicConfig(level=logging.DEBUG)
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QEvent
from Client.Model import User
from Client.View.Home import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow


class ManagerUser(QMainWindow):
    def __init__(self,sender = None):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.ui.btn_home.clicked.connect(self.move_to_page_home)
        self.ui.btn_learning.clicked.connect(self.move_to_page_learning)
        self.ui.btn_edit.clicked.connect(self.Edit_Infor_User)
        self.ui.btn_profile.clicked.connect(self.move_to_page_profile)
        self.ui.horizontalSlider.valueChanged.connect(self.change_Volume)
        self.ui.btn_exit.clicked.connect(self.exit)
        self.username = None
        self.phone = None
        self.sender = sender



    def change_Volume(self):
        pass

    def receiveDataUser(self, data):
        self.username = data['user'].username
        self.phone = data['user'].phone
        # self.username = data['user'][0][2]
        # self.phone = data['user'][0][4]
        # self.test()

    def Edit_Infor_User(self):
        edit_fullname = self.ui.lineEdit.text()
        edit_nickname = self.ui.lineEdit_2.text()
        edit_gender = self.ui.lineEdit_3.text()
        edit_firstname = self.ui.lineEdit_10.text()
        edit_phone = self.ui.lineEdit_11.text()
        edit_email = self.ui.lineEdit_12.text()
        self.sender.sendInforToEdit(edit_fullname,edit_phone)



    def move_to_page_home(self):
        try:
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_learning)
            # self.ui.stackedWidget.setCurrentWidget(self.ui.page_home)
        except Exception as e:
            logging.error("An error occurred", exc_info=True)
            print(e)
    def move_to_page_learning(self):
        try:
            # self.ui.lineEdit.setText(str(self.username))
            # self.ui.lineEdit_11.setText(str(self.phone))
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_home)
        except Exception as e:
            print(f"An error occurred: {e}")

    def move_to_page_profile(self):
        try:
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_profile)
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

    def mouseReleaseEvent(self, event):
        self.initial_pos = None
        super().mouseReleaseEvent(event)
        event.accept()
    def exit(self):
        #os.system(cmd)
        QtCore.QCoreApplication.instance().quit()

    def window_state_changed(self, state):
        if state == Qt.WindowState.WindowMaximized:
            self.ui.btn_pile_stack.setVisible(True)
            self.ui.btn_maximize.setVisible(False)
        else:
            self.ui.btn_maximize.setVisible(True)
            self.ui.btn_pile_stack.setVisible(False)
