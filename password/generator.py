import random
import string

SPECIAL = "!@#$%^&*()-_=+[]{}|;:,.<>?/"

def generate_password(length=12):
    chars = string.ascii_letters + string.digits + SPECIAL
    return "".join(random.choice(chars) for _ in range(length))