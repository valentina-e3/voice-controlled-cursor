# -*- coding: utf-8 -*-
"""
Created on Wed May 17 20:09:57 2023

@author: Valentina
"""

import tkinter as tk
from tkinter import ttk
import time
import csv


BUTTON_ORDER = [0, 1, 2, 3, 4]  # Define the correct order of button clicks
current_button = 0
start_time = 0

def save_results(username, mode, elapsed_time):
   with open('mode_testing_results.csv', 'a') as f:
    # create the csv writer
    writer = csv.writer(f)

    # write a row to the csv file
    writer.writerow([username, mode, elapsed_time])

def show_start_button():
    username = username_entry.get()
    mode = mode_combobox.get()

    username_label.config(text="Username: " + username)
    mode_label.config(text="Mode: " + mode)

    username_label.place(x=root.winfo_screenwidth() - 20, y=20, anchor="ne")
    mode_label.place(x=root.winfo_screenwidth() - 20, y=50, anchor="ne")

    start_button.place(x=root.winfo_screenwidth() // 2, y=root.winfo_screenheight() // 2, anchor="center")

    username_entry_label.place_forget()
    username_entry.place_forget()
    mode_combobox_label.place_forget()
    mode_combobox.place_forget()
    ok_button.place_forget()
    
def show_buttons():
    button1.place(x=1300, y=100)
    button2.place(x=350, y=480)
    button3.place(x=0, y=0)
    button4.place(x=1000, y=700)
    button5.place(x=650, y=50)

def show_input_fields():
    username_label.place_forget()
    mode_label.place_forget()

    start_button.place_forget()

    button1.place_forget()
    button2.place_forget()
    button3.place_forget()
    button4.place_forget()
    button5.place_forget()
    
    username_entry_label.place(x=root.winfo_screenwidth() // 2 - 100,  y=root.winfo_screenheight() // 2 - 180)
    username_entry.place(x=root.winfo_screenwidth() // 2 - 100,  y=root.winfo_screenheight() // 2 - 150)
    mode_combobox_label.place(x=root.winfo_screenwidth() // 2 - 100,  y=root.winfo_screenheight() // 2 - 120)
    mode_combobox.place(x=root.winfo_screenwidth() // 2 - 100,  y=root.winfo_screenheight() // 2 - 90)
    ok_button.place(x=root.winfo_screenwidth() // 2 + 55,  y=root.winfo_screenheight() // 2 - 40)
    
def restart():
    global start_time, current_button
    show_input_fields()
    current_button = 0
    start_time = 0
    for button in buttons:
        button.config(bg="blue")

def handle_button_click(button_index):
    global current_button
    if button_index == BUTTON_ORDER[current_button]:
        buttons[button_index].config(bg="green")  # Set button color to green for correct order
        current_button += 1
        if current_button == len(BUTTON_ORDER):
            # All buttons clicked in the correct order
            elapsed_time = time.time() - start_time
            print("Congratulations! You clicked all buttons in the right order.")
            print("Elapsed Time: {:.2f} seconds".format(elapsed_time))
            save_results(username_entry.get(), mode_combobox.get(), elapsed_time)
            restart()
            # Perform any additional actions or logic here when all buttons are clicked correctly
    else:
        buttons[button_index].config(bg="red")  # Set button color to red for wrong order
        # Perform any actions or logic here for a wrong button click

def handle_start_button_click():
    global start_time
    start_button.place_forget()
    start_time = time.time()
    show_buttons()

root = tk.Tk()
width= root.winfo_screenwidth()               
height= root.winfo_screenheight()
root.geometry("%dx%d" % (width, height))


username_label = tk.Label(root, text="Username:", font=("Arial", 12))
mode_label = tk.Label(root, text="Mode:", font=("Arial", 12))
username_entry_label = tk.Label(root, text="Username:", font=("Arial", 12))
mode_combobox_label = tk.Label(root, text="Mode:", font=("Arial", 12))

username_entry = tk.Entry(root, font=("Arial", 12))
username_entry.insert(0, "test") 
mode_values = [str(i) for i in range(1, 7)]
mode_combobox = ttk.Combobox(root, values=mode_values, font=("Arial", 12))
mode_combobox.current(0)
ok_button = tk.Button(root, text="OK", command=show_start_button)
ok_button.config(width=4, height=1, bg="grey", fg="white", font=("Arial", 12, "bold"))
start_button = tk.Button(root, text="Press here to start", font=("Arial", 18, "bold"), fg="white", bg="red", command=handle_start_button_click)


buttons = []
button1 = tk.Button(root, text="1", command=lambda: handle_button_click(0))
button1.config(width=5, height=5, bg="blue", fg="white", font=("Arial", 18, "bold"))
buttons.append(button1)

button2 = tk.Button(root, text="2", command=lambda: handle_button_click(1))
button2.config(width=20, height=5, bg="blue", fg="white", font=("Arial", 18, "bold"))
buttons.append(button2)

button3 = tk.Button(root, text="3", command=lambda: handle_button_click(2))
button3.config(width=3, height=2, bg="blue", fg="white", font=("Arial", 18, "bold"))
buttons.append(button3)

button4 = tk.Button(root, text="4", command=lambda: handle_button_click(3))
button4.config(width=15, height=1, bg="blue", fg="white", font=("Arial", 18, "bold"))
buttons.append(button4)

button5 = tk.Button(root, text="5", command=lambda: handle_button_click(4))
button5.config(width=1, height=8, bg="blue", fg="white", font=("Arial", 18, "bold"))
buttons.append(button5)

show_input_fields()

root.mainloop()