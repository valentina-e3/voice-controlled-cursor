# -*- coding: utf-8 -*-
"""
Created on Wed Jan 18 18:25:57 2023

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
keyWords = ['kreni', 'stani', 'klik']

def keyword_detection(command, angle, exit_program):
    
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
                    angle_increment = int(re.search(r'\d+', text).group()) // 10 * 10
                    angle.value = (angle.value + angle_increment) % 360
                    command.value = 'stani'
                    cursor_change(angle.value)
                    
                for index, keyWord in enumerate(keyWords):
                    if keyWord.lower() in text.lower() or keyWord[-3:] in text.lower():
                        command.value = keyWord
                        break  
            except Exception:
                if not exit_program.value: print('Please speak again.')

def mouse_movement(command, angle, exit_program):
    while True:
        if exit_program.value: break
        if command.value == 'klik':
            mouse.click('left')
            command.value = 'stani'
        elif command.value == 'kreni':
            x = 3 * math.cos(math.radians(angle.value))
            y = 3 * math.sin(math.radians(angle.value))
            mouse.move(x, -y, absolute=False, duration=0.06)

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
    command = menager.Value(c_char_p, "stani")
    angle = menager.Value('i', 0)
    exit_program = menager.Value(c_bool, False)
    
    p1 = multiprocessing.Process(target=keyword_detection, args=(command,angle,exit_program,))
    p2 = multiprocessing.Process(target=mouse_movement, args=(command, angle, exit_program,))
    p3 = multiprocessing.Process(target=check_key_press, args=(exit_program,))
    
    p1.start()
    p2.start()
    p3.start()

    p1.join()
    p2.join()
    p3.join()
    
    ctypes.windll.user32.SetSystemCursor(save_system_cursor, 32512)
    ctypes.windll.user32.DestroyCursor(save_system_cursor);