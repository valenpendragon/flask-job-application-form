from flask import Flask, render_template, request

app = Flask(__name__)


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
        start_date = request.form["start_date"]
        print(f"start date: {start_date}")
        occupation = request.form["occupation"]
        print(f"occupation: {occupation}")
    return render_template("index.html")


app.run(debug=True, port=5001)
