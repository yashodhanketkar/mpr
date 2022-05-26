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
    current_app,
)
from werkzeug.utils import secure_filename

from ..helper import get_best_model, get_stored_data
from .. import api


bp = Blueprint("predictor", __name__, url_prefix="/predictor")


@bp.route("/")
def predictor():
    model_list = get_best_model()
    data_list = get_stored_data("test")
    return render_template("predictor/predictor.html", data_list=data_list, model_list=model_list)


@bp.route("/upload", methods=("GET", "POST"))
def upload_test_file():
    uploaded_file = request.files["file"]
    destination = os.path.join(current_app.config["TEST_FOLDER"], secure_filename(uploaded_file.filename))
    uploaded_file.save(destination)
    return redirect(url_for("predictor"))


@bp.route("/display", methods=("GET", "POST"))
def predictor_display():
    if request.form["data"] == "empty" or request.form["model"] == "empty":
        return redirect(url_for("predictor"))
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
