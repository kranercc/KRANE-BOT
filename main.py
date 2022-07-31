import sys
import threading
from time import time, sleep

from CONFIG import CONFIG
import controls
import cv2
import win32gui, win32ui, win32con, win32api
import numpy as np
import torch
import krane_utils
import os
import multiprocessing

CLASS_NAMES = []
with open("model/coco.names", 'r') as f:
    for line in f:
        CLASS_NAMES.append(line.strip())

model = torch.hub.load("ultralytics/yolov5", "yolov5n")
# model = torch.hub.load("ultralytics/yolov5", 'custom',
#                        path="C:/Users/iacob/Desktop/trainer/yolov5/runs/train/exp6/weights/best.pt")
device = torch.device('cuda')
model.to(device)

grab_screen = krane_utils.grab_screen
SCREEN_CENTER_COORDS = (
    win32api.GetSystemMetrics(win32con.SM_CXSCREEN) // 2,
    win32api.GetSystemMetrics(win32con.SM_CYSCREEN) // 2,
)

block_shooting = False
last_frame = "trash"

def calculate_chunk(chunk):
    try:
        start_time = time()
        result = model(chunk)
        end_time = time()
        print("Time: " + str(end_time - start_time))
    except:
        return None
    return result


def analyze_to_shoot(frame_copy):
    global block_shooting, top_thread_running, bottom_thread_running, Thread_Pool
    frame_center = (frame_copy.shape[1] // 2, frame_copy.shape[0] // 2)

    result = model(frame_copy)
    data = result.xyxy[0]
    if len(data) > 0:
        data = data[0]
        xmin = int(data[0])
        ymin = int(data[1])
        xmax = int(data[2])
        ymax = int(data[3])
        confidence = data[4]
        class_id = int(data[5])
        if class_id == CONFIG['object_class_id'] and confidence > CONFIG['confidence']:
            aiming_x = ((xmin + xmax) // 2) - frame_center[0]
            aiming_y = ((ymin + ymax) // 2) - frame_center[1]
            cv2.rectangle(last_frame, (xmin, ymin), (xmax, ymax), (100, 0, 0), 2)
            if not block_shooting:
                block_shooting = True
                controls.aim_and_shoot(aiming_x, aiming_y)
            block_shooting = False

def th_grab_screen():
    global last_frame
    while True:
        last_frame = grab_screen(region=(
            SCREEN_CENTER_COORDS[0] - CONFIG['window_size'], SCREEN_CENTER_COORDS[1] - CONFIG['window_size'],
            SCREEN_CENTER_COORDS[0] + CONFIG['window_size'], SCREEN_CENTER_COORDS[1] + CONFIG['window_size']))


threading.Thread(target=th_grab_screen).start()

logic_fps = 0
def th_preview():
    global last_frame, logic_fps
    while True:
        cv2.putText(last_frame, "FPS: " + str(logic_fps), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        cv2.imshow(CONFIG['window_name'], last_frame)
        cv2.waitKey(1)

sleep(2)
threading.Thread(target=th_preview).start()

while True:
    if krane_utils.is_game_window_focused():
        start_time = time()

        analyze_to_shoot(last_frame)

        logic_fps = 1 / (time() - start_time)
