# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 18:19:25 2022

@author: Valentina
"""

import speech_recognition as sr
import mouse
import keyboard
import multiprocessing
from ctypes import c_bool
import re

r = sr.Recognizer()
mic = sr.Microphone()
keyWords = ['dolje lijevo', 'gore lijevo', 'dolje desno', 'gore desno','klik','dolje', 'lijevo', 'desno', 'gore', 'stani']

def keyword_detection(exit_program):
    num = 0
    command = ""
    with mic as source:
        r.adjust_for_ambient_noise(source)
        print('Please start speaking.')
        while True: 
            if exit_program.value: break
            audio = r.listen(source, phrase_time_limit=4)
            try:
                text = r.recognize_google(audio, language = "hr-HR")
                
                if bool(re.search('\d', text)):
                    num = re.search(r'\d+', text).group() 
                elif keyWords[4].lower() in text:
                    num = 0
                else:
                    raise ValueError("You need to provide a number for the step") 
                print(text)
                for index, keyWord in enumerate(keyWords):
                    if keyWord.lower() in text.lower() or (index > 3 and keyWord[-3:] in text.lower()):
                        command = keyWord
                        print("Command: {}".format(command + " " + str(num)))
                        mouse_movement(command,int(num))      
                        break
                
            except Exception:
                if not exit_program.value: print('Please speak again.')

                
def mouse_movement(command, num):
    if command == keyWords[4]:
        mouse.click('left')
        command.value = ""
    elif command == keyWords[0]:
        mouse.move(-num, num, absolute=False, duration=num / 1000)
    elif command == keyWords[1]:
        mouse.move(-num, -num, absolute=False, duration=num / 1000)
    elif command == keyWords[2]:
        mouse.move(num, num, absolute=False, duration=num / 1000)
    elif command == keyWords[3]:
        mouse.move(num, -num, absolute=False, duration=num / 1000)
    elif command == keyWords[5]:
        mouse.move(0, num, absolute=False, duration=num / 1000)
    elif command == keyWords[6]:
        mouse.move(-num, 0, absolute=False, duration=num / 1000)
    elif command == keyWords[7]:
        mouse.move(num, 0, absolute=False, duration=num / 1000)  
    elif command == keyWords[8]:
        mouse.move(0, -num, absolute=False, duration=num / 1000)

def check_key_press(exit_program):
    while True:
        if keyboard.is_pressed('q'):
            print('Exiting the program')
            exit_program.value = True
            break

if __name__ == "__main__":
    menager = multiprocessing.Manager()
    exit_program = menager.Value(c_bool, False)
    
    p1 = multiprocessing.Process(target=keyword_detection, args=(exit_program,))
    p2 = multiprocessing.Process(target=check_key_press, args=(exit_program,))
    
    p1.start()
    p2.start()
      
    p1.join()
    p2.join()
