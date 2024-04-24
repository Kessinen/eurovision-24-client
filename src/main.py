from flask import Flask, redirect, url_for, render_template, request
from os import environ
from requests import get

from forms import LoginForm, ReviewForm


app = Flask(__name__)
app.secret_key = environ.get("SECRET_KEY", "secret_key")
app.config["SECRET_KEY"] = environ.get("SECRET_KEY", "secret_key")
api_url = environ.get("API_URL", "http://localhost:8088/api/v1/")

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/round", methods=["GET", "POST"])
def participants_in_round():
    round_number = request.args.get("round")
    if round_number is None:
        return redirect(url_for("index"))
    participant_list = get(api_url + "participant/round/"+str(round_number)).json()
    logged_user = None
    return render_template("participants.html", participants=participant_list, logged_user=logged_user)


@app.route("/login", methods=["GET", "POST"])
def login():
    #users = get(api_url + "user/all").json()

    login_form = None
    form = LoginForm()
    return render_template("login.html", form=form)

if __name__ == "__main__":
    app.run(debug=True)