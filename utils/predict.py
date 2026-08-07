import joblib
import re
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

# Load model and vectorizer
model = joblib.load("models/model.pkl")
vectorizer = joblib.load("models/vectorizer.pkl")

stop_words = ENGLISH_STOP_WORDS


def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"@\w+", "", text)
    text = re.sub(r"#", "", text)
    text = re.sub(r"[^a-z\s]", "", text)

    words = [
        word for word in text.split()
        if word not in stop_words
    ]

    return " ".join(words)


def predict_sentiment(text):
    cleaned = clean_text(text)

    vector = vectorizer.transform([cleaned])

    prediction = model.predict(vector)[0]

    confidence = 0

    if hasattr(model, "predict_proba"):
        confidence = max(model.predict_proba(vector)[0]) * 100

    return prediction.capitalize(), confidence