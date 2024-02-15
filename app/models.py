from datetime import datetime, timezone
from hashlib import md5
from time import time
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from app import app, db, login


class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(
        sa.String(64), index=True, unique=True
    )
    email: so.Mapped[str] = so.mapped_column(
        sa.String(120), index=True, unique=True
    )
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    about_me: so.Mapped[Optional[str]] = so.mapped_column(sa.String(140))
    last_seen: so.Mapped[Optional[datetime]] = so.mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )

    def __repr__(self):
        return "<User {}>".format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode("utf-8")).hexdigest()
        return f"https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}"

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {"reset_password": self.id, "exp": time() + expires_in},
            app.config["SECRET_KEY"],
            algorithm="HS256",
        )

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(
                token, app.config["SECRET_KEY"], algorithms=["HS256"]
            )["reset_password"]
        except Exception:
            return
        return db.session.get(User, id)

    game_sessions = db.relationship(
        "GameSession", backref="user", lazy="dynamic"
    )


@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))


class GameSession(db.Model):
    id = so.mapped_column(sa.Integer, primary_key=True)
    user_id = so.mapped_column(
        sa.Integer, sa.ForeignKey("user.id"), index=True
    )
    session_date = so.mapped_column(
        sa.Date, default=datetime.now(timezone.utc), index=True
    )
    total_problems = so.mapped_column(sa.Integer)
    problems_correct = so.mapped_column(sa.Integer)
    problems_wrong = so.mapped_column(sa.Integer)
    details = so.relationship(
        "GameDetail", back_populates="session", lazy=True
    )

    def __repr__(self):
        return f"<GameSession {self.id} User {self.user_id}>"


class GameDetail(db.Model):
    id = so.mapped_column(sa.Integer, primary_key=True)
    session_id = so.mapped_column(
        sa.Integer, sa.ForeignKey("game_session.id"), index=True
    )
    operation_type = db.Column(db.String(20), index=True)
    difficulty_level = db.Column(db.String(20), index=True)
    result = so.mapped_column(sa.Boolean)
    session = so.relationship("GameSession", back_populates="details")

    def __repr__(self):
        return f"<GameDetail {self.id} Session {self.session_id}>"
