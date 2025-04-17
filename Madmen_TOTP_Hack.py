from pywinauto import Application
from pywinauto.keyboard import send_keys
import subprocess
import time
import shlex

print("[*] Waiting for TOTP window...")

# Wait for the window
while True:
    try:
        app = Application(backend='uia').connect(title='Cisco Secure Client - Login')
        window = app.window(title='Cisco Secure Client - Login')

        if window.child_window(title="Enter token Code (6 digits)", control_type="Text").exists(timeout=0.5):
            print("[+] Confirmed TOTP window by label. Injecting now...")
            break
    except:
        pass
    time.sleep(0.5)

# --- Generate TOTP ---
try:
    TOTP_SCRIPT = config["TOTP_SCRIPT_PATH"]
    totp_cmd = ['python'] + shlex.split(TOTP_SCRIPT)
    totp_code = subprocess.check_output(totp_cmd, stderr=subprocess.STDOUT).decode().strip()
    print(f"[+] TOTP generated: {totp_code}")
except Exception as e:
    print(f"[!] Failed to generate TOTP using script at {TOTP_SCRIPT}: {e}")
    exit(1)



try:
    # Get the edit box
    edit = window.child_window(auto_id="tokencode", control_type="Edit")
    rect = edit.rectangle()
    center_x = int((rect.left + rect.right) / 2)
    center_y = int((rect.top + rect.bottom) / 2)

    # Focus and click
    edit.set_focus()
    time.sleep(0.2)
    edit.click_input(coords=(center_x, center_y))
    time.sleep(0.4)

    # Use type_keys instead of send_keys (works better for embedded inputs like webviews)
    edit.type_keys(totp_code, with_spaces=False, set_foreground=True)
    time.sleep(0.3)

    # Click the login button
    login_button = window.child_window(title="Log in", control_type="Button")
    login_button.click_input()

    print("[+] TOTP injected and submitted.")

except Exception as e:
    print(f"[!] Injection failed: {e}")

