import json
import os

from flask import (
    Blueprint,
    current_app,
    redirect,
    render_template,
    request,
    url_for,
)

from ..helper import get_best_model, plot_performance
from .auth import login_required

bp = Blueprint("performance", __name__, url_prefix="/performance")


@bp.route("/")
@login_required
def performance():
    model_list = get_best_model()
    return render_template("performance/performance.html", model_list=model_list)


@bp.route("/display", methods=("POST", "GET"))
@login_required
def performance_display():
    if request.form["name"] == "empty":
        return redirect(url_for("performance"))
    file_name = request.form["name"].split(".")[0]
    performance_url = os.path.join(current_app.config["MODELS_FOLDER"], rf"performance/{file_name}.json")
    with open(performance_url, "r", encoding="utf-8") as json_file:
        item = json.load(json_file)
    performance_plot = plot_performance(item)
    model_list = get_best_model()
    return render_template(
        "performance/performance_display.html",
        model_list=model_list,
        performance_plot=performance_plot,
    )
