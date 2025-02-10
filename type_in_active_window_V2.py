from threading import Lock
from pynput import keyboard, mouse
from pynput.keyboard import Controller  # Correct import for Controller
from utils import *
from typing_fixer import register_key, reset_keys
import subprocess
import time
from AppKit import NSWorkspace

prev_active_window = None
prev_active_window_lock = Lock()
config = load_json(CONFIG_JSON_PATH)
keyboard_controller = Controller()

# Functions:
def change_keyboard_language(language_config: dict, active_window_title: str):
    """
    Change the keyboard layout to the wanted layout.

    :param language_config: The language config dict.
    :param active_window_title: string of the active window title.
    :return: None
    """
    # Get the wanted layout:
    wanted_layout = language_config.get(active_window_title)

    # Check the current keyboard layout:
    current_layout = get_current_layout()

    # If the wanted layout is not the current layout, change it:
    if wanted_layout and (wanted_layout != current_layout):
        print(f'active_window changed to: {active_window_title} -> Changing keyboard layout to: "{wanted_layout}"...')
        subprocess.call(CHANGE_LANGUAGE_SCRIPT, shell=True)
    else:
        print(f'active_window changed to: {active_window_title} -> Keyboard layout is already correct.')

def window_change(x, y, button, pressed):
    """
    Change the keyboard layout when the active window changes, also reset the keys_pressed list.

    :return: None
    """
    global prev_active_window, prev_active_window_lock, config
    active_window = run_script(GET_ACTIVE_WINDOW_SCRIPT)
    if (not prev_active_window) or (active_window != prev_active_window):
        change_keyboard_language(config, active_window)
        with prev_active_window_lock:
            prev_active_window = active_window

    reset_keys(x, y, button, pressed)

def type_text(text: str):
    """
    Type the given text in the active window.

    :param text: The text to type.
    :return: None
    """
    # Get the currently active app's bundle identifier
    active_app = NSWorkspace.sharedWorkspace().activeApplication()["NSApplicationBundleIdentifier"]
    
    # Focus on the active window
    subprocess.call(["open", "-a", active_app])
    time.sleep(0.5)  # Adjust this sleep time if necessary

    # Prompt user to focus on the active window
    print("Please bring the active window to the front and focus on it...")

    # Wait for the user to focus on the active window
    time.sleep(2)

    for char in text:
        keyboard_controller.type(char)

# Main:
if __name__ == '__main__':
    start_message()
    with keyboard.Listener(on_press=register_key) as k_listener:
        with mouse.Listener(on_click=window_change) as m_listener:
            type_text("Hello, this is a test text.")
            k_listener.join()
            m_listener.join()
