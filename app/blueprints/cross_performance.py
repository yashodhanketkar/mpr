import ast
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
    abort
)

from .. import api
from ..helper import get_stored_models, get_stored_data, plot_performance
from flask import current_app

bp = Blueprint("cross-performance", __name__, url_prefix="/cross_performance")


@bp.route("/")
def cross_performance():
    model_list = get_stored_models()
    data_list = get_stored_data("data")
    return render_template(
            "performance/cross_performance.html",
            model_list=model_list,
            data_list=data_list
        )


@bp.route("/display", methods=("GET", "POST"))
def cross_performance_display():

    dataset_dir = []
    model = request.form["model"]
    model_dir, model_name = ast.literal_eval(model)
    model_path = os.path.join(current_app.config["MODELS_FOLDER"], rf"models\{model_dir}\{model_name}")

    dataset_list = request.form.getlist("dataset")
    for dataset in dataset_list:
        dataset_dir.append(os.path.join(current_app.config["UPLOAD_FOLDER"], dataset))
    if len(dataset_dir) == 2:
        dataset1_path, dataset2_path = dataset_dir
    else:
        return abort(416)
    model_cross_performance = api.model_cross_performance_specific_model(model_path, dataset1_path, dataset2_path)
    cross_performance_plot = plot_performance(model_cross_performance, True)
    return render_template(
        "performance/cross_performance_display.html",
        cross_performance_plot=cross_performance_plot,
    )