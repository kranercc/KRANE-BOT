import win32gui
import win32con
import win32api
import win32ui
import numpy as np
import cv2
from time import time

from CONFIG import CONFIG
def is_game_window_focused():
    return win32gui.GetWindowText(win32gui.GetForegroundWindow()) == CONFIG["window_name"]

def focus_game_window():
    win32gui.SetForegroundWindow(win32gui.FindWindow(None, CONFIG["window_name"]))
    # if it's minimized, then get it up
    if win32gui.GetWindowPlacement(win32gui.FindWindow(None, CONFIG["window_name"]))[1] == win32con.SW_SHOWMINIMIZED:
        win32gui.ShowWindow(win32gui.FindWindow(None, CONFIG["window_name"]), win32con.SW_RESTORE)

def grab_screen(region=None):
    start_time = time()
    hwin = win32gui.GetDesktopWindow()
    if region:
            left,top,x2,y2 = region
            width = x2 - left + 1
            height = y2 - top + 1
    else:
        width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
        height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
        top = 0
        left = 0

    hwindc = win32gui.GetWindowDC(hwin)
    srcdc = win32ui.CreateDCFromHandle(hwindc)
    memdc = srcdc.CreateCompatibleDC()
    bmp = win32ui.CreateBitmap()
    bmp.CreateCompatibleBitmap(srcdc, width, height)
    memdc.SelectObject(bmp)
    memdc.BitBlt((0, 0), (width, height), srcdc, (left, top), win32con.SRCCOPY)

    signedIntsArray = bmp.GetBitmapBits(True)
    img = np.frombuffer(signedIntsArray, dtype='uint8')
    img.shape = (height,width,4)

    srcdc.DeleteDC()
    memdc.DeleteDC()
    win32gui.ReleaseDC(hwin, hwindc)
    win32gui.DeleteObject(bmp.GetHandle())
    img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
    return img
