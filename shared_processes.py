import speech_recognition as sr
import mouse
import keyboard
import json
import queue
import time
from word2number import w2n
from utils import move_mouse_cursor, set_custom_cursor
import inspect

CURSOR_SPEED = 133.33

r = sr.Recognizer()
mic = sr.Microphone()

def listen(audio_queue, phrase_time_limit, exit_program):
    with mic as source:
        r.adjust_for_ambient_noise(source)
        print("Please start speaking.")
        while True:
            if exit_program.value:
                print("Exit listen process")
                break
            audio = r.listen(source, phrase_time_limit=phrase_time_limit)
            try:
                audio_queue.put_nowait(audio)
            except queue.Full:
                print("Audio queue is full")

def keyword_detection(mode_processor, keywords, audio_queue, command, angle, exit_program):
    def process_command():
        command_val = command.value
        if command_val == "click":
            mouse.click("left")
            command.value = "stop"
            return "click"
        elif command_val != "stop":
            mode_processor_args = {
                "command": command_val,
                "angle": angle.value,
                "num": num_value,
            }
            new_command_val,new_angle_val,cmd_output = mode_processor(mode_processor_args)

            if new_angle_val is not None: angle.value = new_angle_val
            if new_command_val is not None: command.value = new_command_val
            return cmd_output
        return command_val

    while True:
        if exit_program and exit_program.value:
            print("Exit keyword detection process")
            break
        try:
            audio = audio_queue.get_nowait()
        except queue.Empty:
            continue

        try:
            text = json.loads(r.recognize_vosk(audio)).get("text", "").lower()
            if(text != ""):
                print(f"text: {text}")

                words = text.split()
                matching_keywords = set(words).intersection(keywords)
                num_value = None
                try:
                    num_value = w2n.word_to_num(text)
                except:
                    pass

                if matching_keywords:
                    command.value = keywords[next(iter(matching_keywords))]
                elif num_value is not None:
                    command.value = None  
                else:
                    continue

                cmd_output = process_command()
                if cmd_output:
                    print(f"Command: {cmd_output}")

        except Exception as e:
            if not exit_program or not exit_program.value:
                print("Please speak again.", e)




def check_key_press(exit_program):
    while True:
        if keyboard.is_pressed("q"):
            print("Exiting the program")
            exit_program.value = True
            break

def mouse_movement(cursor_move_keywords, cursor_step_size, command, angle, exit_program):
    while True:
        if exit_program.value:
            print("Exit mouse movement process")
            break
        elif command.value in cursor_move_keywords:
            move_mouse_cursor(cursor_step_size, angle.value, cursor_step_size / CURSOR_SPEED)



def cursor_change(command, angle, exit_program):
    while True:
        if exit_program.value:
            print("Exit cursor change process")
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

            set_custom_cursor(angle.value)

            time.sleep(0.5)
