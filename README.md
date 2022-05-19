# 声音定位系统

## 目录结构

- mpy：micropython K210单片机程序

- py：电脑端python程序

## 相关依赖

### OpenGL

1. 安装python库

   请在以下链接中下载对应版本的whl文件，并使用`pip install .whl` 在本地安装

   https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyopengl

    > 不可以使用 pip install PyOpenGL PyOpenGL_accelerate，这样默认安装的是32位版本，在64位系统上会运行会报错

2. 下载相关dll文件

   在这里下载相关的dll文件：http://pan.baidu.com/s/1dFhC8G5

   可放在和.py文件相同的目录下，也可放在系统PATH下（如果提示有同名文件，最好选择跳过而不要替换）

   - 32位系统：C:\Windows\System32
   - 64位系统：C:\Windows\SysWOW64
