from PyQt5 import QtWidgets, QtCore, uic, QtGui, QtPrintSupport
from PyQt5.QtWidgets import QMessageBox  
import pyqtgraph as pg
from pyqtgraph import PlotWidget, plot
from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import *   
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from os import path
import numpy as np
import sys
import os
import math
from pyqtgraph import ImageView
from matplotlib import pyplot as plt
import cv2 as cv
import numpy as np
import sys
import os
import qdarkgraystyle
import logging
from imageModel import ImageModel

# logging.basicConfig(filemane="logFile.txt", Level=logging.DEBUG, format='%(asctime)s %(message)s')

MAIN_WINDOW,_=loadUiType(path.join(path.dirname(__file__),"main.ui"))

# class MainApp2(QtWidgets.QMainWindow,MAIN_WINDOW):
#     def __init__(self):
#         super(MainApp2,self).__init__()
#         QMainWindow.__init__(self)
#         self.setupUi(self)
#     self.actionNew_Window.triggered.connect(self.newWindow)
#     def newWindow(self):
#         new= MainApp()
#         new.show()

class MainApp(QtWidgets.QMainWindow,MAIN_WINDOW):
    def __init__(self):
        super(MainApp, self).__init__()
        # self.ui = Ui_MainWindow()
        self.setupUi(self)
        self.msg = QMessageBox() 

# list of everything
        self.images=[None,None]
        self.image_models=[None,None]
        self.img_views=[self.imageView,self.imageView_2,self.imageView_1_edit,self.imageView_2_edit,self.output_1,self.output_2]
        self.combos=[self.comboBox,self.comboBox_2,self.comboBox_3,self.comboBox_4,self.comboBox_5,self.comboBox_6,self.comboBox_7]
        # combo_components=['FT Magnitude','FT Phase','FT Real Component','FT Imaginary Component']
        self.slider1 = self.slider.value()
        self.slider2 = self.slider_2.value()
# hide
        for i in range(len(self.img_views)):
            self.img_views[i].ui.histogram.hide()
            self.img_views[i].ui.roiBtn.hide()
            self.img_views[i].ui.menuBtn.hide()
            self.img_views[i].ui.roiPlot.hide()

        self.connect_func()

    def connect_func(self):
        self.actionImage1.triggered.connect(lambda: self.browse(0))
        self.actionImage2.triggered.connect(lambda: self.browse(1))

        self.comboBox.currentTextChanged.connect(lambda: self.check_combo(0))
        self.comboBox_2.currentTextChanged.connect(lambda: self.check_combo(1))

        self.comboBox_4.currentTextChanged.connect(self.output_mix)
        self.comboBox_5.currentTextChanged.connect(self.output_mix)

        # self.comboBox_.currentTextChanged.connect(lambda: self.check_combo(1))
        self.slider.valueChanged.connect(self.output_mix)
        self.slider_2.valueChanged.connect(self.output_mix)
    

    # def image_1(self):
    #     self.img_idx = 0
    #     self.browse()

    # def image_2(self):
    #     self.img_idx = 1
    #     self.browse()

    # def combo_1(self):
    #     self.img_idx = 0
    #     self.check_combo()

    # def combo_2(self):
    #     self.img_idx = 1
    #     self.check_combo()

    def browse(self,idx):
        self.file,_ = QtGui.QFileDialog.getOpenFileName(self, 'choose the image', os.getenv('HOME') ,"Images (*.png *.xpm *.jpg)" )
        # fileName = self.file.split('/')[-1]
        if self.file == "":
            pass
        #error when upload img1 before img2
        #set the second argument in imread is flages = 0 to draw in grayscale
        if idx == 0:
            image = self.images[idx] = cv.imread(self.file,0).T
            self.current_size = image.shape[:2]
            self.image_models[idx]=ImageModel(self.file)
            self.draw_img(idx,image)

        elif idx == 1:
            image = self.images[idx] = cv.imread(self.file,0).T
            if image.shape[:2] != self.current_size:
                self.msg.setWindowTitle("Error in Image Size")
                self.msg.setText("The images must have the same size")
                self.msg.setIcon(QMessageBox.Warning)
                x = self.msg.exec_()
                return
            else:
                self.image_models[idx]=ImageModel(self.file)
                self.draw_img(idx,image)

    def draw_img(self,idx,image):
        # self.img_views[idx].show()
        self.img_views[idx].setImage(image)

        #repitition
    def check_combo(self,idx):
        selected_combo = self.combos[idx].currentText()
        if selected_combo == "FT Magnitude":
            self.draw_img(idx+2,self.image_models[idx].magnitude_shift)
        elif selected_combo == "FT Phase":
            self.draw_img(idx+2,self.image_models[idx].phase_shift)
        elif selected_combo == "FT Real Component":
            self.draw_img(idx+2,self.image_models[idx].real_shift)
        elif selected_combo == "FT Imaginary Component":
            self.draw_img(idx+2,self.image_models[idx].imaginary_shift)

    def output_mix(self):
        imgIndex1 = self.comboBox_4.currentIndex()
        imgIndex2 = self.comboBox_5.currentIndex()
        componentOne = self.comboBox_6.currentText().lower()
        componentTwo = self.comboBox_7.currentText().lower()
        self.sliderOneValue = self.slider.value()/100.0
        self.sliderTwoValue = self.slider_2.value()/100.0
        mixOutput = ...
        output_idx = self.comboBox_3.currentIndex()
### el magnitude + phase mix bas el sha8al
        if componentOne == "magnitude":
            if componentTwo == "phase":
                mixOutput = self.image_models[imgIndex1].mix(self.image_models[imgIndex2], self.sliderOneValue,self.sliderTwoValue)
            if componentTwo == "uniform phase":
                mixOutput = self.image_models[imgIndex1].mix(self.image_models[imgIndex2], self.sliderOneValue,self.sliderTwoValue)

        elif componentOne == "phase":
            if componentTwo == "magnitude":
                mixOutput = self.image_models[imgIndex2].mix(self.image_models[imgIndex1], self.sliderTwoValue,self.sliderOneValue)
            elif componentTwo == "uniform magnitude":
                mixOutput = self.image_models[imgIndex2].mix(self.image_models[imgIndex1], self.sliderOneValue,self.sliderTwoValue)

        elif componentOne == "real":
            if componentTwo == "imaginary":
                mixOutput = self.image_models[imgIndex1].mix(self.image_models[imgIndex2], self.sliderOneValue,self.sliderTwoValue)

        elif componentOne == "imaginary":
            if componentTwo == "real":
                mixOutput = self.image_models[imgIndex2].mix(self.image_models[imgIndex1], self.sliderTwoValue,self.sliderOneValue)

        elif componentOne == "uniform phase":
            if componentTwo == "magnitude":
                mixOutput = self.image_models[imgIndex2].mix(self.image_models[imgIndex1], self.sliderTwoValue,self.sliderOneValue)
            elif componentOne == "uniform magnitude":
                mixOutput = self.image_models[imgIndex2].mix(self.image_models[imgIndex1], self.sliderTwoValue,self.sliderOneValue)

        elif componentOne == "uniform magnitude":
            if componentTwo == "phase":
                mixOutput = self.image_models[imgIndex1].mix(self.image_models[imgIndex2], self.sliderOneValue,self.sliderTwoValue)
            elif componentTwo == "uniform phase":
                mixOutput = self.image_models[imgIndex1].mix(self.image_models[imgIndex2], self.sliderOneValue,self.sliderTwoValue)

        self.draw_img(output_idx+4,mixOutput)

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
