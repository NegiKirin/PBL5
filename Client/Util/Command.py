from enum import Enum

<<<<<<< HEAD
class Command(Enum):
    USER = -1
    USERNAME_AND_PASSWORD = -2
=======
class Commands(Enum):
    LOG_FACE_DETECTOR = -1
    FRAME_AND_HT = -2
    HISTORY = -3
    LIST = -4
    DIAGRAM = -5
    SEND_IMAGES_FOR_DEVICE = -6
    SEND_ROOM_NUMBER = -7
    SEND_SESSIONID_AND_USERID = -8
>>>>>>> d40f260d798dedcaeb6eb52611c1e47372bac8fe
