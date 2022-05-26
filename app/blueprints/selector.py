import os

from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    url_for,
    session,
    current_app
)
from werkzeug.utils import secure_filename

from .. import api

bp = Blueprint("selector", __name__, url_prefix="/selector")


@bp.route("/")
def selector():
    return render_template("selector/selector.html")


@bp.route("/display")
def selector_display():
    uploaded_file = request.files["file"]
    destination = os.path.join(current_app.config["UPLOAD_FOLDER"], secure_filename(uploaded_file.filename))
    uploaded_file.save(destination)
    selected_model = api.train_model(destination)
    return render_template("selector_selected.html", message=selected_model)
