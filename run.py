"""run.py

This module handles web pages
"""


import ast
import json
import os

import pygal
from flask import (
    Flask,
    abort,
    redirect,
    render_template,
    request,
    send_file,
    session,
    url_for,
)
from werkzeug.utils import secure_filename

from app import api

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
MODELS_FOLDER = os.path.join(BASE_DIR, "model")
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static/data")
TEST_FOLDER = os.path.join(BASE_DIR, "static/test")
for _FOLDER in (UPLOAD_FOLDER, TEST_FOLDER):
    if not os.path.isdir(_FOLDER):
        os.mkdir(_FOLDER)


app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile(filename="config.py", silent=True)
app.config["MODELS_FOLDER"] = MODELS_FOLDER
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["TEST_FOLDER"] = TEST_FOLDER


def unauth():
    """This function generate responce to unautharized access"""
    response = "Please login to continue"
    return render_template("unauth.html", response=response)


def dir_listing(abs_path):
    """This function returns sub-directories or files based on recieved
    path

    Args:
        abs_path (path): Path sent by user

    Returns:
        files (path): Path to files or sub-directories
    """
    if not os.path.exists(abs_path):
        return abort(404)
    if os.path.isfile(abs_path):
        return send_file(abs_path)
    files = os.listdir(abs_path)
    return files


def get_stored_models():
    """This function returns all models generated from multiple datasets

    Returns:
        model_list (list): List of all models
    """
    model_list = []
    abs_path = os.path.join(app.config["MODELS_FOLDER"], "models")
    model_dirs = dir_listing(abs_path)
    for model_dir in model_dirs:
        new_path = abs_path + rf"\{model_dir}"
        models = dir_listing(new_path)
        model_list.append((model_dir, models))
    return model_list


def get_best_model():
    """This function returns path of best models for each dataset

    Returns:
        model_dirs (path): Path to best models
    """
    abs_path = os.path.join(app.config["MODELS_FOLDER"], "best_model")
    model_dirs = dir_listing(abs_path)
    return model_dirs


def get_stored_data(req_dir):
    """This function returns the path to stored/uploaded datasets

    Args:
        req_dir (string): Name of requested directory

    Returns:
        data_dirs (path): Path to sub-directories or files present in
                          requested directory
    """
    up_dir = os.path.join(BASE_DIR, "static")
    abs_path = os.path.join(up_dir, req_dir)
    data_dirs = dir_listing(abs_path)
    return data_dirs


def plot_performance(data, is_cross_performance=False):
    """This function plot performance graphs in form of bar chart

    Args:
        data (list/tuple): A list or tuple consist of model performance
        is_cross_performance (bool): To run in performance or
                                     cross-performance mode

    Returns:
        bar_plot_data (image): Image of the interactive bar plot based
                               on data recieved
    """
    dataset_name = ""
    names_list = []
    performance_list = []
    print(data)
    if is_cross_performance:
        metrics = ["accuracy", "f1", "precision", "recall", "roc", "pred_time"]
    else:
        metrics = ["accuracy", "f1", "precision", "recall", "roc", "pred_time"]
    for item in data:
        names_list.append(item["name"].split("_")[0])
        if dataset_name == "":
            dataset_name = item["name"].split("_")[1]
        performance_list.append([item[metric] for metric in metrics])

    custom_style = pygal.style.Style(background="transparent", opacity=".7", opacity_hover="1.0")
    bar_plot = pygal.Bar(style=custom_style, fill=True)
    bar_plot.title = f"Performance of models for {dataset_name}"
    bar_plot.x_labels = metrics
    for i, name in enumerate(names_list):
        bar_plot.add(name, performance_list[i])
    bar_plot_data = bar_plot.render_data_uri()
    return bar_plot_data


@app.route("/")
def front():
    if "username" in session:
        return redirect(url_for("home"))
    return render_template("login.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["username"] != "admin":
            error = "Invalid user"
        elif request.form["password"] != "admin":
            error = "Invalid password"
        else:
            session["username"] = request.form["username"]
            return redirect(url_for("front"))
    return render_template("login.html", error=error)


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("front"))


@app.route("/home")
def home():
    if "username" in session:
        username = session["username"]
        return render_template("home.html", user=username)
    return unauth()


@app.route("/selector")
def selector():
    if "username" in session:
        return render_template("selector.html")
    return unauth()


@app.route("/selector/upload", methods=["GET", "POST"])
def upload_data_file():
    if request.method == "POST" and "username" in session:
        uploaded_file = request.files["file"]
        destination = os.path.join(app.config["UPLOAD_FOLDER"], secure_filename(uploaded_file.filename))
        uploaded_file.save(destination)
        selected_model = api.train_model(destination)
        return render_template("selector_selected.html", message=selected_model)
    return abort(404)


@app.route("/predictor")
def predictor():
    if "username" in session:
        model_list = get_best_model()
        data_list = get_stored_data("test")
        return render_template("predictor.html", data_list=data_list, model_list=model_list)
    return unauth()


@app.route("/predictor/upload", methods=["GET", "POST"])
def upload_test_file():
    if request.method == "POST" and "username" in session:
        uploaded_file = request.files["file"]
        destination = os.path.join(app.config["TEST_FOLDER"], secure_filename(uploaded_file.filename))
        uploaded_file.save(destination)
        return redirect(url_for("predictor"))
    return abort(404)


@app.route("/predictor/results", methods=["GET", "POST"])
def predictor_submit():
    if request.method == "POST" and "username" in session:
        if request.form["data"] == "empty" or request.form["model"] == "empty":
            return redirect(url_for("predictor"))
        data = request.form["data"]
        model = request.form["model"]
        data_url = os.path.join(app.config["TEST_FOLDER"], data)
        best_model_dir = os.path.join(app.config["MODELS_FOLDER"], "best_model")
        model_url = os.path.join(best_model_dir, model)
        prediction = api.get_predictions(model_url, data_url)
        arr_pres = 0
        for value in prediction.values():
            if value == "present":
                arr_pres += 1
        pred_len = len(prediction)
        return render_template(
            "predictions.html",
            predictions=prediction,
            arr_present=arr_pres,
            prediction_length=pred_len,
        )
    return abort(404)


@app.route("/performance")
def performance():
    if "username" in session:
        model_list = get_best_model()
        return render_template("performance.html", model_list=model_list)
    return unauth()


@app.route("/performance/display", methods=["GET", "POST"])
def display_performance():
    if request.method == "POST" and "username" in session:
        if request.form["name"] == "empty":
            return redirect(url_for("performance"))
        file_name = request.form["name"].split(".")[0]
        performance_url = os.path.join(app.config["MODELS_FOLDER"], rf"performance/{file_name}.json")
        with open(performance_url, "r", encoding="utf-8") as json_file:
            item = json.load(json_file)
        performance_plot = plot_performance(item)
        model_list = get_best_model()
        return render_template(
            "performance_display.html",
            model_list=model_list,
            performance_plot=performance_plot,
        )
    return abort(404)


@app.route("/cross_performance")
def cross_performance():
    if "username" in session:
        model_list = get_stored_models()
        data_list = get_stored_data("data")
        return render_template("cross_performance.html", model_list=model_list, data_list=data_list)
    return abort(404)


@app.route("/cross_performance/display", methods=["GET", "POST"])
def cross_performance_display():
    if request.method == "POST" and "username" in session:
        dataset_dir = []
        model = request.form["model"]
        model_dir, model_name = ast.literal_eval(model)
        model_path = os.path.join(app.config["MODELS_FOLDER"], rf"models\{model_dir}\{model_name}")

        dataset_list = request.form.getlist("dataset")
        for dataset in dataset_list:
            dataset_dir.append(os.path.join(app.config["UPLOAD_FOLDER"], dataset))
        if len(dataset_dir) == 2:
            dataset1_path, dataset2_path = dataset_dir
        else:
            return abort(416)
        model_cross_performance = api.model_cross_performance_specific_model(model_path, dataset1_path, dataset2_path)
        cross_performance_plot = plot_performance(model_cross_performance, True)
        return render_template(
            "cross_performance_display.html",
            cross_performance_plot=cross_performance_plot,
        )
    return abort(404)


if __name__ == "__main__":
    app.run()
