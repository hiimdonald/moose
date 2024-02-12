import zmq
from datetime import datetime, timezone, timedelta
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
from app.models import User, GameSession
from app.email import send_password_reset_email

# Initialize ZeroMQ for communication with microservices
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://127.0.0.1:8888")


@app.before_request
def before_request():
    """Update last seen time for logged-in users before every request."""
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()


@app.route("/")
def index():
    """Render the homepage."""
    return render_template("index.html", title="Home")


@app.route("/microservice/<difficulty>")
def get_numbers_from_microservice(difficulty):
    """Fetch numbers from a microservice based on difficulty level."""
    try:
        if difficulty not in ["easy", "medium", "hard"]:
            raise ValueError("Invalid difficulty level")

        socket.send_string(difficulty)
        response = socket.recv_json()
        return jsonify(number1=response["num1"], number2=response["num2"])
    except Exception as e:
        print(f"Error fetching numbers from microservice: {e}")
        return jsonify(error="Failed to fetch numbers"), 500


@app.route("/game")
def game():
    """Render the game page."""
    return render_template("game.html", title="Game")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Authenticate users and log them in."""
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
        next_page = request.args.get("next", url_for("index"))
        return redirect(next_page)

    return render_template("login.html", title="Sign In", form=form)


@app.route("/logout")
def logout():
    """Log out the current user."""
    logout_user()
    return redirect(url_for("index"))


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register a new user."""
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
    """Request a password reset."""
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
    """Reset a user's password using a token."""
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
    """Display a user's profile, including their game sessions."""
    user = User.query.filter_by(username=username).first_or_404()
    game_sessions = user.game_sessions.order_by(
        GameSession.session_date.desc()
    )
    return render_template(
        "user.html", user=user, game_sessions=game_sessions, title=username
    )


@app.route("/edit_profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    """Allow users to edit their profile."""
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash("Your changes have been saved.")
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
    """Submit game results for a user session."""
    try:
        data = request.json
        print("Received data:", data)  # Verify data is received correctly

        # Find the most recent session for current user within the last 24hrs
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


@app.route("/about")
def about():
    """Render the about page."""
    return render_template("about.html", title="About")


@app.route("/contact")
def contact():
    """Render the contact page."""
    return render_template("contact.html", title="Contact")
