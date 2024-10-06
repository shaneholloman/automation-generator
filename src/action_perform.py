"""
This module performs actions based on logged input from a CSV file.
It simulates mouse clicks and key presses using pyautogui.
"""

import ast
import csv
import time

import pyautogui

with open("src/logs/input_log.csv", mode="r", encoding="utf-8") as file:
    reader = csv.reader(file)
    for row in reader:
        is_mouse_click, MOUSE_BUTTON, mouse_coord, key_pressed, time_passed = row
        time.sleep(float(time_passed))
        if is_mouse_click == "True":
            x, y = ast.literal_eval(mouse_coord)
            MOUSE_BUTTON = str.replace(MOUSE_BUTTON, "Button.", "")
            if MOUSE_BUTTON == "left":
                pyautogui.click(x, y)
            else:
                pyautogui.rightClick()
        else:
            pyautogui.press(str.replace(key_pressed, "Key.", ""))
