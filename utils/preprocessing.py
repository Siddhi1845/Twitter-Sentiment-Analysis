import re
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

stop_words = ENGLISH_STOP_WORDS

def clean_text(text):
    text = str(text).lower()

    # Remove URLs
    text = re.sub(r"http\S+", "", text)

    # Remove mentions
    text = re.sub(r"@\w+", "", text)

    # Remove hashtags (keep the word)
    text = re.sub(r"#", "", text)

    # Keep only letters and spaces
    text = re.sub(r"[^a-z\s]", "", text)

    words = [
        word
        for word in text.split()
        if word not in stop_words
    ]

    return " ".join(words)