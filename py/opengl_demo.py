from OpenGL.GL import *

from OpenGL.GLU import *
from OpenGL.GLUT import *


def drawFunc():
    #清楚之前画面
    glClear(GL_COLOR_BUFFER_BIT)
    glRotatef(0.1, 0,5,0)   #(角度,x,y,z)
    glutWireTeapot(0.5)
    #刷新显示
    glFlush()
    
#使用glut初始化OpenGL
glutInit()
#显示模式:GLUT_SINGLE无缓冲直接显示|GLUT_RGBA采用RGB(A非alpha)
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGBA)
#窗口位置及大小-生成
glutInitWindowPosition(0,0)
glutInitWindowSize(400,400)
glutCreateWindow(b"first")
#调用函数绘制图像
glutDisplayFunc(drawFunc)
glutIdleFunc(drawFunc)
#主循环
glutMainLoop()