"""api.py

This is API for wbmss
"""


import json
import os
from collections.abc import Callable

from .lib import get_model, get_prediction, test_against_database, test_all_models


def get_json_data(file_relative_path):
    """Returns data obtained from file path

    Args:
        file_relative_path (str): The path provided by user/application

    Returns:
        data (json load): Returns data
    """
    file_dir = os.path.join(os.getcwd(), file_relative_path)
    with open(file_dir, encoding="utf-8") as json_file:
        data = json.load(json_file)
    return data


def get_model_paths(dataset_name):
    """Returns path of models generated from certain dataset

    Args:
        dataset_name (str): Name of dataset

    Returns:
        model_paths (path): Path of models
    """
    dir_path = os.path.join(os.getcwd(), rf"model\{dataset_name}")
    fitted_model_names = next(os.walk(dir_path))[2]
    model_paths = [os.path.join(dir_path, model_name) for model_name in fitted_model_names]
    return model_paths


def train_model(data_path: str, weights: dict) -> tuple:
    return get_model(data_path, weights)


def get_predictions(model_path: str, data_path: str) -> dict:
    return get_prediction(data_path, model_path)


def model_cross_performance_specific_model(model_path: str, data_1_path: str, data_2_path: str) -> tuple:
    return test_against_database(model_path, data_1_path, data_2_path)


def model_cross_performance_all_models(dataset_name: str, data_1_path: str, data_2_path: str) -> None:
    model_paths = get_model_paths(dataset_name)
    test_all_models(model_paths, data_1_path, data_2_path)


def get_model_performance(dataset_performance: str) -> list:
    """Returns model performance

    Args:
        dataset_performance (str): Name of dataset json file

    Returns:
        performance (list): Performance metrics obtained from json file
    """
    file_relative_path = rf"model\performance\{dataset_performance}.json"
    performance = get_json_data(file_relative_path)
    return performance


def get_cross_performance(dataset_performance: str) -> list:
    """Returns cross-performance of model

    Args:
        dataset_performance (str): Name of dataset json file

    Returns:
        performance (list): Cross performance metrics obtained from json
                            file
    """
    file_relative_path = rf"model\cross_performance\{dataset_performance}.json"
    performance = get_json_data(file_relative_path)
    return performance


COMMANDS_DICT = {
    "train_model": train_model,
    "get_predictions": get_predictions,
    "model_cross_performance_specific_model": model_cross_performance_specific_model,
    "model_cross_performance_all_models": model_cross_performance_all_models,
    "get_model_performance": get_model_performance,
    "get_cross_performance": get_cross_performance,
}


def ammts_commands(param: str) -> Callable:
    if param not in COMMANDS_DICT.keys():
        raise NameError
    return COMMANDS_DICT[param]
