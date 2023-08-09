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
from word2number import w2n
import json
import math
import queue

COS_45 = math.cos(math.pi / 4)
SIN_45 = math.sin(math.pi / 4)

r = sr.Recognizer()
mic = sr.Microphone()
keyWords = {
    "up left": "up left",
    "up right": "up right",
    "down left": "down left",
    "down right": "down right",
    "downright": "down right",
    "upright": "up right",
    "uplift": "up left",
    "download": "down left",
    "click": "click",
    "down": "down",
    "left": "left",
    "right": "right",
    "up": "up",
    "quick": "click",
    "op": "up",
    "oh": "up",
    "life": "left",
    "like": "left",
    "lift": "left",
    "list": "left",
    "last": "left",
    "the": "down",
}


def listen(audio_queue, exit_program):
    with mic as source:
        r.adjust_for_ambient_noise(source)
        print("Please start speaking.")
        while True:
            if exit_program.value:
                print("Exit listen process")
                break
            audio = r.listen(source, phrase_time_limit=4)
            try:
                audio_queue.put_nowait(audio)
            except queue.Full:
                print("Audio queue is full")


def keyword_detection(audio_queue, exit_program):
    num = 0
    command = ""
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
            try:
                num = w2n.word_to_num(text)
            except:
                num = 0
            for word, keyWord in keyWords.items():
                if word.lower() in text.lower():
                    command = keyWord
                    print("Command: {}".format(command + " " + str(num)))
                    mouse_movement(command, int(num))
                    break

        except Exception:
            if not exit_program.value:
                print("Please speak again.")


def mouse_movement(command, num):
    if command == "click":
        mouse.click("left")
    elif command == "down":
        mouse.move(0, num, absolute=False, duration=num / 1000)
    elif command == "left":
        mouse.move(-num, 0, absolute=False, duration=num / 1000)
    elif command == "right":
        mouse.move(num, 0, absolute=False, duration=num / 1000)
    elif command == "up":
        mouse.move(0, -num, absolute=False, duration=num / 1000)
    elif command == "up left":
        mouse.move(-num * COS_45, -num * SIN_45, absolute=False, duration=num / 1000)
    elif command == "up right":
        mouse.move(num * COS_45, -num * SIN_45, absolute=False, duration=num / 1000)
    elif command == "down left":
        mouse.move(-num * COS_45, num * SIN_45, absolute=False, duration=num / 1000)
    elif command == "down right":
        mouse.move(num * COS_45, num * SIN_45, absolute=False, duration=num / 1000)


def check_key_press(exit_program):
    while True:
        if keyboard.is_pressed("q"):
            print("Exiting the program")
            exit_program.value = True
            break


if __name__ == "__main__":
    multiprocessing_manager = multiprocessing.Manager()
    audio_queue = multiprocessing_manager.Queue(maxsize=3)
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

    print("Exit program")
