import enchant
import keyboard

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

def on_press(event):
    global current_word
    if event.name is not None:  # Check if it's a character key
        if event.name.isalnum() or event.name == "space": #Alphanumeric or space
            if event.name == "space":
                word_to_check = current_word
                current_word = ""
                if word_to_check: # Check if the word is not empty
                    if is_english_word(word_to_check):
                        print(f"'{word_to_check}' is an English word.")
                    else:
                        print(f"'{word_to_check}' is not an English word.")
            else:
                current_word += event.name
        elif event.name == "backspace":
            current_word = current_word[:-1] # Remove last character
        else: #Other keys
            word_to_check = current_word
            current_word = ""
            if word_to_check: # Check if the word is not empty
                if is_english_word(word_to_check):
                    print(f"'{word_to_check}' is an English word.")
                else:
                    print(f"'{word_to_check}' is not an English word.")


print("Start typing.  Messages will appear as words are completed.")
keyboard.on_press(on_press)  # Use keyboard.on_press directly
keyboard.wait()  # Keep the script running
