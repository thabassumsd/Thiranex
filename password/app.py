from flask import Flask, render_template, request
from analyzer import analyze_password
from generator import generate_password
from database import init_db, save_password, is_reused

app = Flask(__name__)

init_db()

@app.route("/", methods=["GET", "POST"])
def home():
    result = None

    if request.method == "POST":
        password = request.form.get("password")

        if password:
            reused = is_reused(password)
            strength, score, feedback = analyze_password(password)
            suggestion = generate_password()

            save_password(password)

            result = {
                "password": password,
                "reused": reused,
                "strength": strength,
                "score": score,
                "feedback": feedback,
                "suggestion": suggestion
            }

    return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)