from pynput import keyboard, mouse
from pynput.keyboard import Controller
import subprocess

class AutoTyper:
    def __init__(self):
        self.keyboard_controller = Controller()
        self.active_window_title = None
        self.input_text = ""

    def get_active_window_title(self):
        """Gets active window title (macOS - improved)."""
        script = '''
        tell application "System Events"
            set frontApp to first application process whose frontmost is true
            set appName to name of frontApp
        end tell
        return appName
        '''
        try:
            process = subprocess.Popen(['osascript', '-e', script], stdout=subprocess.PIPE)
            out, err = process.communicate()
            if err:
                print(f"Error getting active window info: {err}")
                return None

            app_name = out.decode('utf-8').strip()
            return app_name
        except Exception as e:
            print(f"Error getting active window info: {e}")
            return None

    def detect_active_window(self):
        def on_click(x, y, button, pressed):
            if button == mouse.Button.left and pressed:
                self.active_window_title = self.get_active_window_title()
                if self.active_window_title:
                    print(f"Active window detected: {self.active_window_title}")
                    return False  # Stop the listener
                else:
                    print("Could not detect active window.  Try again.")

        with mouse.Listener(on_click=on_click) as listener:
            listener.join()

    def type_text_in_window(self):
        if self.active_window_title:
            print(f"Typing text in the active window: {self.active_window_title}")

            try:
                script = f'tell application "{self.active_window_title}" to activate'
                subprocess.run(['osascript', '-e', script], capture_output=True, text=True, check=True)
            except subprocess.CalledProcessError as e:
                print(f"Error activating window: {e}")
                return

            try:
                for char in self.input_text:
                    self.keyboard_controller.type(char)
            except Exception as e:
                print(f"Error typing: {e}")
        else:
            print("No active window detected.")

    def on_esc_key(self, key):
        if key == keyboard.Key.esc:
            print("Esc key pressed. Exiting program...")
            return False

    def run(self):
        self.input_text = input("Enter the text to type: ")
        print("Click the left mouse button in the target window to begin...")
        self.detect_active_window()

        if self.active_window_title:
            self.type_text_in_window()
            return  # Exit after typing!
        else:
            print("No active window detected.") # Handle the case where the user doesn't click

        with keyboard.Listener(on_press=self.on_esc_key) as esc_listener: # Keep the ESC listener
            esc_listener.join()


if __name__ == '__main__':
    auto_typer = AutoTyper()
    auto_typer.run()
