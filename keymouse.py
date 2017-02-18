"""
这个模块封装了一些模拟鼠标键盘输出的函数
"""
from baseconst import *

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
    # keypress([VK['VK_LWIN'], ord('Q')])
    x, y = getpos()
    # setpos(0,0)
    print(x, y)
