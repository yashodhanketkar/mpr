"""selector.py blueprint

Provies the selector menu and resutls to the web application.
"""
import os

from flask import Blueprint, current_app, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename

from .. import api
from ..helper import get_stored_data
from .auth import login_required

bp = Blueprint("selector", __name__, url_prefix="/selector")


def weight_register(*mets):
    """This function processes metrics into the weightage

    Args:
        *mets (tuple): The tuple of metrics name

    Returns:
        weights (dict): The dictionary of the metrics and thier
                        preference.
    """
    weights = {}
    for metric in mets:
        weights[metric.lower()] = int(request.form[metric][-1])
    return weights


@bp.route("/")
@login_required
def selector():
    """This page provides input field to upload the training data.

    Returns:
        selector.html (html_template): Provides selection page with
                                       file_input field
    """
    data_list = get_stored_data("data")
    return render_template("selector/selector.html", data_list=data_list)


@bp.route("/upload", methods=("GET", "POST"))
@login_required
def upload():
    """This function provides the user ability to upload dataset for
    training.

    Returns:
        selector.html (html template): Redirects to the selector page.
    """
    uploaded_file = request.files["file"]
    destination = os.path.join(current_app.config["UPLOAD_FOLDER"], secure_filename(uploaded_file.filename))
    uploaded_file.save(destination)
    return redirect(url_for("selector.selector"))


@bp.route("/display", methods=("GET", "POST"))
@login_required
def selector_display():
    """Displays the selected model to user in label field.

    Returns:
        selector_selected (html_template): Provides label field.
    """
    if request.form["data"] == "empty":
        return redirect(url_for("selector.selector"))
    data = request.form["data"]
    weights = weight_register("Accuracy", "F1", "Precision", "Recall", "ROC")
    weights["pred_time"] = request.form["Time"]
    data_url = os.path.join(current_app.config["UPLOAD_FOLDER"], data)
    selected_model = api.train_model(data_url, weights)
    message = f"{selected_model[0]} is most suited model for {selected_model[1]} dataset."
    return render_template("selector/selector_selected.html", message=message, weights=weights)
