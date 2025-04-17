import pyotp
totp = pyotp.TOTP("YOURSECRETTOTPKEY")
print(totp.now())  # Will match your phone!
