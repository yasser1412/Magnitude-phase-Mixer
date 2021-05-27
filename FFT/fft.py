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
from scipy.interpolate import make_interp_spline

MAIN_WINDOW,_=loadUiType(path.join(path.dirname(__file__),"FFT.ui"))

class MainApp(QMainWindow,MAIN_WINDOW):
    # intiate lists
    Narray = [2 , 4 , 8 , 16 , 32 , 64 , 128 , 256 , 512 , 1024,2048,4096,8192,16384]
    ftTimeArray  = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    fftTimeArray = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    ErrorArray = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0,0,0,0]
    
    def __init__(self):
        super(MainApp,self).__init__()
        QMainWindow.__init__(self)
        self.setupUi(self)
        
        self.dftBtn.clicked.connect(lambda: self.call_cpp("ft"))
        self.fftBtn.clicked.connect(lambda: self.call_cpp("fft"))
        self.errorBtn.clicked.connect(lambda: self.call_cpp("error"))
        self.clrBtn.clicked.connect(lambda: self.plotHere.clear())
        self.clrBtn.clicked.connect(lambda: self.plotHere_2.clear())
        
        self.plotHere.plotItem.addLegend(size=(1, 2))
        self.plotHere.plotItem.setTitle("Computation Time")
        self.plotHere.plotItem.setLabel('bottom', "Number of samples")
        self.plotHere.plotItem.setLabel('left', "Time", units = "s")
        self.plotHere.plotItem.showGrid(True, True, alpha=0.3)
        self.plotHere.plotItem.setMouseEnabled(x=False,y=True)
        self.plotHere_2.plotItem.addLegend(size=(1, 2))
        self.plotHere_2.plotItem.setTitle("MSE")
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
                self.fftTimeArray[i] = ((time.time() - start_time))
                
        xnew = np.linspace(min(self.Narray), max(self.Narray), 100)
        # Draw ft,fft execution time with its N
        if (operation == "ft"):
            spl = make_interp_spline(self.Narray, self.ftTimeArray, 3)
            ynew = spl(xnew)
            self.plotHere.plot(xnew, ynew , name = "FT . (N^2)", pen="r" )
        if(operation == "fft"):
            spl = make_interp_spline(self.Narray, self.fftTimeArray, 3)
            ynew = spl(xnew)
            self.plotHere.plot(xnew, ynew*50 , name = "FFT . (NlogN) (Scaled)", pen="b")
        self.plotHere.plotItem.getViewBox().enableAutoRange(axis='y')
        
        #calculate and draw error between ft and fft outputs
        if (operation == "error"):
            library = ctypes.CDLL("./fourier.so")
            library.calculate_errors.restype = ctypes.c_double 
            library.calculate_errors.argtypes  = [ctypes.c_int] 
            
            for i in range (size):
                self.ErrorArray[i] =  library.calculate_errors(self.Narray[i])
            # draw the error with its N
            spl = make_interp_spline(self.Narray, self.ErrorArray, 3)
            ynew = spl(xnew)
            self.plotHere_2.plot(xnew , ynew , name = "Error", pen="g")
        
if __name__=='__main__':
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())