import pynput.keyboard
import langdetect
from langdetect import detect_langs
import bidi.algorithm
import subprocess  # Use subprocess for platform compatibility
import sys

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
            detect_and_print_language(current_text)
            current_text = ""

def on_release(key):
    if key == pynput.keyboard.Key.esc:
        return False

def detect_and_print_language(text):
    if not text.strip():
        print("No text entered.")
        return

    try:
        # 1. Language Detection (with retries)
        detected_language = None
        for _ in range(3):  # Try 3 times (adjust as needed)
            detected_languages = detect_langs(text)
            if detected_languages:
                best_match = detected_languages[0]
                if best_match.lang in ('he', 'en'): # Prioritize he and en
                    detected_language = best_match
                    break

        # 2. BiDi Processing and Output (Platform-Independent)
        if detected_language and detected_language.lang in ('he', 'ar', 'yi', 'fa', 'ur'):
            bidi_text = bidi.algorithm.get_display(text)
            try:
                # Use subprocess for platform compatibility
                process = subprocess.Popen(['echo', '-n', bidi_text], stdout=subprocess.PIPE)
                output, _ = process.communicate()
                sys.stdout.buffer.write(output) # write bytes to stdout
                print() # new line after printing the RTL text

            except Exception as e:
                print(f"Error displaying RTL text: {e}")
                print("Input (RTL):", bidi_text)  # Fallback if subprocess fails

        else:
            print("Input (LTR/Unknown):", text)

        # 3. Output Language
        if detected_language:
            print(f"Detected Language: {detected_language.lang} (Confidence: {detected_language.prob:.2f})")
        else:
            print("Could not reliably determine the language.")

    except langdetect.lang_detect_exception.LangDetectException as e:
        print(f"Language detection failed: {e}")
        print("Could not reliably determine the language. Perhaps the text is too short or contains mixed languages.")

with pynput.keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    print("Listening for keyboard input. Press Esc to exit.")
    listener.join()
    