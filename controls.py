from time import sleep
import pynput
import win32api
import win32con
import win32gui
import ctypes
SendInput = ctypes.windll.user32.SendInput
from CONFIG import CONFIG
import krane_utils

def move_cursor(x, y):
    if not CONFIG['is_aiming']:
        return 
    extra = ctypes.c_ulong(0)
    x = int(x)
    y = int(y)

    ii_ = pynput._util.win32.INPUT_union()
    ii_.mi = pynput._util.win32.MOUSEINPUT(x, y, 0, (0x0001 | 0x8000), 0, ctypes.cast(ctypes.pointer(extra), ctypes.c_void_p))
    command=pynput._util.win32.INPUT(ctypes.c_ulong(0), ii_)
    SendInput(1, ctypes.pointer(command), ctypes.sizeof(command))


def shoot():
    if not CONFIG['is_aiming']:
        return 

    if not krane_utils.is_game_window_focused():
        krane_utils.focus_game_window()
    mouse = pynput.mouse.Controller()
    mouse.press(pynput.mouse.Button.left)
    if not krane_utils.is_game_window_focused():
        krane_utils.focus_game_window()
    sleep(0.1)
    if not krane_utils.is_game_window_focused():
        krane_utils.focus_game_window()
    mouse.release(pynput.mouse.Button.left)
    
    if not krane_utils.is_game_window_focused():
        krane_utils.focus_game_window()

def aim_and_shoot(x,y):
    move_cursor(x,y)
    if abs(x) > CONFIG['shoot_inside_min_range'] and abs(y) > CONFIG['shoot_inside_min_range']:
        return        
    shoot()
    if CONFIG['snap_back_to_reality']:
        move_cursor(-x, -y)

# create thread to listen of mouse click inputs, if the click that is in the config[aim_key] is pressed aim is active if not its not
# use the pynput listener
def listen_for_mouse_click():
    with pynput.mouse.Listener(on_click=click_listenr_logic) as listener:
        listener.join()


def click_listenr_logic(x, y, button, pressed):
    if button == CONFIG["aim_key"]:
        CONFIG['is_aiming'] = pressed
        if pressed:
            print("Aiming")
        else:
            print("Not aiming")
        
    return True


import threading
threading.Thread(target=listen_for_mouse_click).start()
