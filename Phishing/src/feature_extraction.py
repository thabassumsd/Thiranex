import re

phishing_keywords = [

    "verify",
    "urgent",
    "click",
    "login",
    "password",
    "bank",
    "gift",
    "free",
    "winner",
    "account",
    "update",
    "limited",
    "security",
    "confirm"

]

def extract_url_features(text):

    urls = re.findall(r'https?://\S+|www\.\S+', text)

    url_count = len(urls)

    url_length = sum(len(url) for url in urls)

    https_count = sum(1 for url in urls if url.startswith("https"))

    digits = sum(sum(c.isdigit() for c in url) for url in urls)

    dots = sum(url.count('.') for url in urls)

    return [

        url_count,
        url_length,
        https_count,
        digits,
        dots

    ]

def keyword_count(text):

    text = text.lower()

    count = 0

    for word in phishing_keywords:

        if word in text:
            count += 1

    return count