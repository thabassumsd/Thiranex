import re
import math
import random
import string
import sqlite3

# -----------------------------
# Configuration
# -----------------------------
SPECIAL_CHARS = "!@#$%^&*()-_=+[]{}|;:,.<>?/"
COMMON_PASSWORDS = {
    "password", "123456", "12345678", "qwerty",
    "admin", "welcome", "letmein", "password123"
}

DB_NAME = "password_history.db"


# -----------------------------
# Database Setup
# -----------------------------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS password_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            password_hash TEXT
        )
    """)
    conn.commit()
    conn.close()


def save_password(password):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("INSERT INTO password_history (password_hash) VALUES (?)", (password,))
    conn.commit()
    conn.close()


def is_reused(password):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT password_hash FROM password_history WHERE password_hash = ?", (password,))
    result = cur.fetchone()
    conn.close()
    return result is not None


# -----------------------------
# Password Analysis
# -----------------------------
def analyze_password(password):
    score = 0
    feedback = []

    length = len(password)

    # Length check
    if length >= 16:
        score += 3
    elif length >= 12:
        score += 2
    elif length >= 8:
        score += 1
    else:
        feedback.append("Use at least 8 characters.")

    # Complexity checks
    if re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("Add lowercase letters.")

    if re.search(r"[A-Z]", password):
        score += 1
    else:
        feedback.append("Add uppercase letters.")

    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("Add numbers.")

    if re.search(f"[{re.escape(SPECIAL_CHARS)}]", password):
        score += 1
    else:
        feedback.append("Add special characters.")

    # Common password check
    if password.lower() in COMMON_PASSWORDS:
        score -= 3
        feedback.append("This is a commonly used weak password.")

    # Entropy calculation
    charset = 0
    if re.search(r"[a-z]", password):
        charset += 26
    if re.search(r"[A-Z]", password):
        charset += 26
    if re.search(r"\d", password):
        charset += 10
    if re.search(f"[{re.escape(SPECIAL_CHARS)}]", password):
        charset += len(SPECIAL_CHARS)

    entropy = length * math.log2(charset) if charset else 0

    # Strength classification
    if score <= 2:
        strength = "WEAK"
    elif score <= 5:
        strength = "MODERATE"
    elif score <= 7:
        strength = "STRONG"
    else:
        strength = "VERY STRONG"

    return strength, score, entropy, feedback


# -----------------------------
# Password Generator
# -----------------------------
def generate_strong_password(length=16):
    chars = string.ascii_letters + string.digits + SPECIAL_CHARS
    return ''.join(random.choice(chars) for _ in range(length))


# -----------------------------
# Main Program
# -----------------------------
def main():
    init_db()

    print("\n=== PASSWORD STRENGTH ANALYZER ===\n")

    password = input("Enter password: ")

    # Check reuse
    if is_reused(password):
        print("\n⚠ WARNING: This password was used before. Choose a new one.\n")

    strength, score, entropy, feedback = analyze_password(password)

    print("\n------ RESULT ------")
    print("Strength:", strength)
    print("Score   :", score)
    print(f"Entropy : {entropy:.2f} bits")

    print("\n------ FEEDBACK ------")
    if feedback:
        for f in feedback:
            print("-", f)
    else:
        print("Your password is strong.")

    print("\n------ SUGGESTED PASSWORD ------")
    print(generate_strong_password())

    # Save password to history
    save_password(password)


if __name__ == "__main__":
    main()