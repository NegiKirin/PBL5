from PyQt5.QtCore import Qt, QEvent
from Client.Model import User
from Client.View.Home import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow


class ManagerUser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.ui.btn_edit.clicked.connect(self.update_user)
        self.ui.btn_home.clicked.connect(self.move_to_page_home)
        self.ui.btn_learning.clicked.connect(self.move_to_page_learning)
        self.ui.btn_profile.clicked.connect(self.move_to_page_profile)
        self.ui.horizontalSlider.valueChanged.connect(self.change_Volume)

    def change_Volume(self):
        pass

    def update_user(self):
        email = self.ui.lineEdit_12.text()
        fullname = self.ui.lineEdit.text()
        nickname = self.ui.lineEdit_2.text()
        phonenumber = self.ui.lineEdit_11.text()
        gender = self.ui.lineEdit_3.text()
        age = self.ui.lineEdit_10.text()
        user = User(email, fullname, nickname, phonenumber, gender, age)

    def move_to_page_home(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_learning)

    def move_to_page_learning(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_home)

    def move_to_page_profile(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_profile)

    def changeEvent(self, event):
        if event.type() == QEvent.Type.WindowStateChange:
            self.ui.window_state_changed(self.windowState())
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
