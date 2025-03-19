import threading
import time
import pyautogui
import pyperclip
import platform
import random
import requests
from PIL import Image
from io import BytesIO
from pynput import keyboard, mouse
from modules.activeWindow import ActiveWindowManager
from modules.aiResponder import AIResponder


class TypingAssistant:
    def __init__(self, trigger_words=None):
        if trigger_words is None:
            trigger_words = {"varcharai:", "aitext:", "aicode:","aiimage:"}
        self.trigger_words = set(trigger_words)
        self.buffer = ""
        self.target_window = None
        self.running = True
        self.window_manager = ActiveWindowManager()  
        self.ai_responder = AIResponder()  
        self.greetings = [
                            "Hello! How can I assist you today?",
                            "Hey there! Ready to type?",
                            "Hi! What's on your mind?",
                            "Greetings! Need any help?",
                            "Hello! Let's get started.",
                            "Hey! What can I do for you today?",
                            "Hi there! How's it going?",
                            
                            # Funny Greetings
                            "Beep boop! AI at your service 🤖",
                            "Hey! I was just taking a nap. What's up? 😴",
                            "Hello, human! I promise I won't take over the world... yet. 😈",
                            "You type, I assist. That's the deal, right? 😜",
                            "Hi! I'm 90% caffeine and 10% AI. What's up? ☕",
                            "Yo! If you type 'pizza', I might just order one for myself. 🍕",
                            "Hello! I'd tell you a joke, but I'm afraid it'll be too artificial. 😆",
                            "Ah, another day, another keyboard to conquer! ⌨️🔥"
                        ]

    def monitor_keystrokes(self):
        def on_press(key):
            try:
                if hasattr(key, 'char') and key.char is not None:
                    self.buffer += key.char
                elif key == keyboard.Key.space:
                    self.buffer += " "
                elif key == keyboard.Key.backspace:
                    self.buffer = self.buffer[:-1]

                for trigger in self.trigger_words:
                    if self.buffer.endswith(trigger):
                        print(f"Trigger word detected: {trigger}")
                        self.buffer = ""
                        self.target_window = self.window_manager.get_active_window()
                        print(f"Locked to target window: {self.target_window}")

                        command = self.wait_for_command(trigger)
                        if command:
                            if trigger == "aiimage:":
                                response = self.ai_responder.image_command(command)
                                self.write_to_target_window(response, trigger)
                            elif trigger == "varcharai:":
                                response = random.choice(self.greetings) 
                                self.write_to_target_window(response, trigger)
                            else:
                                response = self.ai_responder.process_command(command)
                                self.write_to_target_window(response, trigger)
                        break  # Prevent multiple triggers from firing at once
            except Exception as e:
                print(f"Error processing key: {e}")

        with keyboard.Listener(on_press=on_press) as listener:
            listener.join()

    def wait_for_command(self, trigger):
        command = ""
        print("Waiting for user command (type and press Enter)...")

        def on_press(key):
            nonlocal command
            try:
                if hasattr(key, 'char') and key.char is not None:
                    command += key.char
                elif key == keyboard.Key.space:
                    command += " "
                elif key == keyboard.Key.backspace:
                    command = command[:-1]
                elif key == keyboard.Key.enter:
                    return False  # Stops the listener
            except Exception as e:
                print(f"Error processing command input: {e}")

        with keyboard.Listener(on_press=on_press) as listener:
            listener.join()

        if trigger == "aicode:":
            command = f"{command} without explanation, language name and ```"
        else:
            command = f"{command} without any formatting" 
        
        print(f"Command received: {command}")
        return command

    def write_to_target_window(self, text, trigger):
        try:
            current_window = self.window_manager.get_active_window()
            if current_window == self.target_window:
                if trigger == "aitext:" or trigger == "varcharai:":
                    pyautogui.typewrite(text, interval=0.06)
                elif trigger == "aicode:":
                    pyperclip.copy(text)
                    pyautogui.hotkey('command' if platform.system() == "Darwin" else 'ctrl', 'v', interval=0.2)
                elif trigger == "aiimage:":
                    # Get the image URL
                    image_url = text
                    # Download the image
                    image_response = requests.get(image_url)
                    # Open the image
                    image = Image.open(BytesIO(image_response.content))
                    # Display the image
                    image.show()
            else:
                if self.ask_to_change_focus(current_window):
                    self.target_window = current_window
                    self.write_to_target_window(text, trigger)
        except Exception as e:
            print(f"Error writing to target window: {e}")

    def ask_to_change_focus(self, new_window):
        try:
            print(f"Focus switched to a new window: {new_window}")
            response = input("Would you like to change the target window to this one? (yes/no): ").strip().lower()
            return response in {"yes", "y"}
        except Exception as e:
            print(f"Error prompting for focus change: {e}")
            return False

    def monitor_mouse(self):
        def on_click(x, y, button, pressed):
            if pressed:
                new_window = self.window_manager.get_active_window()
                if new_window != self.target_window:
                    print(f"Focus changed to: {new_window}")
                    self.target_window = new_window

        with mouse.Listener(on_click=on_click) as listener:
            listener.join()

    def start_listeners(self):
        self.target_window = self.window_manager.get_active_window()
        threading.Thread(target=self.monitor_keystrokes, daemon=True).start()
        threading.Thread(target=self.monitor_mouse, daemon=True).start()

        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nExiting program...")
            self.running = False
            pyperclip.copy("")
