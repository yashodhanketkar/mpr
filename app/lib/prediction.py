"""prediction.py

This module runs prediciton process. It takes data from user and returns
the results calculated from model.
"""


import pickle

import numpy as np
import pandas as pd
from .data_formatter import xy_generator


def make_prediction(data, model):
    """This function takes data and returns prediction from model.

    Args:
        data (data): The data taken from user/function
        model (sav): The model to predict the data

    Returns:
        result (bool): The boolean value based on prediciton result
    """
    pred = model.predict(data)
    result = pred > 0
    return result


def pred_formatter(predictions):
    """This function takes prediction results and returns appropriate
    statement

    Args:
        predictions (list): The list of predictions taken from function

    Returns:
        pred_dict (dict): The dictionary produced by evaluating
                          predictions
    """
    pred_dict = {}
    for index, prediction in enumerate(predictions):
        prediction_result = "present" if prediction else "absent"
        pred_dict[index] = prediction_result
    return pred_dict


def get_prediction(data_path=None, model_path=None):
    """This function takes data path and returns prediction results

    Args:
        data_path (str): The data path provided by user
        model_path (str): The model path provided by user

    Returns:
        prediction_dict (dict): The prediction result
    """
    if data_path is None:
        raise ValueError
    if model_path is None:
        raise ValueError
    data = pd.read_csv(data_path, header=None)
    x_value, _ = xy_generator(data)
    best_model = pickle.load(open(model_path, "rb"))
    pred_list = []
    for i in range(len(x_value)):
        arr = np.array(x_value.iloc[i]).reshape(1, -1)
        prediction = make_prediction(arr, best_model)
        pred_list.append(prediction)
    prediction_dict = pred_formatter(pred_list)
    return prediction_dict
