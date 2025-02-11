from pynput import keyboard

typed_text = []

def on_press(key):
    try:
        if hasattr(key, 'char'):
            char = key.char
            if char.isalnum() or char.isspace():
                typed_text.append(char)
            else:
                typed_text.append(str(key))
        elif key == keyboard.Key.space:
            typed_text.append(' ')
        elif key == keyboard.Key.enter:
            typed_text.append('\n')
        elif key == keyboard.Key.backspace and typed_text:
            typed_text.pop()
        else:
            typed_text.append(str(key))

        # Improved RTL handling for Hebrew:
        current_line = ''.join(typed_text)
        try:
            import arabic_reshaper  # Install: pip install arabic-reshaper
            import bidi.algorithm as bidi

            reshaped_line = arabic_reshaper.reshape(current_line)  # Reshape for proper RTL display
            bidi_text = bidi.get_display(reshaped_line)         # Apply BiDi algorithm
            print('\r' + bidi_text, end='', flush=True)      # Print the correctly ordered text
        except ImportError:
            print('\r' + current_line, end='', flush=True)  # Fallback if libraries are not installed
            print("Please install the `arabic-reshaper` and `bidi` packages for proper RTL support.")


    except AttributeError:
        pass

def on_release(key):
    if key == keyboard.Key.esc:
        print("\nEsc key pressed. Exiting program...")
        return False

if __name__ == '__main__':
    print("Listening to keyboard events. Press Esc to stop.")

    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    print("\nCaptured text:")
    try:
        import arabic_reshaper
        import bidi.algorithm as bidi
        reshaped_full_text = arabic_reshaper.reshape(''.join(typed_text))
        bidi_full_text = bidi.get_display(reshaped_full_text)
        print(bidi_full_text)
    except ImportError:
        print(''.join(typed_text))  # Fallback