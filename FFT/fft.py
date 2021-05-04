from PyQt5 import QtWidgets, QtCore, uic, QtGui, QtPrintSupport
import pyqtgraph as pg
from pyqtgraph import PlotWidget, plot
from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import *   
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from os import path
import sys
import os
import subprocess as sp
import time 
import ctypes

MAIN_WINDOW,_=loadUiType(path.join(path.dirname(__file__),"FFT.ui"))

class MainApp(QMainWindow,MAIN_WINDOW):
    # intiate lists
    Narray = [2 , 4 , 8 , 16 , 32 , 64 , 128 , 256 , 512 , 1024]
    ftTimeArray  = [0,0,0,0,0,0,0,0,0,0]
    fftTimeArray = [0,0,0,0,0,0,0,0,0,0]
    ErrorArray = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
    
    def __init__(self):
        super(MainApp,self).__init__()
        QMainWindow.__init__(self)
        self.setupUi(self)
        
        self.dftBtn.clicked.connect(lambda: self.call_cpp("ft"))
        self.fftBtn.clicked.connect(lambda: self.call_cpp("fft"))
        self.errorBtn.clicked.connect(lambda: self.call_cpp("error"))
        self.clrBtn.clicked.connect(lambda: self.plotHere.clear())
        
        self.plotHere.plotItem.addLegend(size=(1, 2))
        self.plotHere.plotItem.setLabel('bottom', "Number of samples")
        self.plotHere.plotItem.setLabel('left', "Computation time", units = "s")
        self.plotHere.plotItem.showGrid(True, True, alpha=0.5)
        self.plotHere_2.plotItem.addLegend(size=(1, 2))
        self.plotHere_2.plotItem.setLabel('left', "Error")
        self.plotHere_2.plotItem.setLabel('bottom', "Number of samples")
        
    def call_cpp(self, operation):
        
        #sp.call(["g++","FFT.cpp"])
        size = self.Narray.__len__()
        
        for i in range (size):
            # calculate the execution time of ft function with each N 
            if (operation == "ft"): 
                start_time = time.time()
                sp.call("./a "+ str(self.Narray[i])+" 1" )
                self.ftTimeArray[i] = (time.time() - start_time)
            
            # calculate the execution time of fft function with each N
            if (operation == "fft"):
                start_time = time.time()
                sp.call("./a "+ str(self.Narray[i])+" 2")
                self.fftTimeArray[i] = (time.time() - start_time)
        
        # Draw ft,fft execution time with its N
        if (operation == "ft"):
            self.plotHere.plot(self.Narray, self.ftTimeArray , name = "FT", pen="r" )
        if(operation == "fft"):
            self.plotHere.plot(self.Narray, self.fftTimeArray , name = "FFT", pen="b")
        
        #calculate and draw error between ft and fft outputs
        if (operation == "error"):
            library = ctypes.CDLL("./fourier.so")
            
            for i in range (size):
                self.ErrorArray[i] = library.calculate_errors(self.Narray[i])
            
            # draw the error with its N
            self.plotHere_2.plot(self.Narray , self.ErrorArray , name = "Error", pen="g")
        
if __name__=='__main__':
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())