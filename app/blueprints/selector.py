import os

from flask import (
    Blueprint,
    current_app,
    render_template,
    request,
)
from werkzeug.utils import secure_filename

from .auth import login_required
from .. import api

bp = Blueprint("selector", __name__, url_prefix="/selector")


@bp.route("/")
@login_required
def selector():
    return render_template("selector/selector.html")


@bp.route("/display")
@login_required
def selector_display():
    uploaded_file = request.files["file"]
    destination = os.path.join(current_app.config["UPLOAD_FOLDER"], secure_filename(uploaded_file.filename))
    uploaded_file.save(destination)
    selected_model = api.train_model(destination)
    return render_template("selector_selected.html", message=selected_model)
