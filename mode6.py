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
from word2number import w2n
import json

r = sr.Recognizer()
mic = sr.Microphone()
keyWords = {
    "click": "click",
    "stop": "stop",
    "left": "left",
    "right": "right",
}


def listen(audio_queue, exit_program):
    with mic as source:
        r.adjust_for_ambient_noise(source)
        print("Please start speaking.")
        while True:
            if exit_program.value:
                print("Listen exit program")
                break
            audio = r.listen(source, phrase_time_limit=3)
            try:
                audio_queue.put_nowait(audio)
            except:
                print("Audio queue is full")


def keyword_detection(audio_queue, command, angle, exit_program):
    while True:
        if exit_program.value:
            print("Keyword detection exit program")
            break
        try:
            audio = audio_queue.get_nowait()
        except:
            continue

        try:
            cmd = r.recognize_vosk(audio)
            d = json.loads(cmd)
            text = d["text"]
            print("text: " + text)
            command.value = ""
            try:
                num = w2n.word_to_num(text)
            except:
                num = -1

            for word, keyWord in keyWords.items():
                if word.lower() in text.lower():
                    command.value = keyWord
                    break
            print("Command: {}".format(command.value + " " + str(num)))
            if num > -1:
                x = num * math.cos(math.radians(angle.value))
                y = num * math.sin(math.radians(angle.value))
                mouse.move(x, -y, absolute=False, duration=num / 1000)
            else:
                if command.value == "click":
                    mouse.click("left")

        except Exception:
            if not exit_program.value:
                print("Please speak again.")


def cursor_change(command, angle, exit_program):
    while True:
        if exit_program.value:
            print("Cursor change exit program")
            break
        if command.value == "left" or command.value == "right":
            if command.value == "left":
                angle.value += 10
            else:
                angle.value -= 10

            if angle.value == -10:
                angle.value = 350
            if angle.value == 360:
                angle.value = 0

            custom_cursor = win32gui.LoadImage(
                0,
                "cursors/cursor_{}.cur".format(angle.value),
                win32con.IMAGE_CURSOR,
                0,
                0,
                win32con.LR_LOADFROMFILE,
            )
            ctypes.windll.user32.SetSystemCursor(custom_cursor, 32512)
            ctypes.windll.user32.DestroyCursor(custom_cursor)

            time.sleep(0.5)


def check_key_press(exit_program):
    while True:
        if keyboard.is_pressed("q"):
            print("Exiting the program")
            exit_program.value = True
            break


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
    command = multiprocessing_manager.Value(c_char_p, "stani")
    angle = multiprocessing_manager.Value("i", 0)
    exit_program = multiprocessing_manager.Value(c_bool, False)

    p1 = multiprocessing.Process(
        target=listen,
        args=(
            audio_queue,
            exit_program,
        ),
    )

    p2 = multiprocessing.Process(
        target=keyword_detection,
        args=(
            audio_queue,
            command,
            angle,
            exit_program,
        ),
    )
    p3 = multiprocessing.Process(
        target=cursor_change,
        args=(
            command,
            angle,
            exit_program,
        ),
    )
    p4 = multiprocessing.Process(target=check_key_press, args=(exit_program,))

    p1.start()
    p2.start()
    p3.start()
    p4.start()

    p1.join()
    p2.join()
    p3.join()
    p4.join()

    ctypes.windll.user32.SetSystemCursor(save_system_cursor, 32512)
    ctypes.windll.user32.DestroyCursor(save_system_cursor)
