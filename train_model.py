import pandas as pd
import joblib
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

from sklearn.model_selection import train_test_split

from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import MultinomialNB

from sklearn.metrics import accuracy_score, classification_report

# --------------------------
# Load Dataset
# --------------------------

df = pd.read_csv("datasets/Tweets.csv")

# Keep only required columns
df = df[["airline_sentiment", "text"]]

# Rename columns
df.columns = ["Sentiment", "Tweet"]

# Keep only Positive, Negative, Neutral
df = df[df["Sentiment"].isin([
    "positive",
    "negative",
    "neutral"
])]

# Remove duplicates
df.drop_duplicates(inplace=True)

# Remove missing values
df.dropna(inplace=True)

print(df.head())
print("\nDataset Shape:", df.shape)

# --------------------------
# Text Cleaning
# --------------------------

stop_words = ENGLISH_STOP_WORDS


def clean_text(text):

    text = text.lower()

    text = re.sub(r"http\S+", "", text)

    text = re.sub(r"@\w+", "", text)

    text = re.sub(r"#", "", text)

    text = re.sub(r"[^a-z\s]", "", text)

    words = []

    for word in text.split():

        if word not in stop_words:

            words.append(word)

    return " ".join(words)


df["Clean_Tweet"] = df["Tweet"].apply(clean_text)

# --------------------------
# TF-IDF
# --------------------------

vectorizer = TfidfVectorizer(max_features=7000)

X = vectorizer.fit_transform(df["Clean_Tweet"])

y = df["Sentiment"]

# --------------------------
# Split Dataset
# --------------------------

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y

)

# --------------------------
# Models
# --------------------------

models = {

    "Logistic Regression": LogisticRegression(max_iter=1000),

    "Linear SVM": LinearSVC(),

    "Naive Bayes": MultinomialNB()

}

best_model = None
best_accuracy = 0

# --------------------------
# Training
# --------------------------

for name, model in models.items():

    model.fit(X_train, y_train)

    pred = model.predict(X_test)

    acc = accuracy_score(y_test, pred)

    print("\n", name)
    print("Accuracy:", round(acc * 100, 2), "%")

    print(classification_report(y_test, pred))

    if acc > best_accuracy:

        best_accuracy = acc

        best_model = model

# --------------------------
# Save Model
# --------------------------

joblib.dump(best_model, "models/model.pkl")

joblib.dump(vectorizer, "models/vectorizer.pkl")

print("\nBest Accuracy:", round(best_accuracy * 100, 2), "%")
print("Model Saved Successfully")