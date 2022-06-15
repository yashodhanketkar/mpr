"""update_models.py

This module generates/updates the default models. The module packs the
model in pickle file for future use.
"""


import pickle

from sklearn import ensemble, neighbors, neural_network, svm, tree


def gen_model():
    """This function makes the models

    Returns:
        models (list): The list of tuple of model name and model
    """
    models = []

    knn_clf = neighbors.KNeighborsClassifier(n_neighbors=3)
    models.append(("KNN", knn_clf))

    dt_clf = tree.DecisionTreeClassifier(criterion="entropy", random_state=15)
    models.append(("DT", dt_clf))

    mlp_clf = neural_network.MLPClassifier(
        hidden_layer_sizes=(32, 32, 16),
        batch_size=32,
        beta_1=0.6,
        beta_2=0.5,
        epsilon=1e-4,
    )
    models.append(("MLP", mlp_clf))

    rf_clf = ensemble.RandomForestClassifier(n_estimators=200, criterion="entropy", verbose=0.1, n_jobs=-1)
    models.append(("RF", rf_clf))

    svm_clf = svm.SVC(kernel="rbf", C=10, gamma="scale", tol=1e-12, break_ties=True, random_state=15)
    models.append(("SVM", svm_clf))

    return models


def pack_models(models):
    """This function packs the model into object file for quick access

    Args:
        models (list): The list of tuple of model name and model

    Returns:
        None
    """
    models_list = models
    with open(r"app\lib\parameters\default_models.sav", "wb") as model_file:
        pickle.dump(models_list, model_file)


if __name__ == "__main__":
    pack_models(gen_model())
