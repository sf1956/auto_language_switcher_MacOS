import enchant
from pynput import keyboard

def is_english_word(word):
    """Checks if a word is in the English dictionary."""
    try:
        d = enchant.Dict("en_US")
        return d.check(word)
    except enchant.errors.NoDictionariesFound:
        print("No English dictionaries found. Please install an Enchant dictionary (e.g., 'en_US').")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

current_word = ""

def on_press(key):
    global current_word
    if key == keyboard.Key.esc:
        return False

    try:
        if key.char.isalnum():
            current_word += key.char
        elif key == keyboard.Key.space or (hasattr(key, 'char') and not key.char.isalnum()):  # Check on space or other key
            word_to_check = current_word
            current_word = ""  # Reset for the next word
            if word_to_check: # Check if the word is not empty
                if not is_english_word(word_to_check):
                    print(f"'{word_to_check}' is not an English word. Exiting.")
                    return False
                else:
                    print(f"'{word_to_check}' is an English word.")
        elif key == keyboard.Key.backspace:
            current_word = current_word[:-1] # Remove last character

    except AttributeError:  # Special key pressed
        if key == keyboard.Key.backspace:
            current_word = current_word[:-1] # Remove last character
        elif (not hasattr(key, 'char')):  # Other keys
            word_to_check = current_word
            current_word = ""
            if word_to_check:
                if is_english_word(word_to_check):
                    print(f"'{word_to_check}' is an English word.")
                else:
                    print(f"'{word_to_check}' is not an English word. Exiting.")
                    #return False


with keyboard.Listener(on_press=on_press) as listener:
    print("Start typing. Words will be checked when completed. Press ESC to exit.")
    listener.join()

print("Program exited.")
