"""helper.py

This modules servers other modules by providing few common functions.
"""
import os

import pygal
from flask import abort, current_app, send_file

from app.lib.cross_model_test import test_all_models
# from .api import model_cross_performance_all_models


model_names = {
    "DT": "Decision Tree",
    "KNN": "K-Nearest Neighbours",
    "RF": "Random Forest",
    "MLP": "Multilayer Perceptron",
    "SVM": "Support Vector Machine",
}


def dir_listing(abs_path):
    """This function returns sub-directories/files based on recieved
    path

    Args:
        abs_path (path): Path sent by user

    Returns:
        files (path): Path to files or sub-directories
    """
    if not os.path.exists(abs_path):
        print("path does not exist")
        return abort(404)
    if os.path.isfile(abs_path):
        print("path exist")
        return send_file(abs_path)
    files = os.listdir(abs_path)
    return files


def get_stored_models():
    """This function returns all models generated from multiple datasets

    Returns:
        model_list (list): List of all models
    """
    model_list = []
    abs_path = os.path.join(current_app.config["MODELS_FOLDER"], "models")
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
    abs_path = os.path.join(current_app.config["MODELS_FOLDER"], "best_model")
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
    up_dir = os.path.join(current_app.config["APP_DIR"], "static")
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
    if is_cross_performance:
        metrics = ["accuracy", "f1", "precision", "recall", "roc"]
        dataset_name_index, type_index = (0, 2)
    else:
        metrics = ["accuracy", "f1", "precision", "recall", "roc", "pred_time"]
        dataset_name_index, type_index = (1, 0)
    for item in data:
        names_list.append(item["name"].split("_")[type_index])
        if dataset_name == "":
            dataset_name = item["name"].split("_")[dataset_name_index]
            if is_cross_performance:
                model = item["name"].split("_")[1]
        performance_list.append([item[metric] for metric in metrics])

    custom_style = pygal.style.Style(
        background="transparent", opacity=".7", opacity_hover="1.0", title_font_size=25
    )
    bar_plot = pygal.Bar(style=custom_style, fill=True)
    if is_cross_performance:
        bar_plot.title = (
            f"Performance of {model_names[model]} model trained on {dataset_name}"
        )
    else:
        bar_plot.title = f"Performance of models for {dataset_name}"
    bar_plot.x_labels = metrics
    for i, name in enumerate(names_list):
        bar_plot.add(name, performance_list[i])
    bar_plot_data = bar_plot.render_data_uri()
    return bar_plot_data


def save_cross_performance_data():
    data_dir = [
        os.path.join(current_app.config["UPLOAD_FOLDER"], data_path)
        for data_path in get_stored_data("data")
    ]
    model_dir = [
        os.path.join(current_app.config["MODELS_FOLDER"], rf'best_model\{model_path}')
        for model_path in get_best_model()
    ]
    test_all_models(model_dir, data_dir)
