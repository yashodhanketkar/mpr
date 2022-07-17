"""selection.py

This module runs the selection process. It takes data from user and
provide it to models and eval module. This module creates directories
and saves the best model for selected database.
"""


import os
import shutil

from datetime import datetime

from .data_formatter import name_generator
from .eval import get_selected_model
from .models import run_model

# def name_generator(file_path):
#     """This function produces file name from file path provided by user

#     Args:
#         file_path (str): File path provided by user

#     Returns:
#         name_str (str): Name of file generated form file path
#     """
#     name = file_path.split("\\")[-1].split(".")[0]
#     name_str = f"{name}"
#     return name_str


def make_directories(file_name):
    """This function makes directories to store models

    Returns:
        None
    """
    cwd = os.getcwd()
    for path in [
        rf"model\models\{file_name}",
        r"model\best_model",
        r"model\performance",
        r"model\cross_performance",
    ]:
        new_dir = os.path.join(cwd, rf"{path}")
        if not os.path.exists(new_dir):
            os.makedirs(new_dir)
        if "~" in new_dir:
            os.system(f"attrib +h {new_dir}")


def save_model(name, model_path, file_name):
    """This function moves the best selected model and store it into
    appropriate directory.

    Args:
        name (str): Name of selected model
        model_path (str): The directory where models are stored
        file_name (str): Name of dataset

    Returns:
        None
    """
    model_temp_path = os.path.join(model_path, rf"models\{file_name}")
    model_save_path = os.path.join(model_path, r"best_model")
    shutil.copy(
        os.path.join(model_temp_path, rf"{name}.sav"),
        os.path.join(model_save_path, rf"{file_name}.sav"),
    )


def get_model(data_path=None, weights=None):
    """This module get path for data and model storage and use them to
    select best model. This function saves the selected model.

    Args:
        data_path (string): The path of database
        weights (dict): Weights provided by user

    Returns:
        selected_model_name, file_name (str)
    """
    if data_path is None:
        raise ValueError
    _, file_name = name_generator(data_path)
    make_directories(file_name)
    model_path = os.path.join(os.getcwd(), "model")
    prediction_list, y_test = run_model(data_path, model_path, file_name)
    selected_model_name = get_selected_model(file_name, prediction_list, y_test, weights)
    save_model(selected_model_name, model_path, file_name)
    return selected_model_name, file_name


if __name__ == "__main__":
    get_model()
