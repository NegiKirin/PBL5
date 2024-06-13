import sys
import logging
import os
import sys
import threading

import tensorflow as tf
import tensorflow_hub as hub
import os
import cv2
import numpy as np
from PyQt5.QtMultimedia import QMediaPlayer
from tqdm.notebook import tqdm
import cv2
import imutils
import numpy as np
from PyQt5 import QtGui, QtCore, QtWidgets

from PyQt5.QtCore import Qt, QEvent, QSize, QRect, QTimer
from PyQt5.QtGui import QPixmap, QImage, QBrush, QPainter, QWindow, QIcon
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QListWidgetItem

# current_directory = os.path.dirname(os.path.abspath(__file__)) + '\\'
# sys.path.append(current_directory)

from Raspberry.View.predict import Predict

EDGES = {
    (0, 1): 'm',
    (0, 2): 'c',
    (1, 3): 'm',
    (2, 4): 'c',
    (0, 5): 'm',
    (0, 6): 'c',
    (5, 7): 'm',
    (7, 9): 'm',
    (6, 8): 'c',
    (8, 10): 'c',
    (5, 6): 'y',
    (5, 11): 'm',
    (6, 12): 'c',
    (11, 12): 'y'
}
class Controller(QMainWindow):
    def __init__(self, sender = None,movenet = None):
        super().__init__()
        self.word = None
        self.listKeyPoints = []
        self.movenet = movenet
        self.timer = None
        self.uic = Predict()
        self.sender = sender
        self.uic.setupUi(self)
        self.cap = None
        # setup event
        # change page register
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        #substract
        self.uic.btn_substract.clicked.connect(self.window().showMinimized)
        #pile
        self.uic.btn_pile_stack.clicked.connect(self.window().showNormal)
        #exit
        self.uic.btn_exit.clicked.connect(self.exit)
        #open camera
        self.viewCameraToPredict()
    def exit(self):
        # os.system(cmd)
        QtCore.QCoreApplication.instance().quit()

    #open camera to predict realtime
    def viewCameraToPredict(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            return

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(20)
        print("open succeed")

    #update frame to QLabel
    def update_frame(self):
        if self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                print("testing")
                keypoints = self.extractKeypoints(frame, self.movenet)
                print("keypoints")
                keypoints = keypoints[:13, :2]
                print(keypoints.shape)
                print("check")
                keypoints = self.normKeypoint(keypoints, dis_mean=0.10192956195594993,
                                              center=(0.4803588539361954, 0.4331198185682297))
                print("checked")
                self.draw_keypoints(frame, keypoints)
                self.draw_connections(frame, keypoints, EDGES)

                self.listKeyPoints.append(keypoints)
                # print(keypoints.shape ,len(self.listKeyPoints))
                if len(self.listKeyPoints) == 58:
                    self.sender.sendKeyPoint(self.listKeyPoints)
                    self.listKeyPoints = []
                height, width, channel = frame.shape
                step = channel * width
                qImg = QImage(frame.data, width, height, step, QImage.Format_RGB888)
                self.uic.label_creen.setPixmap(QPixmap.fromImage(qImg))

    def extractKeypoints(self, img, movenet):
        # Load the input image.
        # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        X = tf.expand_dims(img, axis=0)
        X = tf.cast(tf.image.resize_with_pad(X, 256, 256), dtype=tf.int32)
        # X = tf.cast(tf.image.resize_with_pad(X, 192, 192), dtype=tf.int32)
        outputs = movenet(X)
        keypoints = outputs['output_0'].numpy()
        # print(keypoints.shape)
        # max_key,key_val = keypoints[0,:,55].argmax(),keypoints[0,:,55].max()
        # max_points = keypoints[0,max_key,:]
        # max_points = max_points.astype(float)

        # keypoint = []
        #
        # for i in range(0,len(max_points)-5,3):
        #     keypoint.append([max_points[i],max_points[i+1],max_points[i+2]])

        return np.array(keypoints[0][0])

    def draw_keypoints(self, frame, keypoints):
        for kp in keypoints:
            ky, kx = kp
            # print(ky, kx)
            x, y = int(kx * frame.shape[1]), int(ky * frame.shape[0])
            # print('paint: x={}, y={}'.format(x, y))
            cv2.circle(frame, (x, y), 4, (0, 255, 0), -1)

    def draw_connections(self, frame, keypoints, edges):
        for edge, color in edges.items():
            p1, p2 = edge
            y1, x1 = keypoints[p1]
            y2, x2 = keypoints[p2]
            y1 *= frame.shape[0]
            x1 *= frame.shape[1]
            y2 *= frame.shape[0]
            x2 *= frame.shape[1]

            cv2.line(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 2)

    def move_to_center(self, keypoints, center):
        center_temp = self.find_center(keypoints)
        # move = center - find_center(keypoints)
        move = [center[0] - center_temp[0], center[1] - center_temp[1]]
        for keypoint in keypoints:
            keypoint[0] += move[0]
            keypoint[1] += move[1]
        return keypoints

    def find_center(self, keypoints):
        return [(keypoints[5][0] + keypoints[6][0]) / 2, (keypoints[5][1] + keypoints[6][1]) / 2]

    def find_x(self, A, B, mean):
        c = np.sqrt((A[0] - B[0]) ** 2 + (A[1] - B[1]) ** 2)
        # print(f'c={c}')
        x = (c - mean) / (c + 1e-1)
        return x

    def scale_keypoint(self, keypoints, mean):
        x = self.find_x(keypoints[0], keypoints[1], mean)
        print(x)
        for i in range(1, len(keypoints)):
            if i == 0:
                continue
            # print(i)
            # kx = x * (keypoints[0][0]- keypoints[i][0])
            # ky = x * (keypoints[0][1]- keypoints[i][1])

            kx = x * (keypoints[i][0] - keypoints[0][0])
            ky = x * (keypoints[i][1] - keypoints[0][1])

            # print(f'kx={kx}, ky={ky}')
            keypoints[i] = [keypoints[i][0] - kx, keypoints[i][1] - ky]
        return keypoints

    def normKeypoint(self, keypoints, dis_mean, center):
        keypoints = self.scale_keypoint(keypoints, dis_mean)
        keypoints = self.move_to_center(keypoints, center)
        return keypoints

    def update_frame(self):
        if self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                keypoints = self.extractKeypoints(frame, self.movenet)
                print(keypoints.shape)
                keypoints = keypoints[:13, :2]
                print(keypoints.shape)

                keypoints = self.normKeypoint(keypoints, dis_mean=0.10192956195594993,
                                              center=(0.4803588539361954, 0.4331198185682297))

                self.draw_keypoints(frame, keypoints)
                self.draw_connections(frame, keypoints, EDGES)

                self.listKeyPoints.append(keypoints)
                print(keypoints.shape ,len(self.listKeyPoints))
                if len(self.listKeyPoints) == 58:
                    self.sender.sendKeyPoint(self.listKeyPoints)
                    self.listKeyPoints = []
                height, width, channel = frame.shape
                step = channel * width
                qImg = QImage(frame.data, width, height, step, QImage.Format_RGB888)
                self.uic.label_creen.setPixmap(QPixmap.fromImage(qImg))

    def display_Word_Predict(self,word):
        self.word = word
        self.uic.text_predict.setText(self.word)


if __name__ == '__main__':
    pass
    # app = QApplication(sys.argv)
    # main = ControllerLogin(soc)
    # main.show()
    # sys.exit(app.exec_())