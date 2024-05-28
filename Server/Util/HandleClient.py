import os
import sys
import threading
import time

# from Server.Controller.DeviceReciver import DeviceReceiver


current_directory = os.path.dirname(os.path.abspath(__file__)) + '\\'
sys.path.append(current_directory)
from Server.Network.Receiver import Receiver
from Server.Network.Sender import Sender
# from Server.Controller.DeviceReciver import DeviceReceiver


class HandlerClient:
    def __init__(self):
        self.devices = []
        #run
        # t = threading.Thread(target=self.checkActive, args=())
        # t.start()

    def appendClient(self, conn):
        # Todo: add client receiver
        sender_client = Sender(conn)
        receiver_client = Receiver(conn, sender_client)
        self.devices.append(receiver_client)

    def removeDevice(self, device):
        self.devices.remove(device)

    def checkActive(self):
        while True:
            for device in self.devices:
                if device.active == False:
                    self.removeDevice(device)
                    print("remove device")
            time.sleep(1)