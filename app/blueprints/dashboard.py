import os

from flask import Blueprint, redirect, render_template, url_for

from ..helper import get_cross_performance_graph, save_cross_performance_data
from .auth import login_required


bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")


@bp.route("/")
def dashboard():
    """This displays graphical performance metrics of the best suited
    model for available training datasets.

    Returns:
        dashoboard.html (html template): Provides the graphical display
    """
    best_model_dir = os.path.join(os.getcwd(), r"model\cross_performance")
    if not any(os.scandir(best_model_dir)):
        return redirect(url_for("dashboard.empty"))
    performance_plots = get_cross_performance_graph()
    return render_template("dashboard/dashboard.html", performance_plots=performance_plots)


@bp.route("/empty")
@login_required
def empty():
    """This displays the message when cross-performance data is not
    available

    Returns:
        dashboard_home.html (html template): Provides the message
    """
    return render_template("dashboard/dashboard_home.html")


@bp.route("/update", methods=("GET", "POST"))
@login_required
def get_cross_performance_files():
    """This function allows user to generate cross-performance results.

    Returns:
        dashobard.html (html template): Redirects to dashobard page
    """
    save_cross_performance_data()
    return redirect(url_for("dashboard.dashboard"))
