from flask import Flask, render_template, request
from src.predict import predict_email

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():

    email = request.form["email"]

    result, confidence = predict_email(email)

    return render_template(
        "index.html",
        prediction=result,
        confidence=confidence,
        email=email
    )

if __name__ == "__main__":
    app.run(debug=True)