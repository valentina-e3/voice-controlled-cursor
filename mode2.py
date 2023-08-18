# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 18:19:25 2022

@author: Valentina
"""

import multiprocessing
from ctypes import c_bool, c_char_p
from shared_processes import listen, keyword_detection, check_key_press
from utils import angles_from_commands, move_mouse_cursor

PHRASE_TIME_LIMIT = 3

keywords = {
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

def mode_processor(args):
    command = args["command"]
    num = args["num"]
    if num is not None:
        move_mouse_cursor(num, angles_from_commands[command], num / 1000)
    return (None, "stop", f"{command} {num}")

if __name__ == "__main__":
    multiprocessing_manager = multiprocessing.Manager()
    audio_queue = multiprocessing_manager.Queue(maxsize=3)
    command = multiprocessing_manager.Value(c_char_p, "stop")
    exit_program = multiprocessing_manager.Value(c_bool, False)
    angle = multiprocessing_manager.Value("i", 0)

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

    print("Exit program")
