"""cross_model_test.py

This module test-
    1) model performance against different dataset
    2) models performance against dataset
"""


import json
import os
import pickle
import time

import pandas as pd
from sklearn import metrics

from .data_formatter import convert_to_dual_class, name_generator


def prediction_performance(model_name, data_name, model_clf, data, y_target):
    """This function returns performance of models in form of dictionary
    object.

    Args:
        model_name (str): Name of model to be evaluated
        data_name (str): Name of dataset used for evaluation
        model_clf (clf): Classifier object
        data (dataframe): Dataset used for evaluation
        y_target (series): Expected/True values

    Returns:
        performance_metrics (dict): Performance of model
    """
    start_time = time.perf_counter()
    predictions = model_clf.predict(data)
    end_time = time.perf_counter()
    pred_time = end_time - start_time
    model_data = [model_name, predictions]
    performance_metrics = {
        "name": f"{model_data[0]}_{data_name}",
        "accuracy": metrics.accuracy_score(y_target, model_data[1]),
        "f1": metrics.f1_score(y_target, model_data[1]),
        "precision": metrics.precision_score(y_target, model_data[1]),
        "recall": metrics.recall_score(y_target, model_data[1]),
        "roc": metrics.roc_auc_score(y_target, model_data[1]),
        "pred_time": pred_time,
    }
    return performance_metrics


def test_against_database(model_path, database_1, database_2):
    """This function test model against multiple dataset and returns
    performance

    Args:
        model_path (path): Path of model provided by user
        database_1, database_2 (path): Path of datasets provided by user

    Returns:
        performance_results (tuple): The performance of model against
                                     provided datasets
    """
    performance_status = []
    data_1_name = name_generator(database_1)[1]
    data_1 = pd.read_csv(database_1, header=None)
    x_data_1, y_data_1 = data_1.iloc[:, :-1].copy(), data_1[187].copy()
    y_data_1 = convert_to_dual_class(y_data_1)
    data_2_name = name_generator(database_2)[1]
    data_2 = pd.read_csv(database_2, header=None)
    x_data_2, y_data_2 = data_2.iloc[:, :-1].copy(), data_2[187].copy()
    y_data_2 = convert_to_dual_class(y_data_2)
    model_name = "_".join(name_generator(model_path))
    with open(model_path, "rb") as model_file:
        model_clf = pickle.load(model_file)
    for x, y, data_name in (
        (x_data_1, y_data_1, data_1_name),
        (x_data_2, y_data_2, data_2_name),
    ):
        performance_status.append(prediction_performance(model_name, data_name, model_clf, x, y))
    performance_result = tuple(performance_status)
    return performance_result


def test_all_models(model_paths, database_1, database_2):
    """This function test all models against multiple dataset and save
    performance

    Args:
        model_paths (path): Path of directory where models are stored
        database_1, database_2 (path): Path of datasets provided by user

    Returns:
        None
    """
    model_performance = []
    for model_path in model_paths:
        model_performance.append(test_against_database(model_path, database_1, database_2))
    name = name_generator(model_paths)[0]
    cross_performance_save_dir = os.path.join(os.getcwd(), rf"model\cross_performance\{name}.json")
    with open(cross_performance_save_dir, "w") as json_file:
        json.dump(model_performance, json_file)
