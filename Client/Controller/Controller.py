from Client.Controller.ControllerLogin import ControllerLogin


class Controller:
    def __init__(self, sender):
        self.sender = sender
        self.controllerLogin = ControllerLogin(self.sender)