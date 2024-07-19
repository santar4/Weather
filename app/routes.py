from datetime import datetime, timedelta

from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from app import app, tools, db
from app.forms import CityForm, SignupForm, LoginForm
from app.models import User
from app.tools import get_weather


@app.route('/')
def home():
    return render_template('home.html')


@app.route("/weather/<city>/")
def weather(city):
    data: int | dict = tools.get_weather(city)
    if type(data) is int:
        flash(f"Неправильна назва міста: {city}")
        return redirect(url_for("home"))
    return render_template("weather.html", data=data, city=city)


@app.route('/search', methods=["GET", "POST"])
def weather_search():
    if request.method == "POST":
        city = request.form.get("search")
        if not city:
            flash("Please enter a city.")
            return redirect(url_for("weather_search"))
        data = tools.get_weather(city)
        if type(data) is int:
            flash(f"Can't get weather for this city, check name city: <b>{city}</b>")
            return redirect(url_for("weather_search"))

        return render_template("weather.html", data=data, city=city)

    return render_template("base.html")


def datetime_filter(timestamp):
    return datetime.fromtimestamp(timestamp).strftime('%H:%M')

app.jinja_env.filters['datetime'] = datetime_filter



@app.route("/signup/", methods=["GET", "POST"])
def signup():
    form = SignupForm()

    if form.validate_on_submit():
        user = db.session.execute(db.select(User).where(User.email == form.email.data)).scalar()
        if user:
            flash("User currently exists")
            return redirect(url_for("login"))
        new_user = User(
            nickname=form.nickname.data,
            email=form.email.data,
            password=generate_password_hash(form.password.data)
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("users/signup.html", form=form, title="Signup")


@app.route("/login/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(User).where(User.nickname == form.nickname.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for("home"))
            flash("Wrong password")
            return redirect(url_for("login"))

        flash("Wrong nickname")
        return redirect(url_for("login"))

    return render_template("users/login.html", form=form, title="Login")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))
