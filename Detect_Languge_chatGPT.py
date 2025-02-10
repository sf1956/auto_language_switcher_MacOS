from pynput import keyboard

# Define a function to check if the typed key is from the Hebrew alphabet
def is_hebrew(char):
    # Hebrew characters in the Unicode range for Hebrew
    return '\u0590' <= char <= '\u05FF'

# Define a function to check if the typed key is from the English alphabet
def is_english(char):
    return char.isalpha() and not is_hebrew(char)

# This will store the current detected language
current_language = None

def on_press(key):
    try:
        char = key.char
        if char is not None:  # Only process printable characters
            if is_hebrew(char):
                if current_language != "Hebrew":
                    current_language = "Hebrew"
                    print("Switched to Hebrew")
            elif is_english(char):
                if current_language != "English":
                    current_language = "English"
                    print("Switched to English")
    except AttributeError:
        # Handle special keys (like shift, ctrl, etc.)
        pass

def on_release(key):
    if key == keyboard.Key.esc:
        # Stop listener if ESC is pressed
        return False
"""
# Start listening to the keyboard
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

"""

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    print("Listening for keyboard input. Press Esc to exit.")
    listener.join()
    