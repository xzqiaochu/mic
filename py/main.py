import serial
import numpy as np
import matplotlib.pyplot as plt
from time import time

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
        self.max_center_index = (
            self.max_img_index[1] - 8, -self.max_img_index[0] + 8)
        self.std = img.std()

    def refresh(self):
        self.read()
        self.handle()


class Solve:

    mics = []
    pos = None
    valid = False
    update = False

    def __init__(self, mics):
        self.mics = mics

    def solve(self):
        A = []
        B = []
        for mic in self.mics:
            N = np.matrix([mic.max_center_index[0],
                          mic.max_center_index[1], H])
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
            pos = np.array((A.T * A).I * A.T * B)
            self.pos = pos
            if all(_ >= 0 and _ <= 40 for _ in pos):
                self.valid = True
            else:
                self.valid = False
            self.update = True
        except:
            self.update = False

def axClear(ax):
    ax.cla()
    ax.set_xlim(0, 40)
    ax.set_ylim(0, 40)
    ax.set_zlim(0, 40) # 设置每个坐标轴的取值范围
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')


mic1 = Mic("COM6", [20, 20, 0], np.matrix([[0,  1,  0],
                                           [-1,  0,  0],
                                           [0,  0,  1]]))
mic2 = Mic("COM11", [0, 20, 20], np.matrix([[0,  1,  0],
                                            [0,  0,  1],
                                            [1,  0,  0]]))
mics = [mic1, mic2]
solve = Solve(mics)
plt.ion()
fig = plt.figure()
ax = fig.add_subplot(projection='3d')
last = time()
while True:
    for mic in mics:
        mic.refresh()
    if all(mic.max == 255 for mic in mics):
        solve.solve()
        if solve.update:
            pos = solve.pos
            now = time()
            print("%3.0f, %3.0f, %3.0f, %.1ffps" % (pos[0], pos[1], pos[2], 1 / (now - last)))
            last = now
            # plt.imshow(mic.img, cmap = plt.cm.gray_r)
            axClear(ax)
            if solve.valid:
                ax.scatter(pos[0], pos[1], pos[2], c="b", marker="o")
            else:
                ax.scatter(pos[0], pos[1], pos[2], c="r", marker="o")
            plt.pause(0.001)
