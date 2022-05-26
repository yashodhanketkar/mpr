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


# @bp.route("/login", methods=("GET", "POST"))


@bp.route("/")
def home():
    user = None
    if "username" in session:
        user = session["username"]
        print(user)
    else:
        user = "Guest"
    return render_template("main/home.html", user=user)
