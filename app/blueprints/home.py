from flask import (
    Blueprint,
    render_template,
    session,
)

bp = Blueprint("home", __name__)


@bp.route("/")
def home():
    user = None
    if "username" in session:
        user = session["username"]
        print(user)
    else:
        user = "Guest"
    return render_template("main/home.html", user=user)
