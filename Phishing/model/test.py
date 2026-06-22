import sys
import os

# Add the parent directory (Phishing) to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.preprocess import preprocess_text
from src.feature_extraction import extract_url_features, keyword_count

email = """
Congratulations!

Click here

https://paypal-security-login.com

Verify your account immediately.
"""

clean = preprocess_text(email)

print("Processed Text:")
print(clean)

print("\nURL Features:")
print(extract_url_features(email))

print("\nKeyword Count:")
print(keyword_count(email))