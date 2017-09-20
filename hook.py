"""
这个模块构造了一个方便调用的监控键鼠事件的函数库,以及热键。
by 原照萌
"""
from baseconst import *


# global variables


# wParam in LowLevelMouseProc
# https://msdn.microsoft.com/en-us/library/ms644986(v=vs.85).aspx
# 监视鼠标时接受的代码，不用于发送按键。
VM_list = {
    'LD': 0x0201,  # 鼠标左键按下
    'LU': 0x0202,  # 左键抬起
    'RD': 0x0204,  # 鼠标右键按下
    'RU': 0x0205,  # 右键抬起
    'MM': 0x0200,  # 鼠标移动
    'MW': 0x020A,  # 鼠标滚轮滑动
    'MHW': 0x020E  # 鼠标的水平滚轮滑动（卧槽还有这种鼠标？！）
}


hhooks = {"m": 0, "k": 0}  # handle of hooks
cbf_keyboard = None  # the cbf jut mean Callback function
cbf_mouse = None
usercbf_keyboard = None
usercbf_mouse = None
cbf_hotkey = None

WM_UNHOOKMS = WM_USER + 1
WM_UNHOOKKB = WM_USER + 2

# -------------------------------------------------


def starthook(hooktype):
    """
    WH_KEYBOARD_LL = 13 # install a hook for lowlevel keyboard input event
    WH_MOUSE_LL = 14 # isntall a hook for lowlevel mouse input event
    """
    hooktype = hooktype.lower()
    if hooktype == "m":
        hooktypeId = 14
        callfunc = cbf_mouse
        if not callable(usercbf_mouse):
            raise Exception("you must set the callback function.")
    elif hooktype == "k":
        hooktypeId = 13
        callfunc = cbf_keyboard
        if not callable(usercbf_keyboard):
            raise Exception("you must set the callback function.")
    else:
        raise Exception("hooktype must 'be mouse' or 'keyboard'.")

    thhook = SetWindowsHookEx(hooktypeId, callfunc, GetModuleHandle(c_void_p(None)), 0)
    if thhook == 0:
        raise Exception("SetWindowsHookEx failed!")
    else:
        hhooks[hooktype] = thhook
        if hooktype == 'k':
            msg_list[WM_UNHOOKKB] = _unhookkeyboard
        else:
            msg_list[WM_UNHOOKMS] = _unhookmouse


def _unhookkeyboard():
    ret = UnhookWindowsHookEx(hhooks['m'])  # if function succeed.return nonzero
    if ret == 0:
        raise Exception("UnhookWindowsHookEx failed.")
    hhooks['m'] = 0
    del msg_list[WM_UNHOOKKB]


def _unhookmouse():
    ret = UnhookWindowsHookEx(hhooks['m'])  # if function succeed.return nonzero
    if ret == 0:
        raise Exception("UnhookWindowsHookEx failed.")
    hhooks['m'] = 0
    del msg_list[WM_UNHOOKMS]


def stophook(hooktype):
    if hooktype == 'm':
        postmsg(WM_UNHOOKMS)
    elif hooktype == 'k':
        postmsg(WM_UNHOOKKB)
    else:
        Exception("hooktype can only be 'm' or 'k'.")


def _keyboardproc(nCode, wParam, lParam):
    Param = lParam.contents
    args = {'keystatu': wParam, 'keycode': Param.vkCode,
            'scancode': Param.scanCode, 'flags': Param.flags}
    ret = usercbf_keyboard(args)  # return True for not to block ,False to block

    if ret:
        CallNextHookEx(hhooks['k'], nCode, wParam, lParam)
        return 0
    else:
        return 1


def _mouseproc(nCode, wParam, lParam):
    Param = lParam.contents
    args = {'keystatu': wParam, 'x': Param.pt.x, 'y': Param.pt.y,
            'mouseData': Param.mouseData >> 16}

    ret = usercbf_mouse(args)
    if ret:
        CallNextHookEx(hhooks['m'], nCode, wParam, lParam)
        return 0
    else:
        return 1


def setcbf(myfunc, hooktype):
    global usercbf_keyboard, usercbf_mouse, cbf_keyboard, cbf_mouse

    if hooktype.lower() == "k":
        usercbf_keyboard = myfunc
        keyfunctype = WINFUNCTYPE(c_int, c_int, c_int, POINTER(KBDLLHOOKSTRUCT))
        cbf_keyboard = keyfunctype(_keyboardproc)

    elif hooktype.lower() == "m":
        usercbf_mouse = myfunc
        keyfunctype = WINFUNCTYPE(c_int, c_int, c_int, POINTER(MSLLHOOKSTRUCT))
        cbf_mouse = keyfunctype(_mouseproc)


def sethotkey(func, hotid, mode, vkcode):
    # mode must be selected from mod.
    global cbf_hotkey
    cbf_hotkey = func
    ret = RegisterHotKey(c_void_p(None), hotid, mode, vkcode)
    if ret == 0:
        raise Exception("RegisterHotKey failed.")
    else:
        msg_list[WM_HOTKEY] = cbf_hotkey


def unsethotkey(hotid):
    ret = UnregisterHotKey(c_void_p(None), hotid)
    if ret == 0:
        raise Exception("UnregisterHotKey failed.")
    else:
        if WM_HOTKEY in msg_list:
            del msg_list[WM_HOTKEY]


# test keyboard hook
if __name__ == '__main__':
    def test1(args):
        print("vkCode:", args["keycode"])
        if args["keycode"] == 81:
            closeloop()
        return True

    def test2(args):
        print("x,y:", args["x"], args['y'], "0x%04x" % args["keystatu"])
        if args["keystatu"] == VM_list['RU']:
            closeloop()
        return True

    '''
    setcbf(test1, 'k')
    starthook('k')
    print('start loop,press Q to exit.')
    mainloop()

    '''
    setcbf(test2, 'm')
    starthook('m')
    print('start loop,press mouse right button to exit.')
    mainloop()

    print('unlock hook.')
