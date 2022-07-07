"""reports.py

Gets the report of the certain patients.
"""

from flask import Blueprint, current_app, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename

from ..util.helper import get_best_model
from .auth import login_required

bp = Blueprint("reports", __name__, url_prefix="/reports")

@bp.route("/")
@login_required
def reports():
    patient_list = ["Timmy", "Jim"]
    model_list = get_best_model() 
    return render_template("reports/reports.html", patient_list=patient_list, model_list=model_list)
