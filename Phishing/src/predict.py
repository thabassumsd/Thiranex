import os
import joblib
import pandas as pd
from scipy.sparse import hstack

from src.preprocess import preprocess_text
from src.feature_extraction import extract_url_features, keyword_count

# -------------------------------------------------
# Load trained model and TF-IDF vectorizer
# -------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(BASE_DIR, "model", "phishing_model.pkl")
VECTORIZER_PATH = os.path.join(BASE_DIR, "model", "vectorizer.pkl")

model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)


# -------------------------------------------------
# Prediction Function
# -------------------------------------------------

def predict_email(email_text):

    # Clean email text
    cleaned_text = preprocess_text(email_text)

    # TF-IDF Features
    text_features = vectorizer.transform([cleaned_text])

    # URL Features
    url_features = extract_url_features(email_text)

    # Keyword Count
    keywords = keyword_count(email_text)

    # Combine numerical features
    extra_features = pd.DataFrame([url_features + [keywords]])

    # Merge TF-IDF + URL Features
    final_features = hstack([text_features, extra_features.values])

    # Predict
    prediction = model.predict(final_features)[0]

    # Probability (if supported)
    probability = None

    if hasattr(model, "predict_proba"):
        probability = model.predict_proba(final_features)[0].max() * 100
        print("Prediction value:", prediction)

    if prediction == 1:
        result = "Phishing"
    else:
        result = "Safe"

    return result, probability


# -------------------------------------------------
# Testing
# -------------------------------------------------

if __name__ == "__main__":

    print("=" * 60)
    print("      PHISHING EMAIL DETECTION")
    print("=" * 60)

    email = input("\nEnter Email:\n\n")

    result, probability = predict_email(email)

    print("\nPrediction :", result)

    if probability is not None:
        print(f"Confidence : {probability:.2f}%")