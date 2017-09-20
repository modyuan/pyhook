"""
这个模块封装了一些模拟鼠标键盘输出的函数
"""
from baseconst import *
import time


# 并不是底层的函数，只能对活动窗口起作用。


# mouse event,for sending mouse keys
# https://msdn.microsoft.com/en-us/library/windows/desktop/ms646260(v=vs.85).aspx
# 鼠标的虚拟按键代码，发送按键时用的参数，不用于监控按键

ME_list = {
    'LD': 0x0002,  # mouse left button down
    'LU': 0x0004,  # mouse left button up
    'LP': 0x2 | 0x4,  # mouse left press
    'MD': 0x0020,  # middle button
    'MU': 0x0040,
    'MP': 0x20 | 0x40,
    'RD': 0x0008,  # right button
    'RU': 0x0010,
    'RP': 0x8 | 0x10,
    'WHEEL': 0x0800  # the wheel move,The amount of movement is specified in dwData
}



def keydown(vkcode):
    keybd_event(vkcode, 0, 0, 0)


def keyup(vkcode):
    keybd_event(vkcode, 0, 2, 0)


def keypress(vkcode_list):
    for i in vkcode_list:
        keydown(i)
    for i in vkcode_list:
        keyup(i)


def mouse(vmcode):
    mouse_event(vmcode, 0, 0, 0, c_void_p(None))


def setpos(x, y):
    SetCursorPos(x, y)


def getpos():
    point = POINT()
    GetCursorPos(byref(point))
    return point.x, point.y


if __name__ == '__main__':
    #print(vk.Q)
    #keypress([vk.VK_LWIN, vk.Q])
    x, y = getpos()
    print(x, y)
   # setpos(1900, 0)
    time.sleep(1)
    mouse(ME_list["RP"])

