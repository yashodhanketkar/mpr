"""helper.py

This modules servers other modules by providing few common functions.
"""
import os

import pygal
from flask import abort, current_app, send_file


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
