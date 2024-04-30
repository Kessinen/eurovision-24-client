from flask import Flask, redirect, url_for, render_template, request, make_response
from os import environ
from requests import get, post

from forms import LoginForm, ReviewForm
from rich import print


app = Flask(__name__)
app.secret_key = environ.get("SECRET_KEY", "secret_key")
app.config["SECRET_KEY"] = environ.get("SECRET_KEY", "secret_key")
api_url = environ.get("API_URL", "http://localhost:8000/api/v1/")

@app.route("/", methods=["GET", "POST"])
def index():
    if not request.cookies.get("apikey"):
        return redirect(url_for("login"))
    return render_template("index.html", is_logged_in=True)

@app.route("/round", methods=["GET", "POST"])
def participants_in_round():
    round_number = request.args.get("round")
    if round_number is None:
        return redirect(url_for("index"))
    participant_list = get(api_url + "participant/round/"+str(round_number)).json()
    if request.cookies.get("apikey"):
        is_logged_in = True
    logged_user = None
    return render_template("participants.html", participants=participant_list, is_logged_in=is_logged_in)


@app.route("/login", methods=["GET", "POST"])
def login():
    #users = get(api_url + "user/all").json()

    login_form = None
    form = LoginForm()

    if form.username.data and form.pin.data:
        post_data = {"username": form.username.data, "pin": form.pin.data}
        key = post(api_url + "user/login", params=post_data)
        if key.status_code == 200 and key.json()["apikey"]:
            api_key = key.json()["apikey"]
            response = make_response(redirect(url_for("index")))
            response.set_cookie("apikey", api_key)
            return response
    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    response = make_response(redirect(url_for("login")))
    response.delete_cookie("apikey")
    return response

if __name__ == "__main__":
    app.run(debug=True)