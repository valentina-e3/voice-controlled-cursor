# -*- coding: utf-8 -*-
"""
@author: Valentina Ecimović
"""

import multiprocessing
from ctypes import c_char_p, c_bool
from shared_processes import listen,keyword_detection, check_key_press, mouse_movement
from utils import angles_from_commands

CURSOR_STEP_SIZE = 2
PHRASE_TIME_LIMIT = 1

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

cursor_move_keywords = {
    "up", "down", "left", "right", "up right", "up left", "down right", "down left",
}

def mode_processor(args):
    command = args["command"]
    return (None, angles_from_commands[command], f"{command}")

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
        target=mouse_movement,
        args=(
            cursor_move_keywords,
            CURSOR_STEP_SIZE,
            command,
            angle,
            exit_program,
        ),
    )
    p4 = multiprocessing.Process(
        target=check_key_press,
        args=(exit_program,),
    )

    p1.start()
    p2.start()
    p3.start()
    p4.start()

    p1.join()
    p2.join()
    p3.join()
    p4.join()

    print("Exit program")
