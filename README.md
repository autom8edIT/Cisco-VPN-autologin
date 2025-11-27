[![Build EXE with Secrets](https://github.com/autom8edIT/Cisco-VPN-autologin/actions/workflows/pwsh-build-exe.yml/badge.svg)](https://github.com/autom8edIT/Cisco-VPN-autologin/actions/workflows/pwsh-build-exe.yml)

# autom8ed VPN Auto-Login

**"One script to log them all. One script to bind them."**

Welcome to **autom8ed Cisco "Secure" VPN Auto-Login**, the way it should be, fully autom8ed!

Who hasn't been tired of logging in manually forever? Like it's 2007? This is your fully autom8ed, keypress-simulating, token-smuggling, rage-fueled revenge on corporate UX.

---

## ⚙️ What This Monster Does

- 🕵️ **Watches for Cisco Secure Client's spawn process** (`acwebhelper.exe`)
- 🔐 **Injects your username + password** with surgical precision
- 🔢 **Handles TOTP/2FA** instantly using your secret
- 🤖 **Clicks the right button, at the right time, every time**
- 🧠 **Runs silently**, no popups, no prompts, no mercy

> Because you're not here to click. You're here to connect.

---

If you use <a href="url">Google Authenticator</a> you can use this super sick tool to get ahold of your secret key for any account.
Mad props, tried to make the same tool myself then found this gem by accident and realized there's no point in inventing the wheel again!
**https://github.com/krissrex/google-authenticator-exporter**

## 🚀 Quick Setup

### 1. Clone the Repo
```bash
git clone git@github.com:autom8edIT/Cisco-VPN-autologin.git
cd csc-autologin
```

### 2. Install Requirements
```bash
pip install -r requirements.txt
# Optionally used togehter with a local Flask server instead of fetching creds from a file on the disk.
```

### 3. Create a `.env` File
In the root folder, add your creds/secrets:
```env
VPN_USERNAME=your_username
VPN_PASSWORD=your_password
TOTP_SECRET=your_base32_totp_secret
TOTP_SCRIPT_PATH=C:\Tools\autom8ed\Bin\totp.py
LOG_PATH=C:\Tools\autom8ed\Logs\vpn_auto_login.log
```
> 🔐 **Pro Tip**: `.env` is in `.gitignore` — your secrets are safe.

---

## 🧠 How It Works

Every action, every click, perfectly timed. No lag. No fail.

---

## 🌪️ Why it's autom8ed? Because life is way too short to spend on repeating meaningless tasks over and over.

- Built by **The Machine** — a force of nature in IT and overclocking.
- Designed to make *daily annoyances vanish* while flexing Python, pywinauto, and automation skills.
- This is part of a **larger autom8edIT Tools ecosystem**, evolving into a full-blown fix anything and everything for Windows.
- Pure violence against UX friction.

---

## 🧰 Requirements
- Python 3.10+
- Modules:
  - `pywinauto`
  - `python-dotenv`
  - `pyotp` (or equivalent, depending on your TOTP method)

---

## 🖥️ Screenshot
```
[👻] Waiting for acwebhelper.exe...
[🔐] Injected username and password.
[🔢] Injected TOTP code: 249017
[✅] Login complete. VPN connection established.
```

---

## 📛 Disclaimer
This tool is for legit use only — don't use it to bypass corporate security unless you *are* the corporate security. Automate responsibly. Or not. I'm not your dad.

---

## 🧠 Author
**The Machine / autom8edIT**  
GitHub: [@autom8edIT](https://github.com/autom8edIT)  
"I didn't choose to be bypassing every roadblock. THey got setup to challenge me."

---

## 🧪 Future Plans
- GUI launcher version
- Logging dashboard with stats
- Self-update system
- Full integration into autom8ed services.
- Further evolve the browser extension so it can identify any TOTP website and automatically inject the MFA code. Plus make it possible to tweak the UI to your preference.
---

## 🔥 autom8ed Motto
Don't just use tools, especially any default configs, master the tool and let it just be an extension of you!
> Microsoft nor Cisco authorized this. So I did, because not having it made my work way less efficient and made me go insane from enterng my creds nonstop.

**Welcome to the end of manual login.**
