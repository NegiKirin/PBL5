from Client.Controller.ControllerLogin import ControllerLogin
from Client.Controller.ManagerUser import ManagerUser


# from Client.Controller.Test import ManagerUser
class Controller:
    def __init__(self, sender,movenet):
        self.movenet = movenet
        self.sender = sender
        self.controllerLogin = ControllerLogin(self.sender)
        self.managerUser = ManagerUser(self.sender,self.movenet)
