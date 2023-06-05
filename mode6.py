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
import keyboard
import mouse
import math
import re
from ctypes import c_char_p, c_bool

r = sr.Recognizer()
mic = sr.Microphone()

def keyword_detection(angle, exit_program):
    
    with mic as source:
        r.adjust_for_ambient_noise(source)
        print('Please start speaking.')
        while True: 
            if exit_program.value: break
            audio = r.listen(source, phrase_time_limit=5)
            
            try:
                text = r.recognize_google(audio, language = "hr-HR")
                print(text)
                if bool(re.search('\d', text)):
                    number = int(re.search(r'\d+', text).group()) // 10 * 10
                    if 'kreni' in text.lower():
                        x = number * math.cos(math.radians(angle.value))
                        y = number * math.sin(math.radians(angle.value))
                        mouse.move(x, -y, absolute=False, duration=number / 1000)
                    else:                
                        angle_increment = number
                        angle.value = (angle.value + angle_increment) % 360
                        cursor_change(angle.value)
                else:
                    if "klik" in text.lower() or "ik" in text.lower():
                        mouse.click('left')
                    
            except Exception:
                if not exit_program.value: print('Please speak again.')


def cursor_change(angle):
    custom_cursor = win32gui.LoadImage(0, "cursors/cursor_{}.cur".format(angle), win32con.IMAGE_CURSOR, 
                                0, 0, win32con.LR_LOADFROMFILE);
    ctypes.windll.user32.SetSystemCursor(custom_cursor, 32512)
    ctypes.windll.user32.DestroyCursor(custom_cursor)


def check_key_press(exit_program):
    while True:
        if keyboard.is_pressed('q'):
            print('Exiting the program')
            exit_program.value = True
            break
        
if __name__ == "__main__":
    cursor = win32gui.LoadImage(0, 32512, win32con.IMAGE_CURSOR, 
                                0, 0, win32con.LR_SHARED)
    save_system_cursor = ctypes.windll.user32.CopyImage(cursor, win32con.IMAGE_CURSOR, 
                                0, 0, win32con.LR_COPYFROMRESOURCE)
    custom_cursor = win32gui.LoadImage(0, "cursors/cursor_0.cur", win32con.IMAGE_CURSOR, 
                                    0, 0, win32con.LR_LOADFROMFILE);

    ctypes.windll.user32.SetSystemCursor(custom_cursor, 32512)
    
    menager = multiprocessing.Manager()
    angle = menager.Value('i', 0)
    exit_program = menager.Value(c_bool, False)
    
    p1 = multiprocessing.Process(target=keyword_detection, args=(angle,exit_program,))
    p2 = multiprocessing.Process(target=check_key_press, args=(exit_program,))
    
    p1.start()
    p2.start()

    p1.join()
    p2.join()
    
    ctypes.windll.user32.SetSystemCursor(save_system_cursor, 32512)
    ctypes.windll.user32.DestroyCursor(save_system_cursor);