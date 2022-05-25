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

bp = Blueprint("home", __name__)


@bp.route("/login", methods=("GET", "POST"))
def login():
    error = None
    if request.method == "POST":
        if request.form["username"] != "admin":
            error = "Invalid user"
        elif request.form["password"] != "admin":
            error = "Invalid password"
        else:
            session["username"] = request.form["username"]
            return redirect(url_for("home.home"))
    return render_template("login.html", error=error)


@bp.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("front"))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("home.login"))

        return view(**kwargs)

    return wrapped_view


@bp.route("/")
def front():
    return redirect(url_for("home"))


@bp.route("/home")
@login_required
def home():
    username = 'Loureist'
    return render_template("home.html", user=username)
