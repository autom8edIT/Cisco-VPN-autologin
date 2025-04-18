import pyotp
import os

# Fetch the TOTP secret key from environment variables
totp_secret_key = os.getenv("TOTP_SECRET")

if not totp_secret_key:
    raise ValueError("TOTP_SECRET environment variable is not set!")

# Initialize TOTP with the secret key
totp = pyotp.TOTP(totp_secret_key)
print(totp.now())  # Will match your phone!
