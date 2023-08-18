# -*- coding: utf-8 -*-
"""
Created on Sat Mar  4 11:51:21 2023

@author: Valentina
"""

import win32con
import win32gui
import ctypes
import speech_recognition as sr
import multiprocessing
from ctypes import c_char_p,c_bool
from shared_processes import listen, keyword_detection, check_key_press
from utils import move_mouse_cursor, set_custom_cursor

r = sr.Recognizer()
mic = sr.Microphone()

PHRASE_TIME_LIMIT = 3

keywords = {
    "click": "click",
    "go": "go",
    "quick": "click",
}

def mode_processor(args):
    command = args["command"]
    angle = args["angle"]
    num = args["num"]
    if command == "go":
        move_mouse_cursor(num, angle, num / 1000)
        return (None, None, f"{command} {num}")
    elif num is not None:
        new_angle_val = (num // 10 * 10) % 360
        set_custom_cursor(new_angle_val)
        return ("stop", new_angle_val, str(num))
        

if __name__ == "__main__":
    cursor = win32gui.LoadImage(
        0, 32512, win32con.IMAGE_CURSOR, 0, 0, win32con.LR_SHARED
    )
    save_system_cursor = ctypes.windll.user32.CopyImage(
        cursor, win32con.IMAGE_CURSOR, 0, 0, win32con.LR_COPYFROMRESOURCE
    )
    custom_cursor = win32gui.LoadImage(
        0, "cursors/cursor_0.cur", win32con.IMAGE_CURSOR, 0, 0, win32con.LR_LOADFROMFILE
    )

    ctypes.windll.user32.SetSystemCursor(custom_cursor, 32512)

    multiprocessing_manager = multiprocessing.Manager()
    audio_queue = multiprocessing_manager.Queue(maxsize=3)
    command = multiprocessing_manager.Value(c_char_p, "stop")
    angle = multiprocessing_manager.Value("i", 0)
    exit_program = multiprocessing_manager.Value(c_bool, False)

    p1 = multiprocessing.Process(
        target=listen,
        args=(
            audio_queue,
            PHRASE_TIME_LIMIT,
            exit_program,
        ),
    )
    p2 = multiprocessing.Process(
        target=keyword_detection,
        args=(
            mode_processor,
            keywords,
            audio_queue,
            command,
            angle,
            exit_program,
        ),
    )
    p3 = multiprocessing.Process(
        target=check_key_press,
        args=(exit_program,),
    )

    p1.start()
    p2.start()
    p3.start()

    p1.join()
    p2.join()
    p3.join()

    ctypes.windll.user32.SetSystemCursor(save_system_cursor, 32512)
    ctypes.windll.user32.DestroyCursor(save_system_cursor)

    print("Exit program")
