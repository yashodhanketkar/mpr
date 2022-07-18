"""models.py

This model creates, trains, and tests the models. The data obtained
during testing is saved to the list. This list and target values are
returned.
"""


import datetime
import os
import pickle

import pandas as pd
from sklearn.model_selection import train_test_split

from .data_formatter import xy_generator


def make_models(spec=None):
    """This function makes the models

    Returns:
        models (list): The list of tuple of model name and model
        spec (list): The list of tuple of model provided by user
    """
    if spec:
        return spec

    with open(r"app\lib\parameters\default_models.sav", "rb") as model_file:
        models = pickle.load(model_file)

    return models


def run_classifier(model, x_train, y_train, x_test, temp_path):
    """This function run trains the model and test them

    Args:
        model (list): The list of tuple of model name and model
        x_train (dataframe): The training data
        y_train (series): Labels for training data
        x_test (dataframe): The testing data
        temp_path (str): The path to save models

    Returns:
        Name (str): The name of model
        y_pred (array): Predicted values from test data
        test_time_ms (time): Amount of time requried in miliseconds to
        get predictions from test data
    """
    name, clf = model
    clf.fit(x_train, y_train)
    start_time = datetime.datetime.now()
    y_pred = clf.predict(x_test)
    end_time = datetime.datetime.now()
    test_time = end_time - start_time
    with open(rf"{temp_path}\{name}.sav", "wb") as model_file:
        pickle.dump(clf, model_file)
    test_time_ms = test_time.total_seconds() * 1000
    return name, y_pred, test_time_ms


def run_model(data_path, temp_path, file_name):
    """This function split data into training and testing set.The
    function returns the prediction list and actual labels

    Args:
        data_path (str): The path to data set
        temp_path (str): The path to save models
        file_name (str): The name of dataset

    Returns:
        prediction_list (list): The list of model name, predictions
        array and testing time
        y_test_array (array): The array of label for test data

    """
    models_list = make_models()
    prediction_list = []
    data = pd.read_csv(data_path, header=None)
    x_value, y_value = xy_generator(data)
    x_train, x_test, y_train, y_test = train_test_split(x_value, y_value, test_size=0.25, random_state=42)
    dump_path = os.path.join(temp_path, rf"models\{file_name}")
    for model in models_list:
        prediction_list.append(run_classifier(model, x_train, y_train, x_test, dump_path))
    y_test_array = y_test.to_numpy()
    return prediction_list, y_test_array
