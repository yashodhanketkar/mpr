"""auth.py blueprint

Provides the authorization functionality to the web application.
"""
import functools

from flask import Blueprint, flash, redirect, render_template, request, session, url_for, abort
from werkzeug.security import check_password_hash, generate_password_hash

from app.db import get_db

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=("GET", "POST"))
def register():
    """Registers users with unique username.

    Args:
        POST.USERNAME (str): Username provided by user with POST method
        POST.PASSWORD (str): Password provided by user with POST method

    Returns:
        login.html (html_template): if no error is present
        register.html (html_template): if error is present
    """
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
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = "Username already present."
            else:
                return redirect(url_for("auth.login"))
    flash(error)

    return render_template("auth/register.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    """Logins the user.

    Args:
        POST.USERNAME (str): Username provided by user with POST method
        POST.PASSWORD (str): Password provided by user with POST method

    Returns:
        home.html (html_template): if username is in session
        login.html (html_template): if username is not in session
    """
    error = None
    if "user_id" in session:
        return redirect(url_for("home.home"))
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()

        user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()

        if not user:
            error = "Invalid credentials."
        elif not check_password_hash(user["password"], password):
            error = "Invalid credentials."

        if error is None:
            session.clear()
            session["username"] = user["username"]
            session["userrole"] = user["userrole"]
            return redirect(url_for("home.home"))

    return render_template("auth/login.html", error=error)


@bp.route("/unauth")
def unauth():
    """Provides unautharized page.

    Returns:
        unauth.html (html_template): if username is not in session
    """
    return render_template("auth/unauth.html")


@bp.route("/logout")
def logout():
    """Clears the users session and redirect to login page.

    Returns:
        login.html (html_template): Redirect to login page
    """
    session.clear()
    return redirect(url_for("auth.login"))


def login_required(view):
    """Decorater for login access.

    Args:
        view (view): Request for the view function

    Returns:
        unauth.html (html_template): if username is not in session
        wrapped_view (function) -> *.html (html_template)
            : if username is in session
    """

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if "username" not in session:
            print("No username in session")
            abort(401)
        return view(**kwargs)

    return wrapped_view
