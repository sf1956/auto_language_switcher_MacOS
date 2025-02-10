import pynput.keyboard
import bidi.algorithm  # For Bi-Directional Text
import json  # Import the json library


#current_text = ""

def load_conversion_map(filename="conversion_map.json"):  # Function to load the map
    try:
        with open(filename, "r", encoding="utf-8") as f: # added encoding
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: {filename} not found. Using default map.")
        return {  # Default map (if file not found)
            'q': 'ק', 'w': 'ו', 'e': 'ה', 'r': 'ר', 't': 'ט', 'y': 'י', 'u': 'ו', 'i': 'י', 'o': 'ם', 'p': 'פ',
            'a': 'א', 's': 'ס', 'd': 'ד', 'f': 'ף', 'g': 'ג', 'h': 'ח', 'j': 'ג', 'k': 'כ', 'l': 'ל', ';': 'ך',
            'z': 'ז', 'x': 'ץ', 'c': 'צ', 'v': 'ב', 'b': 'נ', 'n': 'מ', 'm': 'נ', ',': 'ץ', '.': 'ת', '/': '?',
            'Q': 'ק', 'W': 'ו', 'E': 'ה', 'R': 'ר', 'T': 'ט', 'Y': 'י', 'U': 'ו', 'I': 'י', 'O': 'ם', 'P': 'פ',
            'A': 'א', 'S': 'ס', 'D': 'ד', 'F': 'ף', 'G': 'ג', 'H': 'ח', 'J': 'ג', 'K': 'כ', 'L': 'ל', ':': 'ך',
            'Z': 'ז', 'X': 'ץ', 'C': 'צ', 'V': 'ב', 'B': 'נ', 'N': 'מ', 'M': 'נ', '<': 'ץ', '>': 'ת', '?': '?',
            ' ': ' ',  # Keep space as is
            # Add more mappings as needed (numbers, punctuation)
            '1': '1', '2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7', '8': '8', '9': '9', '0': '0',
            '!': '!', '@': '@', '#': '#', '$': '$', '%': '%', '^': '^', '&': '&', '*': '*', '(': '(', ')': ')',
            '-': '-', '_': '_', '=': '=', '+': '+', '[': '[', ']': ']', '{': '{', '}': '}', '\\': '\\', '|': '|',
            ';': ';', ':': ':', '"': '"', "'": "'", '<': '<', '>': '>', ',': ',', '.': '.', '/': '/', '?': '?',
            '`': '`', '~': '~'
        }

conversion_map = load_conversion_map() # Load the map

current_text = ""

def on_press(key):
    global current_text
    try:
        char = key.char
        current_text += char
    except AttributeError:
        if key == pynput.keyboard.Key.space:
            current_text += " "
        elif key == pynput.keyboard.Key.backspace:
            current_text = current_text[:-1]
        elif key == pynput.keyboard.Key.enter:
            print("Original (English):", current_text)
            current_text = ""
        elif key == pynput.keyboard.Key.f10:  # F10 key pressed
            converted_text = convert_to_hebrew(current_text)
            bidi_text = bidi.algorithm.get_display(converted_text)
            print("\nConverted (Hebrew): " + bidi_text)
            #print("Converted (Hebrew):", bidi_text)
            current_text = ""

def on_release(key):
    if key == pynput.keyboard.Key.esc:
        return False

def convert_to_hebrew(text):
    converted_text = ""
    for char in text:
        if char in conversion_map:
            converted_text += conversion_map[char]
        else:
            converted_text += char  # Keep character if no mapping exists
    return converted_text

with pynput.keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    print("Listening for keyboard input. Press F10 to convert, Enter to print, Esc to exit.")
    listener.join()

    