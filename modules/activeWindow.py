import platform
import subprocess

class ActiveWindowManager:
    def __init__(self):
        self.os_name = platform.system()
    
    def get_active_window(self):
        if self.os_name == "Darwin":  # macOS
            return self.get_active_window_mac()
        elif self.os_name == "Windows":
            return self.get_active_window_windows()
        else:
            print("Unsupported OS")
            return None
    
    def get_active_window_mac(self):
        try:
            script = '''
                tell application "System Events"
                    set frontmostApp to name of first application process whose frontmost is true
                end tell
            '''
            result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
            return result.stdout.strip()
        except Exception as e:
            print(f"Error getting active window (macOS): {e}")
            return None
    
    def get_active_window_windows(self):
        try:
            import win32gui
            return win32gui.GetWindowText(win32gui.GetForegroundWindow())
        except Exception as e:
            print(f"Error getting active window (Windows): {e}")
            return None