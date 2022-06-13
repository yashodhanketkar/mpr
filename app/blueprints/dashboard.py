import os

from flask import Blueprint, render_template, url_for, redirect
# , abort, current_app, request

from ..helper import save_cross_performance_data, get_cross_performance_graph
from .auth import login_required

bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")


@bp.route("/")
def display_graphs():
    best_model_dir = os.path.join(os.getcwd(), r'model\cross_performance')
    if not any(os.scandir(best_model_dir)):
        return redirect(url_for("dashboard.empty"))
    performance_plots = get_cross_performance_graph()
    return render_template("dashboard/dashboard.html", performance_plots=performance_plots)


@bp.route("/empty")
@login_required
def empty():
    return render_template("dashboard/dashboard_home.html")


@bp.route('/update', methods=('GET', 'POST'))
@login_required
def get_cross_performance_files():
    save_cross_performance_data()
    return redirect(url_for("dashboard.dashboard"))
