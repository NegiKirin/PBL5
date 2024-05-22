import socket

host = ''  # ip of server
port = 1234
from Client.Model import User

class Sender:
    def __init__(self):
        sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sender_socket.bind((host, port))
        sender_socket.listen(1100)
    def send(self,user:User):
        pass
