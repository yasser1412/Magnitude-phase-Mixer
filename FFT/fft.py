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
import numpy as np


MAIN_WINDOW,_=loadUiType(path.join(path.dirname(__file__),"FFT.ui"))

class MainApp(QMainWindow,MAIN_WINDOW):
    
    dftTimeArray  = [0,0,0,0,0,0,0,0,0,0]
    fftTimeArray = [0,0,0,0,0,0,0,0,0,0]
    Narray = [2 , 4 , 8 , 16 , 32 , 64 , 128 , 256 , 512 , 1024]
    realErrorArray = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
    imagErrorArray = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
    def __init__(self):
        super(MainApp,self).__init__()
        QMainWindow.__init__(self)
        self.setupUi(self)
        
        self.dftBtn.clicked.connect(lambda: self.call_cpp(1))
        self.fftBtn.clicked.connect(lambda: self.call_cpp(2))
        self.clrBtn.clicked.connect(lambda: self.plotHere.clear())
        self.errorBtn.clicked.connect(lambda: self.dft_fft_error())
        
    def call_cpp(self, index):
        
        sp.call(["g++","FFT.cpp"])
        size = self.Narray.__len__()
        
        for i in range (size):
            
            if (index == 1): 
                start_time = time.time()
                sp.call("./a "+ str(self.Narray[i])+" 1" )
                self.dftTimeArray[i] = (time.time() - start_time)
            
            if (index == 2):
                start_time = time.time()
                sp.call("./a "+ str(self.Narray[i])+" 2")
                self.fftTimeArray[i] = (time.time() - start_time)
            
        self.plotHere.plotItem.addLegend(size=(1, 2))
        
        if (index == 1):
            self.plotHere.plot(self.Narray, self.dftTimeArray , name = "DFT", pen="r" )
            
        if(index == 2):
            self.plotHere.plot(self.Narray, self.fftTimeArray , name = "FFT", pen="b")
        
        self.plotHere.plotItem.showGrid(True, True, alpha=0.5)
        self.plotHere.plotItem.setLabel('bottom', "Number of samples")
        self.plotHere.plotItem.setLabel('left', "Computation time", units = "s")
        
        
    def dft_fft_error(self):
        library = ctypes.CDLL("./test.so")
        size = self.Narray.__len__()
        
        for i in range (size):
            self.realErrorArray[i] , self.imagErrorArray[i] = library.calculate_errors(self.Narray[i])
        
        self.plotHere_2.plotItem.addLegend(size=(1, 2))
        self.plotHere_2.plot(self.Narray , self.realErrorArray , name = "real errors")
        self.plotHere_2.plot(self.Narray , self.imagErrorArray , name = "imag errors")
        
if __name__=='__main__':
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())