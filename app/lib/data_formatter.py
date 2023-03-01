import pandas as pd


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


def name_generator(file_path, _crossref=True):
    """Generates directory path and name of classifier from file path
    provided by user

    Args:
        file_path (str): File path provider by user

    Returns:
        dir_name (str): Name of directory of classifier
        clf_name (str): Name of classifier
    """
    clf_name = file_path.split("\\")[-1].split(".")[0]
    # if not _crossref:
    #     return clf_name
    dir_name = file_path.split("\\")[-2]
    return dir_name, clf_name


def xy_generator(data):
    """Generates the x and y value

    longdesc

    Args:
        data (dataframe): Pandas dataframe values

    Returns:
        x_value (dataframe): X values, the trainig values
        y_value (series): Y values, the labels for training value
    """
    label_index = len(data.columns) - 1
    x_value, y_value = data.iloc[:, :-1].copy(), data[label_index].copy()
    y_value = convert_to_dual_class(y_value)
    return x_value, y_value
