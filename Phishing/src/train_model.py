import os
import joblib
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from scipy.sparse import hstack
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

from preprocess import preprocess_text
from feature_extraction import extract_url_features, keyword_count


# -------------------------------------------------
# Load Dataset
# -------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATASET_PATH = os.path.join(BASE_DIR, "dataset", "emails.csv")

df = pd.read_csv(DATASET_PATH)

print("Dataset Loaded Successfully")
print(df.head())


# -------------------------------------------------
# Preprocess Email Text
# -------------------------------------------------

df["clean_text"] = df["text"].apply(preprocess_text)


# -------------------------------------------------
# TF-IDF Features
# -------------------------------------------------

vectorizer = TfidfVectorizer(max_features=5000)

X_text = vectorizer.fit_transform(df["clean_text"])


# -------------------------------------------------
# URL + Keyword Features
# -------------------------------------------------

extra_features = []

for email in df["text"]:

    url_features = extract_url_features(email)

    keyword = keyword_count(email)

    extra_features.append(url_features + [keyword])

extra_features = pd.DataFrame(extra_features)


# -------------------------------------------------
# Combine Features
# -------------------------------------------------

X = hstack([X_text, extra_features.values])

y = df["label"]


# -------------------------------------------------
# Train/Test Split
# -------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


# -------------------------------------------------
# Train Model
# -------------------------------------------------

model = RandomForestClassifier(
    n_estimators=500,
    random_state=42
)

model.fit(X_train, y_train)


# -------------------------------------------------
# Prediction
# -------------------------------------------------

predictions = model.predict(X_test)


# -------------------------------------------------
# Accuracy
# -------------------------------------------------

accuracy = accuracy_score(y_test, predictions)

print("\n==============================")
print("Accuracy :", accuracy)
print("==============================")

print("\nActual Labels:")
print(list(y_test))

print("\nPredicted Labels:")
print(list(predictions))

print("\nClassification Report\n")
print(classification_report(y_test, predictions))


# -------------------------------------------------
# Confusion Matrix
# -------------------------------------------------

cm = confusion_matrix(y_test, predictions)

plt.figure(figsize=(5,4))

sns.heatmap(
    cm,
    annot=True,
    fmt="d",
    cmap="Blues",
    xticklabels=["Safe", "Phishing"],
    yticklabels=["Safe", "Phishing"]
)

plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")

plt.show()


# -------------------------------------------------
# Save Model
# -------------------------------------------------

MODEL_DIR = os.path.join(BASE_DIR, "model")

os.makedirs(MODEL_DIR, exist_ok=True)

joblib.dump(
    model,
    os.path.join(MODEL_DIR, "phishing_model.pkl")
)

joblib.dump(
    vectorizer,
    os.path.join(MODEL_DIR, "vectorizer.pkl")
)

print("\nModel Saved Successfully!")