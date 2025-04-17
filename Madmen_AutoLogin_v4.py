# ================================
# Madmen AutoLogin v4
# ENV-Driven. UI-Sniping. TOTP-Cracking.
# https://github.com/ArcticOverclockers/madmen-tools
# ================================

from pywinauto.application import Application
from pywinauto.keyboard import send_keys
from pywinauto import timings
from madmen_env_loader import load_env_config

config = load_env_config()

USERNAME = config["VPN_USERNAME"]
PASSWORD = config["VPN_PASSWORD"]
TOTP_SCRIPT = config["TOTP_SCRIPT_PATH"]  # Optional: use this below too

print(f"🔐 Username loaded: {USERNAME}")

# Now go dominate the Cisco UI using these creds...

import subprocess
import time

print("🧭 Waiting for Cisco Secure Client - Login window...")

timings.after_clickinput_wait = 1
found = False

# --- Wait for Login Window ---
for _ in range(30):
    try:
        app = Application(backend="uia").connect(title="Cisco Secure Client - Login", timeout=1)
        dlg = app.window(title="Cisco Secure Client - Login")
        dlg.set_focus()
        print("✅ Login window detected.")
        found = True
        break
    except:
        time.sleep(1)

if not found:
    print("❌ Login window not found within timeout.")
    exit(1)

# --- Inject Username/Password ---
try:
    dlg.child_window(control_type="Edit", found_index=0).set_text(USERNAME)
    dlg.child_window(control_type="Edit", found_index=1).set_text(PASSWORD)

    login_btn = dlg.child_window(title_re="Log in\\s*", control_type="Button")
    if login_btn.exists(timeout=3):
        print("🧪 Found login button... trying click_input()")
        try:
            login_btn.click_input()
        except:
            print("⚠️ click_input failed. Trying invoke...")
            login_btn.wrapper_object().invoke()

        time.sleep(1)
        dlg.type_keys("{ENTER}")
        print("🚀 Login submitted.")
    else:
        print("❌ Login button not found.")
        exit(1)

except Exception as e:
    print(f"⚠️ Could not interact with login form: {e}")
    exit(1)

# --- Wait for TOTP window ---
print("[*] Waiting for TOTP window...")
while True:
    try:
        if dlg.child_window(title="Enter token Code (6 digits)", control_type="Text").exists(timeout=0.5):
            print("[+] Confirmed TOTP window by label. Injecting now...")
            break
    except:
        pass
    time.sleep(0.5)

# --- Generate TOTP ---
try:
    totp_code = subprocess.check_output(['python', TOTP_SCRIPT]).decode().strip()
    print(f"[+] TOTP generated: {totp_code}")
except Exception as e:
    print(f"[!] Failed to generate TOTP: {e}")
    exit(1)

# --- Inject into TOTP field ---
try:
    edit = dlg.child_window(auto_id="tokencode", control_type="Edit")
    rect = edit.rectangle()
    center_x = int((rect.left + rect.right) / 2)
    center_y = int((rect.top + rect.bottom) / 2)

    edit.set_focus()
    time.sleep(0.2)
    edit.click_input(coords=(center_x, center_y))
    time.sleep(0.4)
    edit.type_keys(totp_code, with_spaces=False, set_foreground=True)
    time.sleep(0.3)

    login_button = dlg.child_window(title="Log in", control_type="Button")
    login_button.click_input()

    print("🎯 TOTP injected and submitted.")

except Exception as e:
    print(f"[!] TOTP injection failed: {e}")
    exit(1)
