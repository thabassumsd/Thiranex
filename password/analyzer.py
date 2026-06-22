import re

SPECIAL_CHARS = "!@#$%^&*()-_=+[]{}|;:,.<>?/"

def analyze_password(password):
    score = 0
    feedback = []

    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Use at least 8 characters")

    if re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("Add lowercase letters")

    if re.search(r"[A-Z]", password):
        score += 1
    else:
        feedback.append("Add uppercase letters")

    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("Add numbers")

    if re.search(f"[{re.escape(SPECIAL_CHARS)}]", password):
        score += 1
    else:
        feedback.append("Add special characters")

    if score <= 2:
        strength = "WEAK"
    elif score <= 4:
        strength = "MODERATE"
    else:
        strength = "STRONG"

    return strength, score, feedback