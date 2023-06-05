# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 08:02:22 2023

@author: Valentina
"""

import keyboard
import win32con
import win32gui
import ctypes
import time
import speech_recognition as sr
import mouse
import multiprocessing
from ctypes import c_char_p, c_bool
import math
import re

r = sr.Recognizer()
mic = sr.Microphone()
keyWords = ['stani', 'lijevo', 'desno', 'klik']

def keyword_detection(command, angle, exit_program):
    with mic as source:
        r.adjust_for_ambient_noise(source)
        print('Please start speaking.')
        while True: 
            if exit_program.value: break
            audio = r.listen(source, phrase_time_limit=3)
            try:
                text = r.recognize_google(audio, language = "hr-HR")
                print(text)
                if bool(re.search('\d', text)):
                    number = int(re.search(r'\d+', text).group()) // 10 * 10
                    x = number * math.cos(math.radians(angle.value))
                    y = number * math.sin(math.radians(angle.value))
                    mouse.move(x, -y, absolute=False, duration=number / 1000)
                else:      
                    for index, keyWord in enumerate(keyWords):
                        if keyWord.lower() in text.lower() or keyWord[-3:] in text.lower():
                            command.value = keyWord
                            if(command.value) == 'klik': mouse.click('left')
                            print("Command: {}".format(command.value))
                            break
            except Exception:
                if not exit_program.value: print('Please speak again.')
    
def cursor_change(command, angle, exit_program):
    i = 0
    while True:
        if exit_program.value: break
        if command.value == 'lijevo' or command.value == 'desno':
            angle.value = i * 10
            custom_cursor = win32gui.LoadImage(0, "cursors/cursor_{}.cur".format(angle.value), win32con.IMAGE_CURSOR, 
                                        0, 0, win32con.LR_LOADFROMFILE);
            ctypes.windll.user32.SetSystemCursor(custom_cursor, 32512)
            ctypes.windll.user32.DestroyCursor(custom_cursor)
            
            if command.value == 'lijevo': i += 1
            else: i -= 1
            
            if i == -1: i = 35
            i %= 36    
            time.sleep(0.5)

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
    command = menager.Value(c_char_p, "stani")
    angle = menager.Value('i', 0)
    exit_program = menager.Value(c_bool, False)
    
    p1 = multiprocessing.Process(target=keyword_detection, args=(command,angle, exit_program,))
    p2 = multiprocessing.Process(target=cursor_change, args=(command, angle, exit_program,))
    p3 = multiprocessing.Process(target=check_key_press, args=(exit_program,))
    
    p1.start()
    p2.start()
    p3.start()

    p1.join()
    p2.join()
    p3.join()
    
    ctypes.windll.user32.SetSystemCursor(save_system_cursor, 32512)
    ctypes.windll.user32.DestroyCursor(save_system_cursor);



    