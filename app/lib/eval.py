"""eval.py

This is automated performance evaluation module. It takes the data from
models module and ranks the models based on performances. It returns
name of best model for the selected database.
"""


import json

from sklearn import metrics

from .weightage import default_weights, get_weightage


def get_best_model_name(best_model):
    """Get name of best model

    Args:
        best_model (model_object): The model

    Returns:
        best_model_name (str): The name of model
    """
    best_model_complete_name = best_model["name"]
    best_model_name = best_model_complete_name.split("_")[0]
    return best_model_name


def get_metrics_values(file_name, prediction_list, y_target):
    """Get list of metrics and create list of values based on metrics
    performance.

    Args:
        file_name (str): Name of the dataset
        prediction_list (list): The list of tuples of model data
        y_target (series): The pandas series of actual values

    Returns:
        models (list): The list of dictionary of models name and metrics
        values
    """
    models = []
    for item in prediction_list:
        models.append(
            {
                "name": item[0] + f"_{file_name}",
                "accuracy": metrics.accuracy_score(y_target, item[1]),
                "f1": metrics.f1_score(y_target, item[1]),
                "precision": metrics.precision_score(y_target, item[1]),
                "recall": metrics.recall_score(y_target, item[1]),
                "roc": metrics.roc_auc_score(y_target, item[1]),
                "pred_time": item[2] / len(y_target),
            }
        )

    with open(rf"model\performance\{file_name}.json", "w") as json_file:
        json.dump(models, json_file)

    for model in models:
        for _attr, _val in model.items():
            if _attr == "name":
                continue
            model[_attr] = round(_val, 6)

    return models


def get_score(metrics_value, weights=None):
    """This function ets the list of dictionary of model name and
    metrics values to score model by returning weighted sum of metrics.

    Args:
        metrics_values (list): The list of dictionary of model name and
        metrics values.
        weights (list): The dictionary of weights provided by user. If
        not provided use default values.

    Returns:
        weighted_score (list): The list of dictionary of model name and
        total score.

    """
    if not weights:
        weights = default_weights()

    weightage = get_weightage(weights)
    weighted_score = []

    for item in metrics_value:
        weighted_score.append(
            {
                "name": item["name"],
                "score": item["accuracy"] * weightage["accuracy"]
                + item["f1"] * weightage["f1"]
                + item["precision"] * weightage["precision"]
                + item["recall"] * weightage["recall"]
                + item["roc"] * weightage["roc"]
                - item["pred_time"] * (weightage["pred_time"] ** 2),
            }
        )

    return weighted_score


def get_selected_model(file_name, prediction_list, y_target, weights=None):
    """This model selects best model according to scores and returns
    name

    Args:
        file_name (str): The name of dataset
        prediction_list (list): The list of dictionary of model name
        and metrics
        y_target (array): The array of actual label of testing data
        weights (dict): The dictionary of weights provided by user

    Returns:
        best_model_name (str): The name of best of selected based on
        score

    """
    metrics_values = get_metrics_values(file_name, prediction_list, y_target)
    model_score = get_score(metrics_values, weights)
    selected_model = sorted(model_score, key=lambda x: x["score"])
    best_model = selected_model[-1]
    best_model_name = get_best_model_name(best_model)
    return best_model_name
