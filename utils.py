import math
import win32con
import win32gui
import ctypes
import mouse

angles_from_commands = {
    "up": 90,
    "down": 270,
    "left": 180,
    "right": 0,
    "up right": 45,
    "down right": 315,
    "up left": 135,
    "down_left": 225,
}

def move_mouse_cursor(cursor_step_size, angle, duration):
    x = cursor_step_size * math.cos(math.radians(angle))
    y = cursor_step_size * math.sin(math.radians(angle))
    mouse.move(x, -y, absolute=False, duration=duration)

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