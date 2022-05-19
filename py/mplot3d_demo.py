from matplotlib import pyplot as plot
import numpy as np
import math
from mpl_toolkits.mplot3d import Axes3D

figure = plot.figure()
axes = Axes3D(figure)

X = np.arange(-10,10,0.25)
Y = np.arange(-10,10,0.25)#前两个参数为自变量取值范围
X,Y = np.meshgrid(X,Y)

Z = np.sqrt(X*X+Y*Y) #z关于x,y的函数关系式,此处为锥面
axes.plot_surface(X,Y,Z,cmap='rainbow')
plot.show()