from regex import L
import serial
import numpy as np
import matplotlib.pyplot as plt
from sympy import N

H = 7

class Mic:

    __ser = None

    coordinate = None
    direction = None

    id = None
    raw_img = None
    img = None

    max = None
    max_img_index = None
    max_center_index = None
    std = None

    def __init__(self, port_name, coordinate, direction):
        self.coordinate = coordinate
        self.direction = direction
        self.__ser = serial.Serial()
        self.__ser.port = port_name
        self.__ser.baudrate = 115200
        self.__ser.bytesize = 8
        self.__ser.stopbits = 1
        self.__ser.parity = "N"
        self.__ser.open()

    def read(self):
        while True:
            self.__ser.flushInput()
            while ord(self.__ser.read()) != 0xA5:
                pass
            id = ord(self.__ser.read())
            img = []
            s = 0
            for i in range(16 * 16):
                data = ord(self.__ser.read())
                img.append(data)
                s = s + data
            check = ord(self.__ser.read())
            end = ord(self.__ser.read())
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

class Solve:

    mics = []
    pos = None

    def __init__(self, mics):
        self.mics = mics

    def solve(self):
        A = []
        B = []
        for mic in self.mics:
            N = np.matrix([mic.max_center_index[0], mic.max_center_index[1], H])
            N = N * mic.direction
            N = np.array(N)
            l, m, n = N[0][0], N[0][1], N[0][2] 
            x0 = mic.coordinate[0]
            y0 = mic.coordinate[1]
            z0 = mic.coordinate[2]
            A.append([m, -l, 0])
            B.append(-(l * y0 - m * x0))
            A.append([0, n, -m])
            B.append(-(m * z0 - n * y0))
            A.append([n, 0, -l])
            B.append(-(l * z0 - n * x0))
        A = np.matrix(A)
        A = A.reshape((len(self.mics) * 3, 3))
        B = np.matrix(B)
        B = B.reshape((len(self.mics) * 3, 1))
        try:
            self.pos = (A.T * A).I * A.T * B
            return np.array(self.pos)
        except:
            return None

mic1 = Mic("COM6", [20, 20, 0], np.matrix([[ 0,  1,  0],
                                           [-1,  0,  0],
                                           [ 0,  0,  1]]))
mic2 = Mic("COM11", [0, 20, 20], np.matrix([[ 0,  1,  0],
                                            [ 0,  0,  1],
                                            [ 1,  0,  0]]))
mics = [mic1, mic2]
solve = Solve(mics)
# plt.ion()
while True:
    mic1.refresh()
    mic2.refresh()
    if mic1.max == 255 and mic2.max == 255:
        # mic1.max_center_index = (0, 0)
        # mic2.max_center_index = (0, 0)
        pos = solve.solve()
        if pos.all() != None:
            print("%3.0f, %3.0f, %3.0f" % (pos[0], pos[1], pos[2]))
        # print(mic1.max_center_index, mic2.max_center_index)
        # plt.imshow(mic.img, cmap = plt.cm.gray_r)
        # plt.pause(0.01)
