import enchant
from pynput import keyboard
import math

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

def english_word_probability(word):
    """Calculates a better probability of a word being English."""

    if not word:
        return 0.0

    try:
        d = enchant.Dict("en_US")

        if is_english_word(word):
            return 1.0

        suggestions = d.suggest(word)

        if not suggestions:
            return 0.0

        # Improved Heuristic:
        # 1. Check if the word is a prefix of ANY word in the dictionary.
        # 2. If not a prefix, use a weighted score based on suggestion length and count.

        # Correct Prefix Check:
        for i in range(len(word), 0 , -1):
            if d.check(word[:i]):
                return 0.9

        # If not a prefix, use a score based on suggestion length and count
        score = 0
        for suggestion in suggestions:
            score += math.exp(-abs(len(word)-len(suggestion))) # Weight based on length difference.

        probability =  score / len(suggestions) if suggestions else 0.0
        return min(1.0, probability)

    except enchant.errors.NoDictionariesFound:
        print("No English dictionaries found. Please install an Enchant dictionary (e.g., 'en_US').")
        return 0.0
    except Exception as e:
        print(f"An error occurred: {e}")
        return 0.0


current_word = ""
PROBABILITY_THRESHOLD = 0.5  # P% = 50% (adjust as needed)

def on_press(key):
    global current_word
    if key == keyboard.Key.esc:
        return False

    try:
        if key.char.isalnum():
            current_word += key.char
            probability = english_word_probability(current_word)
            if probability < PROBABILITY_THRESHOLD:
                print(f"'{current_word}': Probability is below {PROBABILITY_THRESHOLD*100:.0f}%.") # Print only if below threshold

        elif key == keyboard.Key.space or (hasattr(key, 'char') and not key.char.isalnum()):  # Check on space or other key
            word_to_check = current_word
            current_word = ""  # Reset for the next word
            if word_to_check:
                if is_english_word(word_to_check):
                    print(f"'{word_to_check}' is an English word.")
                else:
                    print(f"'{word_to_check}' is not an English word.")
        elif key == keyboard.Key.backspace:
            current_word = current_word[:-1]
            probability = english_word_probability(current_word)
            if current_word and probability < PROBABILITY_THRESHOLD: #Check if current_word is not empty
                print(f"'{current_word}': Probability is below {PROBABILITY_THRESHOLD*100:.0f}%.")  # Print only if below threshold
        elif (hasattr(key, 'char') and not key.char.isalnum()): # Other keys
            word_to_check = current_word
            current_word = ""
            if word_to_check:
                if is_english_word(word_to_check):
                    print(f"'{word_to_check}' is an English word.")
                else:
                    print(f"'{word_to_check}' is not an English word.")
    except AttributeError:  # Special key pressed
        if key == keyboard.Key.backspace:
            current_word = current_word[:-1]
            probability = english_word_probability(current_word)
            if current_word and probability < PROBABILITY_THRESHOLD: #Check if current_word is not empty
                print(f"'{current_word}': Probability is below {PROBABILITY_THRESHOLD*100:.0f}%.")  # Print only if below threshold
        elif (not hasattr(key, 'char')):  # Other keys
            word_to_check = current_word
            current_word = ""
            if word_to_check:
                if is_english_word(word_to_check):
                    print(f"'{word_to_check}' is an English word.")
                else:
                    print(f"'{word_to_check}' is not an English word.")



with keyboard.Listener(on_press=on_press) as listener:
    print(f"Start typing. A message will appear if the probability of the current word being English is below {PROBABILITY_THRESHOLD*100:.0f}%. Press ESC to exit.")
    listener.join()

print("Program exited.")

