from pywinauto.application import Application
from pywinauto import timings
import subprocess
import time
import shlex
from madmen_env_loader import load_env_config  # <-- don't forget this!

config = load_env_config()  # <-- must come before using config

USERNAME = config["VPN_USERNAME"]
PASSWORD = config["VPN_PASSWORD"]

if not USERNAME or not PASSWORD:
    print("❌ Username or password not loaded from config.")
    exit(1)

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
        # ⬇️ ADD DEBUG SCAN HERE
        print("❌ Login button not found. Dumping child elements for analysis:")

        for i, elem in enumerate(dlg.descendants()):
            try:
                ctrl_type = elem.friendly_class_name()
                rect = elem.rectangle()
                title = elem.window_text()
                print(f"[{i}] Type: {ctrl_type}, Title: '{title}', Rect: {rect}")
            except Exception as e:
                print(f"[{i}] ⚠️ Error reading element: {e}")
        exit(1)

except Exception as e:
    print(f"⚠️ Could not interact with login form: {e}")
    exit(1)

# Wait for TOTP window to appear
print("⏳ Waiting for TOTP window...")
found_totp = False
for i in range(30):
    try:
        totp_app = Application(backend="uia").connect(title_re=".*Multi-factor authentication.*", timeout=1)
        totp_dlg = totp_app.top_window()
        totp_dlg.set_focus()
        print("✅ TOTP window detected.")
        found_totp = True
        break
    except Exception:
        time.sleep(1)

if not found_totp:
    print("❌ TOTP window not found.")
    exit(1)

# Call TOTP script and grab code
try:
    TOTP_SCRIPT = config["TOTP_SCRIPT_PATH"]
    totp_cmd = ['python'] + shlex.split(TOTP_SCRIPT)
    result = subprocess.run(totp_cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"❌ TOTP script failed with return code {result.returncode}")
        print(result.stderr)
        exit(1)

    code = result.stdout.strip()
    print(f"🔐 Got TOTP code: {code}")
except Exception as e:
    print(f"❌ Failed to run TOTP script: {e}")
    exit(1)


# Interact with TOTP window
try:
    totp_dlg.child_window(control_type="Edit", found_index=0).set_text(code)

    totp_login_btn = totp_dlg.child_window(title_re="Log in\\s*", control_type="Button")
    if totp_login_btn.exists(timeout=3):
        print("🧪 Found TOTP login button... trying click_input()")
        try:
            totp_login_btn.click_input()
        except:
            print("⚠️ click_input failed. Trying invoke()...")
            totp_login_btn.wrapper_object().invoke()
        time.sleep(1)
        totp_dlg.type_keys("{ENTER}")
        print("🎯 TOTP code submitted.")
    else:
        print("❌ TOTP login button not found.")
        exit(1)
except Exception as e:
    print(f"⚠️ Could not interact with TOTP window: {e}")
    exit(1)
