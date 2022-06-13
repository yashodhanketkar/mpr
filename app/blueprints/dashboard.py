from flask import Blueprint, render_template, url_for, redirect
# , abort, current_app, request

from ..helper import save_cross_performance_data
from .auth import login_required

bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")


@bp.route("/")
@login_required
def dashboard():
    return render_template("dashboard/dashboard_home.html")


@bp.route('/update', methods=('GET', 'POST'))
@login_required
def get_cross_performance_files():
    save_cross_performance_data()
    return redirect(url_for("dashboard.dashboard"))


def display_graphs():
    ...
