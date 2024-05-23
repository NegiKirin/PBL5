import pickle
import threading
import socket
import Client.Model.User
from Client.Util.Command import Command

BUFF_SIZE = 65536
HEADERSIZE = 10
COMMANDSIZE = 3
class Receiver:
    def __init__(self, conn, sender, controller):
        self.socket = conn
        self.sender = sender
        self.controller = controller

        t = threading.Thread(target=self.run, args=())
        # t.setDaemon = True
        t.start()

    def getCommand(self, data):
        command = int(data[:COMMANDSIZE])
        return command
    def getSize(self, data):
        size = int(data[COMMANDSIZE:HEADERSIZE])
        return size

    def receiveUser(self, data):
        # Todo: Receive User
        try:
            size = self.getSize(data)
            print(size)
            print(data)
            main_data = None
            full_msg = b''
            new_msg = True
            while True:
                msg = self.socket.recv(1024)
                if new_msg:
                    msg = data + msg
                    new_msg = False
                full_msg += msg
                print(full_msg)
                if len(full_msg) - HEADERSIZE - COMMANDSIZE == size:
                    main_data = pickle.loads(full_msg[HEADERSIZE + COMMANDSIZE:])
                    print(main_data)
                    break

            if main_data is {}:
                # Todo: print error
                self.controller.controllerLogin.setError()
                print()
            else:
                # Todo: change page
                print()

        except Exception as e:
            print(e)

    def run(self):
        while True:
            print("Waiting command")
            try:
                print('wait command')
                data = self.socket.recv(13)
                cm = self.getCommand(data)
                print('new command', cm)
                if cm == Command.USER.value:
                    self.receiveUser(data)

            except socket.error as error:
                print(error)
                print("Receiver error")
            except Exception as e:
                print(e)