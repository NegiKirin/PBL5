from Client.Controller.ControllerLogin import ControllerLogin
from Client.Controller.ManagerUser import ManagerUser

class Controller:
    def __init__(self, sender):
        self.sender = sender
        self.controllerLogin = ControllerLogin(self.sender)
        self.managerUser = ManagerUser(self.sender)