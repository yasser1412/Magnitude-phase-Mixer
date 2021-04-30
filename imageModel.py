import numpy as np
import cv2 as cv

class ImageModel():
    def __init__(self,path):
        self.path = path
        self.image = cv.imread(self.path,flags=cv.IMREAD_GRAYSCALE).T
        self.size = self.image.shape

        self.dft = np.fft.fft2(self.image)
        self.dft_shift = np.fft.fftshift(self.dft)

        self.magnitude = np.abs(self.dft)
        self.magnitude_shift = 20*np.log(np.abs(self.dft_shift))

        self.phase = np.angle(self.dft)
        self.phase_shift = np.angle(self.dft_shift)

        self.real = np.real(self.dft)
        self.real_shift = 20*np.log(np.real(self.dft_shift))

        self.imaginary = np.imag(self.dft)
        self.imaginary_shift = np.imag(self.dft_shift)

        self.uniform_magnitude = np.ones(self.image.shape)
        self.uniform_phase = np.zeros(self.image.shape)
### lsa h a3ml el modes
    def mix(self, image2:'Image', mag_real_ratio, ph_img_ratio):
        w1 = mag_real_ratio
        w2 = ph_img_ratio        
        mixInverse = None
        # m = 1 

        # if self.comboBox_6.currentText() == "Magnitude" and self.comboBox_7.currentText() == "Phase" or self.comboBox_7.currentText() == "Magnitude" and self.comboBox_6.currentText() == "Phase":
        # if m == 1:
        print("Mixing Magnitude and Phase")
        
        M1 = self.magnitude
        M2 = image2.magnitude

        P1 = self.phase
        P2 = image2.phase

        magnitudeMix = w1*M1 + (1-w1)*M2
        phaseMix = (1-w2)*P1 + w2*P2

        combined = np.multiply(magnitudeMix, np.exp(1j * phaseMix))
        mixInverse = np.real(np.fft.ifft2(combined))
        
        # elif self.comboBox_6.currentText() == "Real" and self.comboBox_7.currentText() == "Imaginary" or self.comboBox_7.currentText() == "Real" and self.comboBox_6.currentText() == "Imaginary":
        # elif m == 0:
        #     print("Mixing Real and Imaginary")
            
        #     R1 = self.real
        #     R2 = image2.real

        #     I1 = self.imaginary
        #     I2 = image2.imaginary

        #     realMix = w1*R1 + (1-w1)*R2
        #     imaginaryMix = (1-w2)*I1 + w2*I2

        #     combined = realMix + imaginaryMix * 1j
        #     mixInverse = np.real(np.fft.ifft2(combined))
        
        return abs(mixInverse)

