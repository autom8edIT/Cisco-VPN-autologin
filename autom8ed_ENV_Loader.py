# autom8ed_env_loader.py
from dotenv import load_dotenv
import os

def load_env_config():
    load_dotenv()
    config = {
        "VPN_USERNAME": os.getenv("VPN_USERNAME"),
        "VPN_PASSWORD": os.getenv("VPN_PASSWORD"),
        "TOTP_SECRET": os.getenv("TOTP_SECRET"),
        "TOTP_SCRIPT_PATH": os.getenv("TOTP_SCRIPT_PATH"),
        "LOG_PATH": os.getenv("LOG_PATH", "vpn_log.txt")  # Default fallback
    }
    missing = [k for k, v in config.items() if v is None]
    if missing:
        raise EnvironmentError(f"Missing required environment variables: {', '.join(missing)}")
    return config
