# -*- coding: utf-8 -*-
"""
@author: Valentina
"""

import speech_recognition as sr
import mouse
import keyboard
import multiprocessing
from ctypes import c_char_p, c_bool
import time
from datetime import datetime
import vosk

r = sr.Recognizer()
mic = sr.Microphone()
keyWords = ['dolje lijevo', 'gore lijevo', 'dolje desno', 'gore desno','klik','dolje', 'lijevo', 'desno', 'gore', 'stani']

def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

def keyword_detection(command, exit_program):
    with mic as source:
        r.adjust_for_ambient_noise(source)
        print('Please start speaking.')
        while True: 
            if exit_program.value: break
           # print("Start listen: " + get_current_time())
            audio = r.listen(source, phrase_time_limit=1.5)
            #print("End listen: " + get_current_time())
            try:
             #   print("Start recognition: " + get_current_time())
                text = r.recognize_google(audio)
              #  print("Start recognition: " + get_current_time())
                print("text: " + text)
                for index, keyWord in enumerate(keyWords):
                    if keyWord.lower() in text.lower() or (index > 3 and keyWord[-3:] in text.lower()) or (index > 3 and keyWord[:3] in text.lower()):
                        command.value = keyWord
                        print("Command: {}".format(command.value))
                        break
                    
            except Exception:
                if not exit_program.value: print('Please speak again.')

def mouse_movement(command, exit_program):   
    while True:
        if exit_program.value: break
        if command.value == keyWords[4]:
            mouse.click('left')
            command.value = keyWords[9]
        elif command.value == keyWords[0]:
            mouse.move(-1, 1, absolute=False, duration=0.0141)
        elif command.value == keyWords[1]:
            mouse.move(-1, -1, absolute=False, duration=0.0141)
        elif command.value == keyWords[2]:
            mouse.move(1, 1, absolute=False, duration=0.0141)
        elif command.value == keyWords[3]:
            mouse.move(1, -1, absolute=False, duration=0.0141)
        elif command.value == keyWords[5]:
            mouse.move(0, 1, absolute=False, duration=0.01)
        elif command.value == keyWords[6]:
            mouse.move(-1, 0, absolute=False, duration=0.01)
        elif command.value == keyWords[7]:
            mouse.move(1, 0, absolute=False, duration=0.01)  
        elif command.value == keyWords[8]:
            mouse.move(0, -1, absolute=False, duration=0.01)

def check_key_press(exit_program):
    while True:
        if keyboard.is_pressed('q'):
            print('Exiting the program')
            exit_program.value = True
            break

if __name__ == "__main__":
    menager = multiprocessing.Manager()
    command = menager.Value(c_char_p, "stani")
    exit_program = menager.Value(c_bool, False)
    
    p1 = multiprocessing.Process(target=keyword_detection, args=(command,exit_program,))
    p2 = multiprocessing.Process(target=mouse_movement, args=(command,exit_program,))
    p3 = multiprocessing.Process(target=check_key_press, args=(exit_program,))
    
    p1.start()
    p2.start()
    p3.start()
      
    p1.join()
    p2.join()
    p3.join()
    
  
    