from enum import Enum

class Command(Enum):
    USER = -1
    USERNAME_AND_PASSWORD = -2
    SEND_SERVER_REGISTER = -3
    SEND_CLIENT_REGISTER = -4
    SEND_SERVER_EDIT = -5