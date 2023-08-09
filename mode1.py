# -*- coding: utf-8 -*-
"""
@author: Valentina Ecimović
"""
import speech_recognition as sr
import mouse
import keyboard
import multiprocessing
from ctypes import c_char_p, c_bool
import time
from datetime import datetime
import vosk
import json

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
    "stop": "stop",
    "up": "up",
    "quick": "click",
    "top": "stop",
    "oh": "up",
    "ah": "up",
    "life": "left",
    "like": "left",
    "lift": "left",
    "list": "left",
    "last": "left",
    "the": "down",
    "nope": "stop",
    "dope": "stop",
    "spot": "stop",
    "scope": "stop",
}


def listen(audio_queue, exit_program):
    with mic as source:
        r.adjust_for_ambient_noise(source)
        print("Please start speaking.")
        while True:
            if exit_program.value:
                print("Listen exit program")
                break
            audio = r.listen(source, phrase_time_limit=1)
            try:
                audio_queue.put_nowait(audio)
            except:
                print("Audio queue is full")


def keyword_detection(audio_queue, command, exit_program):
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
            for word, keyWord in keyWords.items():
                if word.lower() in text.lower():
                    command.value = keyWord
                    print("Command: {}".format(command.value))
                    break

        except Exception:
            if not exit_program.value:
                print("Please speak again.")


def mouse_movement(command, exit_program):
    while True:
        if exit_program.value:
            print("Mouse movement exit program")
            break

        if command.value == "click":
            mouse.click("left")
            command.value = "stop"
        elif command.value == "down":
            mouse.move(0, 1, absolute=False, duration=0.0075)
        elif command.value == "left":
            mouse.move(-1, 0, absolute=False, duration=0.0075)
        elif command.value == "right":
            mouse.move(1, 0, absolute=False, duration=0.0075)
        elif command.value == "up":
            mouse.move(0, -1, absolute=False, duration=0.0075)
        elif command.value == "up left":
            mouse.move(-1, -1, absolute=False, duration=0.0106)
        elif command.value == "up right":
            mouse.move(1, -1, absolute=False, duration=0.0106)
        elif command.value == "down left":
            mouse.move(-1, 1, absolute=False, duration=0.0106)
        elif command.value == "down right":
            mouse.move(1, 1, absolute=False, duration=0.0106)


def check_key_press(exit_program):
    while True:
        if keyboard.is_pressed("q"):
            print("Exiting the program")
            exit_program.value = True
            break


if __name__ == "__main__":
    multiprocessing_manager = multiprocessing.Manager()
    audio_queue = multiprocessing_manager.Queue(maxsize=3)
    command = multiprocessing_manager.Value(c_char_p, "stop")
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
            exit_program,
        ),
    )
    p3 = multiprocessing.Process(
        target=mouse_movement,
        args=(
            command,
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

    print("End program")
