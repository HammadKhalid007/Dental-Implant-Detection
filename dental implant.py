import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QDialog, QMessageBox, QFileDialog, QPushButton, QLabel
# import pyrebase
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QLabel, QVBoxLayout
import imutils
import time
import numpy as np
import cv2,os,time
import pyshine as ps
from threading import Thread
from PIL import Image, ImageDraw, ImageFont
import winsound
import torch


class LoginScreen(QMainWindow):
    def __init__(self):
        super(LoginScreen, self).__init__()
        V = app.desktop().screenGeometry()
        h = V.height()
        w = V.width()
        widget.setGeometry(500, 250, w-1120, h-558)
        widget.setFixedWidth(w-1120)
        widget.setFixedHeight(h-558)
        widget.setWindowTitle("Dental Implant")
        loadUi("D:\External Disk\BCS\Projects\GUI\main.ui",self)
        self.pushButton.clicked.connect(self.loginfunction)


    def loginfunction(self):
        main = mainscreen()
        widget.addWidget(main)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class mainscreen(QMainWindow):
    def __init__(self):
        super(mainscreen, self).__init__()
        loadUi("D:\External Disk\BCS\Projects\GUI/2nd_screen.ui",self)
        V = app.desktop().screenGeometry()
        h = V.height()
        w = V.width()
        widget.setGeometry(0, 25, w, h-25)
        widget.setFixedWidth(w)
        widget.setFixedHeight(h-25)
        self.pushButton.clicked.connect(self.loginscreen)
        self.button = self.findChild(QPushButton, "pushButton_4")
        self.label = self.findChild(QLabel, "label_3")
        self.button.clicked.connect(self.clicker)
        self.pushButton_3.clicked.connect(self.image)


    def clicker(self):
        fname = QFileDialog.getOpenFileName(self, "Open File", "D:\External Disk\BCS\Projects\GUI/test/images", "All Files (*);; PNG Files (*.png);; Jpg Files (*.jpg")
        self.pixmap = QPixmap(fname[0])
        self.label.setPixmap(self.pixmap)
        # return pixmap



    def image(self):
        # Load the YOLOv7 model
        model = torch.hub.load('WongKinYiu/yolov7', 'custom', 'best.pt')
        # model.summary()
        #
        imag = self.pixmap
        if imag is not None:
            # Convert QPixmap to QImage
            image = imag.toImage()
            # Convert QImage to PIL Image
            img = Image.fromqimage(image)

        # Load the image
        # Get the predictions
        results = model(img)


        # Extract the bounding boxes, labels, and scores
        boxes = results.xyxy[0].tolist()
        labels = results.names[0]
        scores = results.xyxy[0][:, 4].tolist()

        # Total detections

        if len(boxes)!=0:
            total_detections = len(boxes)
            # Count the detections for each class
            class_counts = {}
            for label in labels:
                class_counts[label] = 0

            for label_index in results.pred[0][:, -1].tolist():
                class_counts[labels[int(label_index)]] += 1

            # Calculate the percentage of detections for each class
            class_percentages = {label: count / total_detections * 100 for label, count in class_counts.items()}

            # Print the report of total detections and the detection of each class in percentage
            print("Detection Report:")
            print(f"Total Detections: {total_detections}\n")

            implant_names = {
                'o': 'subperiosteal',
                'd': 'zygomatic',
                'n': 'transosteal',
                'E': 'endosteal'
            }

            for label, count in class_counts.items():
                percentage = class_percentages.get(label, 0)
                implant_type = implant_names.get(label, '')
                if implant_type:
                    print(f"{implant_type}: Count={count}, Percentage={percentage:.2f}%")

            # Plot the image and bounding boxes
            draw = ImageDraw.Draw(img)
            font = ImageFont.truetype("arial.ttf", 40)

            for box, score, label_index in zip(boxes, scores, results.pred[0][:, -1].tolist()):
                xmin, ymin, xmax, ymax = box[:4]
                label = f"{labels[int(label_index)]} {score:.2f}"
                draw.rectangle([(xmin, ymin), (xmax, ymax)], outline="red", width=6)
                draw.text((xmin, ymin - 40), label, font=font, fill="red")

                implant_type = implant_names.get(labels[int(label_index)], '')
                if implant_type:
                    draw.text((xmin, ymin - 80), implant_type, font=font, fill="red")

            my_list = [class_counts.get(label, 0) for label in ['o', 'd', 'n', 'E']]

            img.show()
        else:
            print("no implant found")
            img.show()



    def loginscreen(self):
        log = LoginScreen()
        widget.addWidget(log)
        V = app.desktop().screenGeometry()
        h = V.height()
        w = V.width()
        widget.setGeometry(500, 250, w-1120,h-558)
        # widget.setFixedWidth(w-1120)
        # widget.setFixedHeight(h-558)
        widget.setCurrentIndex(widget.currentIndex() + 1)





app = QtWidgets.QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()
widget2 = QtWidgets.QStackedWidget()
widget3 = QtWidgets.QStackedWidget()
b = QtWidgets.QStackedWidget()
login = LoginScreen()
widget.addWidget(login)
widget.show()
try:
    sys.exit(app.exec_())
except:
    print("Exiting")
