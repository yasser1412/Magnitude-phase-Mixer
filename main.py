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
        self.images=[]
        self.img_views=[self.imageView,self.imageView_2,self.imageView_1_edit,self.imageView_2_edit]
# hide
        for i in range(len(self.img_views)):
            self.img_views[i].ui.histogram.hide()
            self.img_views[i].ui.roiBtn.hide()
            self.img_views[i].ui.menuBtn.hide()
            self.img_views[i].ui.roiPlot.hide()

        self.connect_func()

    def connect_func(self):
        self.actionImage1.triggered.connect(self.image_1)
        self.actionImage2.triggered.connect(self.image_2)

    def image_1(self):
        self.img_idx = 0
        self.browse()

    def image_2(self):
        self.img_idx = 1
        self.browse()
    
    def browse(self):
        self.file,_ = QtGui.QFileDialog.getOpenFileName(self, 'choose the image', os.getenv('HOME') ,"Images (*.png *.xpm *.jpg)" )
        # fileName = self.file.split('/')[-1]
        if self.file == "":
            pass
#check images size
        #set the second argument flages=0 to draw in grayscale
        self.image = cv.imread(self.file,0).T
        if self.img_idx == 0:
            self.current_size = self.image.shape[:2]
            self.img_views[self.img_idx].show()
            self.img_views[self.img_idx].setImage(self.image)
            
        elif self.img_idx == 1:
            if self.image.shape[:2] != self.current_size:
                self.msg.setWindowTitle("Error in Image Size")
                self.msg.setText("The images must have the same size")
                self.msg.setIcon(QMessageBox.Warning)
                x = self.msg.exec_()
                return
            else:
                self.img_views[self.img_idx].show()
                self.img_views[self.img_idx].setImage(self.image)
        self.img_components()

    def img_components(self):
        
        self.dft = np.fft.fft2(self.image)
        self.dft_shift = np.fft.fftshift(self.dft)
        self.magnitude = np.abs(self.dft_shift)
        self.magnitude_spectrum = 20*np.log(np.abs(self.dft_shift))
        self.phase = np.angle(self.dft_shift)
        self.real = np.real(self.dft_shift)
        self.real_spectrum = 20*np.log(np.real(self.dft_shift))
        self.imaginary = np.imag(self.dft_shift)
        # lsa ha check el combobox ba2a
        if self.comboBox.currentText() == "FT Magnitude":
            self.img_views[self.img_idx+2].show()
            self.img_views[self.img_idx+2].setImage(self.magnitude_spectrum)
        elif self.comboBox.currentText() == "FT Phase":
            self.img_views[self.img_idx+2].show()
            self.img_views[self.img_idx+2].setImage(self.phase)
        elif self.comboBox.currentText() == "FT Real Component":
            self.img_views[self.img_idx+2].show()
            self.img_views[self.img_idx+2].setImage(self.real_spectrum)
        elif self.comboBox.currentText() == "FT Imaginary Component":
            self.img_views[self.img_idx+2].show()
            self.img_views[self.img_idx+2].setImage(self.imaginary)

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
