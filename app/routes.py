import os
from datetime import datetime, timezone, timedelta
from urllib.parse import urlsplit
from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_user, logout_user, current_user, login_required
import sqlalchemy as sa
from app import app, db
from app.forms import (
    LoginForm,
    RegistrationForm,
    EditProfileForm,
    ResetPasswordRequestForm,
    ResetPasswordForm,
)
from app.models import User, Post, GameDetail, GameSession
from app.email import send_password_reset_email


# used for testing only until microservice is available
import random


# send-email?subject=Winter%20is%20Coming&recipient=d.kallail@gmail.com&body=Prepare%20for%20the%20White%20Walkers


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()


@app.route("/")
def index():
    return render_template("index.html", title="Home")


# Update this URL to partner's microservice endpoint
MICROSERVICE_URL = "http://localhost:8000/api/mock_generate_numbers"


def get_numbers_from_microservice(difficulty):
    # Point to the mock service endpoint instead of the actual microservice
    response = request.get(MICROSERVICE_URL, params={"difficulty": difficulty})
    if response.status_code == 200:
        data = response.json()
        return data["number1"], data["number2"]
    else:
        return None, None  # Handle errors appropriately


@app.route("/get_math_problem", methods=["GET"])
def get_math_problem():
    difficulty = request.args.get("difficulty", default="easy", type=str)
    num1, num2 = get_numbers_from_microservice(difficulty)

    # Modify this to generate different types of problems
    math_problem = f"{num1} + {num2}"
    return jsonify({"math_problem": math_problem, "difficulty": difficulty})


@app.route("/start_game", methods=["POST"])
def start_game():
    difficulty = request.form["difficulty"]
    # partner's microservice to get the math problem
    # based on difficulty. For now, use the dummy function
    num1, num2 = get_numbers_from_microservice(difficulty)
    math_problem = f"{num1} + {num2}"
    # Redirect to a new route that displays the math problem, or directly
    # render a template with the problem
    return jsonify({"math_problem": math_problem, "difficulty": difficulty})


@app.get("/game")
def game():
    return render_template("game.html")


@app.route("/api/mock_generate_numbers")
def mock_generate_numbers():
    difficulty = request.args.get("difficulty", "easy")

    if difficulty == "hard":
        num_range = (100, 999)
    elif difficulty == "medium":
        num_range = (10, 99)
    else:  # Default to 'easy'
        num_range = (1, 9)

    number1, number2 = sorted(
        (random.randint(*num_range), random.randint(*num_range)), reverse=True
    )

    # Only return the two numbers, without options
    return jsonify(number1=number1, number2=number2)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data)
        )
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        if not next_page or urlsplit(next_page).netloc != "":
            next_page = url_for("index")
        return redirect(next_page)
    return render_template("login.html", title="Sign In", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Congratulations, you are now a registered user!")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


@app.route("/reset_password_request", methods=["GET", "POST"])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.email == form.email.data)
        )
        if user:
            send_password_reset_email(user)
        flash("Check your email for the instructions to reset your password")
        return redirect(url_for("login"))
    return render_template(
        "reset_password_request.html", title="Reset Password", form=form
    )


@app.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for("index"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash("Your password has been reset.")
        return redirect(url_for("login"))
    return render_template("reset_password.html", form=form)


@app.route("/user/<username>")
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    game_sessions = user.game_sessions.order_by(
        GameSession.session_date.desc()
    )

    return render_template("user.html", user=user, game_sessions=game_sessions)


@app.route("/edit_profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash("Your changes have been saved.")

        # Redirect to the user's profile page after successful update
        return redirect(url_for("user", username=current_user.username))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template(
        "edit_profile.html", title="Edit Profile", form=form
    )


@app.route("/submit_game", methods=["POST"])
@login_required
def submit_game():
    try:
        data = request.json
        print("Received data:", data)  # Verify data is received correctly

        # Find the most recent session for the current user within the last 24 hours
        last_24_hours = datetime.now() - timedelta(days=1)
        recent_session = (
            GameSession.query.filter(
                GameSession.user_id == current_user.id,
                GameSession.session_date >= last_24_hours,
            )
            .order_by(GameSession.session_date.desc())
            .first()
        )

        # If a session exists, update it
        if recent_session:
            recent_session.total_problems += data["total_problems"]
            recent_session.problems_correct += data["problems_correct"]
            recent_session.problems_wrong += data["problems_wrong"]
        else:
            # If no session exists within the last 24 hours, create a new one
            new_session = GameSession(
                user_id=current_user.id,
                session_date=datetime.now(),
                total_problems=data["total_problems"],
                problems_correct=data["problems_correct"],
                problems_wrong=data["problems_wrong"],
            )
            db.session.add(new_session)

        print("Attempting to commit session")
        db.session.commit()
        print("Game results submitted successfully")
        return jsonify({"message": "Game results submitted successfully!"})

    except Exception as e:
        # Log the exception and return an error response
        print(f"Error submitting game results: {e}")
        return jsonify({"error": "Failed to submit game results"}), 500
