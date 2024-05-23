import socket
import threading
import sys

from Server.Util.HandleClient import HandlerClient


class Server:
    # def __init__(self):
    #     self.soc = None
    #     self.host = "192.168.220.1"
    #     self.port = 9999
    #     t = threading.Thread(target=self.create_socket(), args=())
    #     # t.setDaemon = True
    #     t.start()
    #
    # def create_socket(self):
    #     self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     self.soc.bind((self.host,self.port))
    #     self.soc.listen(2)
    #
    #     while True:
    #         print("Waiting for connection")
    #         client, addr = self.soc.accept()
    #         print("Client connected!")
    #         try:
    #             print('Connected by', addr)
    #             while True:
    #                 data = client.recv(1024)
    #                 str_data = data.decode("utf8")
    #
    #                 print(str_data)
    #                 if str_data == "quit":
    #                     break
    #                 """if not data:
    #                     break
    #                 """
    #                 print("Client: " + str_data)
    #
    #                 msg = input("Server: ")
    #                 client.sendall(bytes(msg, "utf8"))
    #         finally:
    #             client.close()

    def __init__(self):
        self.soc = None
        self.soc_UDP = None
        self.face_names = []
        self.host = "127.0.0.1"
        self.port = 9999

        self.create_socket()
        self.create_socket_UDP()
        self.binding_socket()
        self.listening_socket(1)


        t = threading.Thread(target=self.accept_socket, args=())
        # t.setDaemon = True
        t.start()

        self.handlerClient = HandlerClient()
        # self.drawGUI()

    def create_socket(self):
        try:
            self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # self.soc.settimeout(1)
            print('Has been created a socket server')
        except socket.error as msg:
            print(str(msg) + ' .Trying to connecting again...')
            self.create_socket()

    def create_socket_UDP(self):
        try:
            self.soc_UDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.soc_UDP.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 65536)
        except socket.error as msg:
            print(str(msg))
            # self.create_socket_UDP()

    def binding_socket(self):
        try:
            self.soc.bind((self.host, self.port))
            self.soc_UDP.bind((self.host, self.port))
            print('Binding id = ' + str(self.host) + ' port = ' + str(self.port))
        except socket.error as msg:
            print(str(msg) + ' .Trying to binding socket again...')
            # self.binding_socket()

    def accept_socket(self):
        while True:
            try:
                conn, address = self.soc.accept()
                print('Establish connection with IP = ' + str(address[0]) + " | PORT = " + str(address[1]))
                # 0: device checkin / 1: client
                # index = conn.recv(1024).decode('utf8')

                # if index == '1':
                #     # create client
                #
                #     print("client connected")
                # elif index == '0':
                #     # create device
                #     self.handlerDevice.appendDevice(conn)
                #     print("device connected")

                self.handlerClient.appendClient(conn)
                print("client connected")

            except socket.error as msg:
                print(str(msg) + '\n' + 'Trying to accept...')

    def listening_socket(self, time):
        try:
            self.soc.listen(time)
        except socket.error as msg:
            print(str(msg) + '\n' + 'Trying to listening ' + str(time) + ' s...')
            # self.listening_socket(time)

    def close_socket(self):
        try:
            self.soc.close()
        except socket.error as msg:
            print(str(msg) + ' Trying to close socket...')
            # self.close_socket()

    def drawGUI(self):
        app = QApplication(sys.argv)
        main_win = MainWindow()
        main_win.show()
        # main_win.start_capture_video()
        sys.exit(app.exec_())

if __name__ == '__main__':
    s = Server()