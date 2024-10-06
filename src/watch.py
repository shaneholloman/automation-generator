"""
This module records mouse clicks and keyboard presses, logging them to a CSV file.
It uses pynput to listen for input events and csv to write the log.
"""

import csv
import time
from pynput.keyboard import Listener as KeyboardListener
from pynput.mouse import Listener as MouseListener


class InputLogger:
    """
    A class to log mouse and keyboard inputs to a CSV file.
    """

    def __init__(self, log_file):
        """
        Initialize the InputLogger.

        Args:
        log_file (str): Path to the log file
        """
        self.log_file = log_file
        self.exit_program = False
        self.last_action_time = None

    def log_mouse_click(self, x, y, button, pressed):
        """
        Log mouse click events to the CSV file.

        Args:
        x (int): X-coordinate of the mouse click
        y (int): Y-coordinate of the mouse click
        button (pynput.mouse.Button): The mouse button that was clicked
        pressed (bool): True if the button was pressed, False if released

        Returns:
        bool: False if the program should exit, True otherwise
        """
        if self.exit_program:
            return False
        action_time = time.time()
        duration = action_time - self.last_action_time if self.last_action_time else 0
        self.last_action_time = action_time
        if pressed:
            with open(self.log_file, mode="a", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow([True, button, (x, y), None, duration])
        return True

    def log_key_press(self, key):
        """
        Log key press events to the CSV file.

        Args:
        key (pynput.keyboard.Key): The key that was pressed

        Returns:
        bool: False if the program should exit, True otherwise
        """
        action_time = time.time()
        duration = action_time - self.last_action_time if self.last_action_time else 0
        self.last_action_time = action_time
        with open(self.log_file, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            pressed_key = ""
            try:
                pressed_key = key.char
            except AttributeError:
                if key == key.esc:
                    self.exit_program = True
                    return False
                pressed_key = key
            writer.writerow([False, None, None, pressed_key, duration])
        return True

    def start(self):
        """
        Start the input listeners.
        """
        with MouseListener(
            on_click=self.log_mouse_click
        ) as mouse_listener, KeyboardListener(
            on_press=self.log_key_press
        ) as keyboard_listener:
            mouse_listener.join()
            keyboard_listener.join()


def main():
    """
    Main function to set up and start the input logger.
    """
    logger = InputLogger("src/logs/input_log.csv")
    logger.start()


if __name__ == "__main__":
    main()
