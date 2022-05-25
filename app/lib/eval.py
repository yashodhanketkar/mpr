"""eval.py

This is automated performance evaluation module. It takes the data from
models module and ranks the models based on performances. It returns
name of best model for the selected database.
"""


import copy
import json

from sklearn import metrics


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


def assign_metrics_rank(key, pred_list, rank):
    """Assigns ranks by sorting metric performance.

    Args:
        key (str): The name of metric to be ranked
        pred_list (list): The list of dictionaries consist of model data
        rank (list): The list of ranks
    """
    rank_list = []
    val_list = [item[key] for item in pred_list]
    sort_list = sorted(val_list, reverse=True)
    for val_item in val_list:
        i = 0
        for sort_item in sort_list:
            i += 1
            if val_item == sort_item:
                rank_list.append(i)
    for i, rank_item in enumerate(rank_list):
        rank[i][key] = rank_item


def get_metrics_rank(file_name, prediction_list, y_target):
    """Get list of metrics and create list of ranks based on metrics
    performance.

    Args:
        file_name (str): Name of the dataset
        prediction_list (list): The list of tuples of model data
        y_target (series): The pandas series of actual values

    Returns:
        ranks (list): The list of dictionary of models name and metrics
                      rank
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
    ranks = copy.deepcopy(models)
    for item in ["accuracy", "f1", "precision", "recall", "roc", "pred_time"]:
        assign_metrics_rank(item, models, ranks)
    return ranks


def get_score(metrics_rank, weights=None):
    """This function ets the list of dictionary of model name and
    metrics rank to score model by returning weighted sum of metrics.

    Args:
        metrics_rank (list): The list of dictionary of model name and
                             metrics rank.
        weights (list): The dictionary of weights provided by user. If
                        not provided use default values.

    Returns:
        weighted_score (list): The list of dictionary of model name and
                               total score.

    """
    if weights is None:
        with open(r"app\lib\parameters\default_param.json", "r") as json_file:
            weights = json.load(json_file)

    weighted_score = []
    for item in metrics_rank:
        weighted_score.append(
            {
                "name": item["name"],
                "score": item["accuracy"] * weights["accuracy"]
                + item["f1"] * weights["f1"]
                + item["precision"] * weights["precision"]
                + item["recall"] * weights["recall"]
                + item["roc"] * weights["roc"]
                + item["pred_time"] * weights["pred_time"],
            }
        )
    return weighted_score


def get_selected_model(file_name, prediction_list, y_target, weights=None):
    """This model selects best model according to scores and returns
    name

    Args:
        file_name (str): The name of dataset
        prediction_list (list): The list of dictionary of model name and
            metrics
        y_target (array): The array of actual label of testing data
        weights (dict): The dictionary of weights provided by user

    Returns:
        best_model_name (str): The name of best of selected based on
                               score

    """
    metrics_rank = get_metrics_rank(file_name, prediction_list, y_target)
    model_score = get_score(metrics_rank, weights)
    selected_model = sorted(model_score, key=lambda x: x["score"])
    best_model = selected_model[0]
    best_model_name = get_best_model_name(best_model)
    return best_model_name
