"""selector.py blueprint

Provies the selector menu and resutls to the web application.
"""
import os

from flask import Blueprint, current_app, render_template, request
from werkzeug.utils import secure_filename

from .. import api
from .auth import login_required

bp = Blueprint("selector", __name__, url_prefix="/selector")


@bp.route("/")
@login_required
def selector():
    """This page provides input field to upload the training data.

    Returns:
        selector.html (html_template): Provides selection page with
                                       file_input field
    """
    return render_template("selector/selector.html")


@bp.route("/display")
@login_required
def selector_display():
    """Displays the selected model to user in label field.

    Returns:
        selector_selected (html_template): Provides label field.
    """
    uploaded_file = request.files["file"]
    destination = os.path.join(current_app.config["UPLOAD_FOLDER"], secure_filename(uploaded_file.filename))
    uploaded_file.save(destination)
    selected_model = api.train_model(destination)
    return render_template("selector_selected.html", message=selected_model)
