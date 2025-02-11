from pynput import keyboard

typed_text = []

def on_press(key):
    try:
        # Check if the key is an alphanumeric character or space
        if key.char.isalnum() or key.char == ' ':
            typed_text.append(key.char)
        else:
            typed_text.append(f'<{key.char}>')
    except AttributeError:
        if key == keyboard.Key.space:
            typed_text.append(' ')
        elif key == keyboard.Key.enter:
            typed_text.append('\n')
        elif key == keyboard.Key.backspace and typed_text:
            typed_text.pop()
        else:
            typed_text.append(f'<{key.name}>')

    # Print the captured text
    print(''.join(typed_text))

def on_release(key):
    # Stop listener on Esc key
    if key == keyboard.Key.esc:
        print("Esc key pressed. Exiting program...")
        return False

if __name__ == '__main__':
    print("Listening to keyboard events. Press Esc to stop.")

    # Start the keyboard listener
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
