import sys
from PyQt5 import QtWidgets
import sys, os
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtCore, QtGui, QtWidgets

# current_directory = os.path.dirname(os.path.abspath(__file__)) + '\\'
# sys.path.append(current_directory)

from Client.View.Login import Login
class ControllerLogin(QMainWindow):
    def __init__(self, sender = None):
        super().__init__()

        self.uic = Login()
        self.sender = sender
        self.uic.setupUi(self)
        # setup event
        # change page register
        self.uic.btn_change_page.clicked.connect(self.show_register)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.uic.label_10.hide()
        self.uic.label_11.hide()
        self.uic.label_12.hide()

        # change page login
        self.uic.btn_login.clicked.connect(self.show_login)
        # close window
        self.uic.btn_exit.clicked.connect(self.closeEvent)
        #checklogin
        self.uic.btn_signIn.clicked.connect(self.Check_Login)
        self.uic.btn_register.clicked.connect(self.SendInforRegister)
        #change text to mode password
        self.uic.LEdit_password_signin.setEchoMode(QtWidgets.QLineEdit.Password)
        self.uic.LEdit_confirm.setEchoMode(QtWidgets.QLineEdit.Password)
        self.uic.LEdit_password_register.setEchoMode(QtWidgets.QLineEdit.Password)


    def show_register(self):
        self.uic.stackedWidget.setCurrentWidget(self.uic.page_2)
    def show_login(self):
        self.uic.stackedWidget.setCurrentWidget(self.uic.page_1)
    def setErrorRegister(self):
        self.uic.label_11.setText("username already exists")
        self.uic.label_11.show()
    def closeEvent(self,event):
        self.close()
    def setError(self):
        self.uic.label_10.setText("username or password error")
        self.uic.label_10.show()
    def Check_Login(self):
        username = self.uic.LEdit_email_signin.text()
        print(username)
        password = self.uic.LEdit_password_signin.text()
        print(password)
        self.sender.sendUsernameAndPassword(username, password)
        print("sendSucced")
    def SendInforRegister(self):
        username = self.uic.LEdit_email_register.text()
        password = self.uic.LEdit_password_register.text()
        confirm_password = self.uic.LEdit_confirm.text()
        phone = self.uic.LEdit_phone.text()
        if confirm_password != password:
            self.uic.label_12.setText("confirm_password error is not same password")
            self.uic.label_12.show()
        else:
            self.sender.sendInforRegister(username, password, phone)



if __name__ == '__main__':
    pass
    # app = QApplication(sys.argv)
    # main = ControllerLogin(soc)
    # main.show()
    # sys.exit(app.exec_())