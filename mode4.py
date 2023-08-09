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
from ctypes import c_bool
from word2number import w2n
import json
import queue

r = sr.Recognizer()
mic = sr.Microphone()

keyWords = {
    "click": "click",
    "go": "go",
    "quick": "click",
}


def listen(audio_queue, exit_program):
    with mic as source:
        r.adjust_for_ambient_noise(source)
        print("Please start speaking.")
        while True:
            if exit_program.value:
                print("Exit listen process")
                break
            audio = r.listen(source, phrase_time_limit=3)
            try:
                audio_queue.put_nowait(audio)
            except queue.Full:
                print("Audio queue is full")


def keyword_detection(audio_queue, angle, exit_program):
    while True:
        if exit_program.value:
            print("Exit keyword detection process")
            break
        try:
            audio = audio_queue.get_nowait()
        except queue.Empty:
            continue

        try:
            text = json.loads(r.recognize_vosk(audio))["text"]
            print("text: " + text)
            command = ""
            try:
                num = w2n.word_to_num(text)
            except:
                num = -1

            for word, keyWord in keyWords.items():
                if word.lower() in text.lower():
                    command = keyWord
                    break
            print("Command: {}".format(command + " " + str(num)))
            if num > -1:
                if command == "go":
                    x = num * math.cos(math.radians(angle.value))
                    y = num * math.sin(math.radians(angle.value))
                    mouse.move(x, -y, absolute=False, duration=num / 1000)
                else:
                    angle.value = (num // 10 * 10) % 360
                    set_custom_cursor(angle.value)

            else:
                if command == "click":
                    mouse.click("left")

        except Exception:
            if not exit_program.value:
                print("Please speak again.")


def set_custom_cursor(angle):
    custom_cursor = win32gui.LoadImage(
        0,
        "cursors/cursor_{}.cur".format(angle),
        win32con.IMAGE_CURSOR,
        0,
        0,
        win32con.LR_LOADFROMFILE,
    )
    ctypes.windll.user32.SetSystemCursor(custom_cursor, 32512)
    ctypes.windll.user32.DestroyCursor(custom_cursor)


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
