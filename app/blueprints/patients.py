"""reports.py

Gets the report of the certain patients.
"""

import os

from flask import Blueprint, current_app, render_template, request, send_from_directory, send_from_directory
from werkzeug.utils import secure_filename

from app.lib.prediction import get_prediction

from ..gen_patients import Patient
from ..util.db import get_db
from ..util.helper import get_best_model
from .auth import login_required

bp = Blueprint("patients", __name__, url_prefix="/patients")


@bp.route("/")
@login_required
def patients():
    return render_template("patients/patients.html")


@bp.route("/get_reports")
@login_required
def reports():
    db = get_db()
    patient_list = db.execute("SELECT name FROM patients").fetchall()
    model_list = get_best_model() 
    return render_template("patients/get_reports.html", patient_list=patient_list, model_list=model_list)


@bp.route("/registration", methods=["GET", "POST"])
@login_required
def patient_registration():
    error = None
    message = ''
    if request.method == "POST":
        fname = request.form["fname"]
        lname = request.form["lname"]
        admission_date = request.form["date"]
        report = request.files["report"]

        if not fname: fname = "John"
        if not lname: lname = "Doe"
        if report:
            filename = secure_filename(report.filename)
            destination = os.path.join(current_app.config["PATIENT_FOLDER"], filename)
            report.save(destination)

        _patient = Patient(filename, fname, lname, admission_date)
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
    patient_name = request.form["patient"]
    model = request.form["model"]
    db = get_db()

    _patient = db.execute("SELECT * FROM patients WHERE name = ?", (patient_name,)).fetchone()
    patient = {
        "id": _patient["id"],
        "name": _patient["name"],
        "admission_date": _patient["admission_date"],
        "report_url": _patient["report_url"],
    }

    patient_report_path = os.path.join(current_app.config["PATIENT_FOLDER"], patient["report_url"])
    best_model_dir = os.path.join(current_app.config["MODELS_FOLDER"], "best_model")
    model_url = os.path.join(best_model_dir, model)
    result = get_prediction(patient_report_path, model_url, is_testing_set=True)
    patient["result"] = "Negative" if result[0] == 'absent' else "Positive"
    return render_template("patients/reports.html", patient=patient)


@bp.route('/uploads/<path:filename>', methods=['GET', 'POST'])
@login_required
def download(filename):
    return send_from_directory(directory=current_app.config["PATIENT_FOLDER"], path=filename, filename=filename)
