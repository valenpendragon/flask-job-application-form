from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
import os
from datetime import datetime

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("FLASK_JOB_FORM")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = os.getenv("GMAIL_ACCOUNT")
app.config["MAIL_PASSWORD"] = os.getenv("GMAIL_APP_PASSWORD")
db = SQLAlchemy(app)

mail = Mail(app)


class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(80))
    date = db.Column(db.Date)
    occupation = db.Column(db.String(80))


@app.route("/", methods=["GET", "POST"])
def index():
    print(f"request method: {request.method}")
    if request.method == "POST":
        first_name = request.form["first_name"]
        print(f"first name: {first_name}")
        last_name = request.form["last_name"]
        print(f"last name: {last_name}")
        email = request.form["email"]
        print(f"email: {email}")
        date = request.form["start_date"]
        print(f"start date: {date}")
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        occupation = request.form["occupation"]
        print(f"occupation: {occupation}")

        form = Form(first_name=first_name, last_name=last_name,
                    email=email, date=date_obj,
                    occupation=occupation)
        db.session.add(form)
        db.session.commit()

        message_body = f"Thank you for your submission, {first_name}. " \
                       f"Here is the information you submitted to us : \n" \
                       f"{first_name} {last_name}\n " \
                       f"Employment Status: {occupation}\n " \
                       f"Date available: {date} \n" \
                       f"Thank you again."

        message = Message(subject="New form submission",
                          sender=app.config["MAIL_USERNAME"],
                          recipients=[email],
                          body=message_body)
        mail.send(message)

        flash(f"{first_name}, your form was submitted successfully!", "success")

    return render_template("index.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True, port=5001)
