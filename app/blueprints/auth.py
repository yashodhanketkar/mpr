import functools

from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    url_for,
    session
)
from werkzeug.security import check_password_hash, generate_password_hash

from app.db import get_db

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=("GET", "POST"))
def register():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()

        if not (username or password):
            error = "Invalid credentials."

        if error is None:
            try:
                db.execute(
                    "INSERT INTO users(username, password) VALUES (?,?)",
                    (username, generate_password_hash(password))
                )
                db.commit()
            except db.IntegrityError as e:
                error = "Username already present."
            else:
                return redirect(url_for("auth.login"))
    flash(error)

    return render_template("auth/register.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    error = None
    if "user_id" in session:
        return redirect(url_for("home.home"))
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()

        user = db.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        ).fetchone()

        if not user:
            error = "Invalid credentials."
        elif check_password_hash(user["password"], password):
            error = "Invalid credentials."

        if error is None:
            session.clear()
            session["username"] = user["username"]
            return redirect(url_for("home.home"))

    return render_template("auth/login.html", error=error)


@bp.route("/unauth")
def unauth():
    return render_template("auth/unauth.html")


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if "username" not in session:
            return redirect(url_for('auth.unauth'))

        return view(**kwargs)

    return wrapped_view
