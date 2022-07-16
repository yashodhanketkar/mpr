"""reports.py

Gets the report of the certain patients.
"""

import json
import os

from flask import Blueprint, current_app, render_template, request, send_from_directory, send_from_directory, flash
from werkzeug.utils import secure_filename

from app.lib.prediction import get_prediction

from ..gen_patients import get_patients, example, Patient
from ..util.db import get_db
from ..util.helper import get_best_model, get_stored_data
from .auth import login_required

bp = Blueprint("patients", __name__, url_prefix="/patients")


@bp.route("/")
@login_required
def patients():
    return render_template("patients/patients.html")


@bp.route("/get_reports")
@login_required
def reports():
    patient_list = get_stored_data("patients")
    patient_list = get_patients()
    model_list = get_best_model() 
    return render_template("patients/get_reports.html", patient_list=patient_list, model_list=model_list)


@bp.route("/registration", methods=["GET", "POST"])
@login_required
def patient_registration():
    error = None
    message = ''
    if request.method == "POST":
        fname = request.form["fname"]
        if not fname: fname = "John"
        lname = request.form["lname"]
        if not lname: lname = "Doe"
        admission_date = request.form["date"]
        report = request.files["report"]
        if report:
            filename = secure_filename(report.filename)
        url = os.path.join(current_app.config["PATIENT_FOLDER"], filename)
        print(fname, lname, admission_date, url)
        _patient = Patient(url, fname, lname, admission_date)
        print(_patient)
        message = f"{_patient.name} registered succesfully"
        db = get_db()

        if error is None:
            try:
                db.execute(
                    "INSERT INTO patients(id, name, admission_date, report_url) VALUES (?,?,?,?)",
                    (_patient.id, _patient.name, _patient.admission_date, _patient.report_url),
                )
                db.commit()
            except db.IntegrityError:
                error = "Information provided is wrong"
                return error
    return render_template("patients/registration.html", message=message)


@bp.route("/display", methods=["POST"])
@login_required
def reports_dispaly():
    patient_str = request.form["patient"]
    model = request.form["model"]
    patient = json.loads(patient_str)
    patient_report_path = os.path.join(current_app.config["PATIENT_FOLDER"], patient["report_url"])
    best_model_dir = os.path.join(current_app.config["MODELS_FOLDER"], "best_model")
    model_url = os.path.join(best_model_dir, model)
    result = get_prediction(patient_report_path, model_url, is_testing_set=True)
    patient["result"] = "Negative" if result[0] == 'absent' else "Positive"
    return render_template("patients/reports.html", patient=patient)


@bp.route("/display", methods=["GET"])
@login_required
def reports_dispaly_get():
    patient = example()
    result = get_prediction(r"app\static\patients\patient_1.csv", r"model\best_model\dataset1.sav", is_testing_set=True)
    _result = "Negative" if result[0] == 'absent' else "Positive"
    patient.__setattr__("result", _result)
    return render_template("patients/reports.html", patient=patient)


@bp.route('/uploads/<path:filename>', methods=['GET', 'POST'])
@login_required
def download(filename):
    return send_from_directory(directory=current_app.config["PATIENT_FOLDER"], path=filename, filename=filename)
