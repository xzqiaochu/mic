import serial
import serial.tools.list_ports
import numpy as np
import matplotlib.pyplot as plt
from multiprocessing import Process, Queue
from time import time
import copy

H = 8.5
MIN_VAL = 255
Q2SOLVE_MAX_CACHE = 9
Q2SHOW_MAX_CACHE = 1

class MicConfig:
    pos = []
    dir = []

    def __init__(self, pos, dir):
        self.pos = pos
        self.dir = dir

g_micconfigs = {}
g_micconfigs[1] = MicConfig([20, 20, 0], [[ 0,  1,  0],
                                          [-1,  0,  0],
                                          [ 0,  0,  1]])
g_micconfigs[2] = MicConfig([0, 20, 20], [[ 0,  1,  0],
                                          [ 0,  0,  1],
                                          [ 1,  0,  0]])
g_micconfigs[3] = MicConfig([20, 0, 20], [[-1,  0,  0],
                                          [ 0,  0,  1],
                                          [ 0,  1,  0]])

class MicData():
    id = 0
    img = np.array(0)
    max = 0
    std = 0
    max_p = (0, 0)
    handle_t = 0

class Mic(Process):

    ser = serial.Serial()
    q2solve = Queue()

    raw_img = []
    data = MicData()

    def __init__(self, port_name, q2solve):
        Process.__init__(self)
        self.ser = serial.Serial()
        self.ser.port = port_name
        self.ser.baudrate = 115200
        self.ser.bytesize = 8
        self.ser.stopbits = 1
        self.ser.parity = "N"
        self.q2solve = q2solve

    def read(self):
        while True:
            # self.ser.flushInput()
            while ord(self.ser.read()) != 0xA5:
                pass
            id = ord(self.ser.read())
            img = []
            s = 0
            for _ in range(16 * 16):
                data = ord(self.ser.read())
                img.append(data)
                s = s + data
            check = ord(self.ser.read())
            end = ord(self.ser.read())
            if end == 0x5A and s % 0x100 == check:
                self.data.id = id
                self.raw_img = img
                return

    def handle(self):
        img = np.array(self.raw_img)
        img = img.reshape(16, 16)
        img = img[::-1, ::-1]
        
        max = img.max()
        std = img.std()
        max_img_p = np.unravel_index(img.argmax(), img.shape)
        max_p = (max_img_p[1] - 8, -max_img_p[0] + 8)

        self.data.img = img
        self.data.max = max
        self.data.std = std
        self.data.max_p = max_p

    def refresh(self):
        st = time()
        self.read()
        self.handle()
        while self.data.max < MIN_VAL:
            self.read()
            self.handle()
        self.data.handle_t = time() - st

    def run(self):
        self.ser.open()
        while True:
            self.refresh()
            if self.q2solve.qsize() > Q2SOLVE_MAX_CACHE:
                self.q2solve.get()
            data = copy.deepcopy(self.data)
            self.q2solve.put(data)

class SolveData():
    micdatas = [MicData()]
    pos = np.array(0)
    loss = 0
    handle_t = 0

class Solve(Process):
    mic_num = 0
    q2solve = Queue()
    q2show = Queue()

    data = SolveData()

    def __init__(self, mic_num, q2solve, q2show):
        Process.__init__(self)
        self.mic_num = mic_num
        self.q2solve = q2solve
        self.q2show = q2show

    def solve(self):
        A = []
        B = []
        for micdata in self.data.micdatas:
            micconfig = g_micconfigs[micdata.id]
            pos = micconfig.pos
            dir = micconfig.dir
            N = np.matrix([micdata.max_p[0], micdata.max_p[1], H])
            N = np.array(N * dir)
            l, m, n = N[0][0], N[0][1], N[0][2]
            x0, y0, z0 = pos[0], pos[1], pos[2]
            A.append([m, -l, 0])
            B.append(-(l * y0 - m * x0))
            A.append([0, n, -m])
            B.append(-(m * z0 - n * y0))
            A.append([n, 0, -l])
            B.append(-(l * z0 - n * x0))
        A = np.matrix(A)
        A = A.reshape((self.mic_num * 3, 3))
        B = np.matrix(B)
        B = B.reshape((self.mic_num * 3, 1))
        try:
            X = (A.T * A).I * A.T * B
            E = A * X - B 
            self.data.pos = np.array(X)
            loss2 = sum([e ** 2 for e in np.array(E)])[0] / (self.mic_num * 3)
            self.data.loss = loss2 ** 0.5
            return True
        except:
            return False

    def waitReady(self):
        st = time()
        self.data.micdatas = []
        tmplist = []
        while len(self.data.micdatas) < self.mic_num:
            micdata = self.q2solve.get()
            if micdata.id not in tmplist:
                self.data.micdatas.append(micdata)
                tmplist.append(micdata.id)
        self.data.micdatas.sort(key = lambda r:r.id)
        self.data.wait_t = time() - st

    def refresh(self):
        st = time()
        self.waitReady()
        while self.solve() == False:
            self.waitReady()
        self.data.handle_t = time() - st

    def run(self):
        while True:
            self.refresh()
            if self.q2show.qsize() > Q2SHOW_MAX_CACHE:
                self.q2show.get()
            data = copy.deepcopy(self.data)
            self.q2show.put(data)

class Show(Process):

    q2show = Queue()

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    solvedata = SolveData()

    last_t = 0
    wait_t = 0

    def __init__(self, q2show):
        Process.__init__(self)
        self.q2show = q2show
        plt.ion()

    def clear(self):
        self.ax.cla()
        self.ax.set_xlim(0, 40)
        self.ax.set_ylim(0, 40)
        self.ax.set_zlim(0, 40)  # 设置每个坐标轴的取值范围
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
        self.ax.scatter(0, 0, 0, c="black", marker="o")
        self.ax.plot([0, 0], [0, 0], [0, 40], c = "black")
        self.ax.plot([0, 0], [0, 40], [0, 0], c = "black")
        self.ax.plot([0, 40], [0, 0], [0, 0], c = "black")

    def showText(self):
        now = time()
        pos = self.solvedata.pos
        print("[%.1ffps]" % (1 / (now - self.last_t)), end = "\t")
        print("%2.0f, %2.0f, %2.0f" % (pos[0], pos[1], pos[2]), end = "\t")
        print([micdata.max_p for micdata in self.solvedata.micdatas], end = "\t")
        print(round(self.solvedata.loss, 1), end = "\t")
        print([round(micdata.handle_t * 1000) for micdata in self.solvedata.micdatas], end = "\t")
        print(round(self.solvedata.handle_t * 1000), end = "\t")
        print(round((now - self.last_t) * 1000))
        self.last_t = now

    def showImg(self):
        self.clear()
        pos = self.solvedata.pos
        self.ax.scatter(pos[0], pos[1], pos[2], c="r", marker="o")

        for micdata in self.solvedata.micdatas:
            micconfig = g_micconfigs[micdata.id]
            pos = micconfig.pos
            dir = micconfig.dir
            N = np.matrix([micdata.max_p[0], micdata.max_p[1], H])
            N = np.array(N * dir)
            l, m, n = N[0][0], N[0][1], N[0][2]
            x0, y0, z0 = pos[0], pos[1], pos[2]
            t = 40 / H
            x1 = t * l + x0
            y1 = t * m + y0
            z1 = t * n + z0
            self.ax.plot([x0, x1], [y0, y1], [z0, z1], c = "b")

    def waitReady(self):
        st = time()
        while self.q2show.empty():
            plt.pause(0.01)
        self.wait_t = time() - st

    def refresh(self):
        self.solvedata = self.q2show.get()
        self.showText()
        self.showImg()

    def run(self):
        self.ax.view_init(elev = 45, azim = 45)
        while True:
            self.waitReady()
            self.refresh()

def main():
    ports = serial.tools.list_ports.comports()
    ports_num = len(ports)
    if ports_num == 0:
        print ("No serial port found!")
        return

    q2solve = Queue(Q2SOLVE_MAX_CACHE)
    q2show = Queue(Q2SHOW_MAX_CACHE)

    mics = []
    for port in ports:
        mic = Mic(port.device, q2solve)
        mics.append(mic)
    solve = Solve(ports_num, q2solve, q2show)
    show = Show(q2show)

    for mic in mics:
        mic.start()
    solve.start()
    show.start()

    while True:
        pass

if __name__ == '__main__':
    main()