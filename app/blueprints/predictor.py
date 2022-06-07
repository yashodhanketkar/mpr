"""predictor.py blueprint

Provies the predictor menu and resutls to the web application.
"""
import os

from flask import Blueprint, current_app, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename

from .. import api
from ..helper import get_best_model, get_stored_data
from .auth import login_required

bp = Blueprint("predictor", __name__, url_prefix="/predictor")


@bp.route("/")
@login_required
def predictor():
    """This page provides user the options for the predictions. The
    user is provided two lists
    1. List of the database provided by user
    2. List of the suitabel model trained by the system

    Return:
        predictor.html (html template): Returns the predictor page with
                                        required data.
    """
    model_list = get_best_model()
    data_list = get_stored_data("test")
    return render_template("predictor/predictor.html", data_list=data_list, model_list=model_list)


@bp.route("/upload", methods=("GET", "POST"))
@login_required
def upload_test_file():
    """This function provides the user ability to upload dataset for
    prediction.

    Returns:
        predictor.html (html template): Redirects to the predictor
                                        page.
    """
    uploaded_file = request.files["file"]
    destination = os.path.join(current_app.config["TEST_FOLDER"], secure_filename(uploaded_file.filename))
    uploaded_file.save(destination)
    return redirect(url_for("predictor.predictor"))


@bp.route("/display", methods=("GET", "POST"))
@login_required
def predictor_display():
    """This page displays the results of the preedictions

    Returns:
        predictor.html (html template): If incorrect data is provided
        prediction.html (html template): Displays predictions results
    """
    if request.form["data"] == "empty" or request.form["model"] == "empty":
        return redirect(url_for("predictor.predictor"))
    data = request.form["data"]
    model = request.form["model"]
    data_url = os.path.join(current_app.config["TEST_FOLDER"], data)
    best_model_dir = os.path.join(current_app.config["MODELS_FOLDER"], "best_model")
    model_url = os.path.join(best_model_dir, model)
    prediction = api.get_predictions(model_url, data_url)
    arr_pres = 0
    for value in prediction.values():
        if value == "present":
            arr_pres += 1
    pred_len = len(prediction)
    return render_template(
        "predictor/predictions.html",
        predictions=prediction,
        arr_present=arr_pres,
        prediction_length=pred_len,
    )
