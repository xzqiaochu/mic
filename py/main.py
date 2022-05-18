import serial
import numpy as np
import matplotlib.pyplot as plt

class Mic:

    ser = None
    id = None
    raw_img = None
    img = None

    max = None
    max_img_index = None
    max_center_index = None
    std = None

    def __init__(self, port_name):
        self.ser = serial.Serial()
        self.ser.port = port_name
        self.ser.baudrate = 115200
        self.ser.bytesize = 8
        self.ser.stopbits = 1
        self.ser.parity = "N"
        self.ser.open()

    def read(self):
        while True:
            self.ser.flushInput()
            while ord(self.ser.read()) != 0xA5:
                pass
            id = ord(self.ser.read())
            img = []
            s = 0
            for i in range(16 * 16):
                data = ord(self.ser.read())
                img.append(data)
                s = s + data
            check = ord(self.ser.read())
            end = ord(self.ser.read())
            if end == 0x5A and s % 0x100 == check:
                self.id = id
                self.raw_img = img
                return

    def handle(self):
        img = np.array(self.raw_img)
        img = img.reshape(16, 16)
        # img = img.T
        img = img[::-1, ::-1]
        self.img = img

        self.max = img.max()
        self.max_img_index = np.unravel_index(img.argmax(), img.shape)
        self.max_center_index = (self.max_img_index[1] - 8, -self.max_img_index[0] + 8)
        self.std = img.std()
        
    def refresh(self):
        self.read()
        self.handle()

mic = Mic("COM8")
# plt.ion()
while True:
    mic.refresh()
    if mic.max == 255:
        print(mic.max_center_index)
        # plt.imshow(mic.img, cmap = plt.cm.gray_r)
        # plt.pause(0.01)
