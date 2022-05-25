"""models.py

This model creates, trains, and tests the models. The data obtained
during testing is saved to the list. This list and target values are
returned.
"""


import datetime
import os
import pickle

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier


def convert_to_dual_class(multiclass_value):
    """Convert multiclass problems to dualclass problems by processing
    target outputs

    Args:
        multiclass_value (data): Multiclass data
    Returns:
        dual_class_value (data): Converted dataset
    """

    # Convert multiclass values by converting valid non-zero values to 1.0
    # This results in only binary class with 0.0 and 1.0 values
    convert_value = multiclass_value.apply(lambda x: 0.0 if x == 0 else 1.0)
    dual_class_value = pd.Series(convert_value.tolist())
    return dual_class_value


def make_models():
    """This function makes the models

    Returns:
        models (list): The list of tuple of model name and model
    """
    models = []

    knn_clf = KNeighborsClassifier(n_neighbors=3)
    models.append(("KNN", knn_clf))

    # dt_clf = DecisionTreeClassifier(criterion="entropy", random_state=15)
    # models.append(("DT", dt_clf))

    # mlp_clf = MLPClassifier(
    #     hidden_layer_sizes=(32, 32, 16),
    #     batch_size=32,
    #     beta_1=0.6,
    #     beta_2=0.5,
    #     epsilon=1e-4,
    # )
    # models.append(("MLP", mlp_clf))

    # rf_clf = RandomForestClassifier(n_estimators=200, criterion="entropy", verbose=0.1, n_jobs=-1)
    # models.append(("RF", rf_clf))

    # svm_clf = SVC(kernel="rbf", C=10, gamma="scale", tol=1e-12, break_ties=True, random_state=15)
    # models.append(("SVM", svm_clf))
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
    x_value, y_value = data.iloc[:, :-1].copy(), data[187].copy()
    y_value = convert_to_dual_class(y_value)
    x_train, x_test, y_train, y_test = train_test_split(x_value, y_value, test_size=0.25, random_state=42)
    dump_path = os.path.join(temp_path, rf"models\{file_name}")
    for model in models_list:
        prediction_list.append(run_classifier(model, x_train, y_train, x_test, dump_path))
    y_test_array = y_test.to_numpy()
    return prediction_list, y_test_array
