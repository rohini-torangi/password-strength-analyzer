from flask import Flask, render_template, request, session
import hashlib
import secrets
import string

app = Flask(__name__)
app.secret_key = "password-security-lab-key"


def check_password_strength(password):
    score = 0
    suggestions = []

    if len(password) >= 8:
        score += 1
    else:
        suggestions.append("Use at least 8 characters.")

    if any(c.isupper() for c in password):
        score += 1
    else:
        suggestions.append("Add uppercase letters.")

    if any(c.islower() for c in password):
        score += 1
    else:
        suggestions.append("Add lowercase letters.")

    if any(c.isdigit() for c in password):
        score += 1
    else:
        suggestions.append("Add numbers.")

    if any(c in string.punctuation for c in password):
        score += 1
    else:
        suggestions.append("Add special characters.")

    if score <= 2:
        strength = "Weak"
    elif score <= 4:
        strength = "Medium"
    else:
        strength = "Strong"

    return score, strength, suggestions


@app.route("/", methods=["GET", "POST"])
def index():

    result = None
    score = 0
    strength = ""
    suggestions = []
    hashed_password = ""
    otp_message = ""

    if request.method == "POST":

        password = request.form.get("password", "")

        score, strength, suggestions = check_password_strength(password)

        # SHA-256 Hash
        hashed_password = hashlib.sha256(
            password.encode()
        ).hexdigest()

        # Generate 6 digit OTP
        otp = str(secrets.randbelow(900000) + 100000)

        session["otp"] = otp

        otp_message = f"Demo OTP: {otp}"

        result = True

    return render_template(
        "index.html",
        result=result,
        score=score,
        strength=strength,
        suggestions=suggestions,
        hashed_password=hashed_password,
        otp_message=otp_message
    )


@app.route("/verify", methods=["POST"])
def verify():

    entered_otp = request.form.get("otp", "")
    actual_otp = session.get("otp")

    if entered_otp == actual_otp:
        message = "OTP Verified Successfully!"
    else:
        message = "Invalid OTP. Please try again."

    return render_template(
        "index.html",
        result=False,
        score=0,
        strength="",
        suggestions=[],
        hashed_password="",
        otp_message=message
    )


if __name__ == "__main__":
    app.run(debug=True)
