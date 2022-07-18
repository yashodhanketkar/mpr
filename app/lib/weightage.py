"""weightage.py

This modules generates the weightage for the parameters. The weightage
is generated with consideration to the users parameter preference.
"""


def weight_gen(ranks=None):
    """Generate weightage from users ranking choice

    Args:
        ranks (list): List of ranking

    returns:
        weightage (list): List of weights generated
    """
    _seq = [1.0, 0.8, 0.6, 0.4, 0.2]

    if not ranks or not all(isinstance(_i, int) for _i in ranks) or sum(ranks) != 5:
        print("Corrupted ranks, returning default weightage.")
        return [0.6] * 5

    total = 0
    weightage = []

    for rank in ranks:
        _weightage = 0
        for _i in range(total, total + rank):
            _weightage += _seq[_i]
        weightage += [round(_weightage / rank, 1)] * (rank)
        total += rank

    return weightage


def counter(iter_object, _reverse=False, _get="v"):
    """Counter function to provide the count of items with respect to
    user choice. The items are sorted with respect to the input.

    Args:
        iter_object (iterable): Iterable item to count items.
        _reverse (boolean): Whether reverse order is needed.
        _get (str): v for count, k for items

    Returns:
        list: List of the counted item

    Raises:
        AttributeError: If _get contains invalid value.
    """

    def getError():
        raise AttributeError("Only 'k' and 'v' are allowed.")

    counted_dict_object = {}
    present = []

    for val in iter_object:
        if val not in present:
            present.append(val)
            counted_dict_object[val] = 1
            continue

        counted_dict_object[val] += 1

    return [
        val if _get == "v" else key if _get == "k" else getError()
        for key, val in sorted(counted_dict_object.items(), key=lambda item: item[0], reverse=_reverse)
    ]


def get_time_weightage(time_pref):
    """Returns the the weightage for the time

    Args:
        time_pref (dict_item): The time parameter value

    Returns:
        dict: Weightage for time parameter
    """
    match time_pref:
        case "slow":
            _w = 0.25
        case "fast":
            _w = 0.75
        case _:
            _w = 0.5

    return {"pred_time": _w}


def get_weightage(parameter_pref):
    """Returns weightage for parameters.

    Args:
        parameter_pref (dict): The dictionary contain user preference
        for parameters.

    Returns:
        weightage_perf (dict): The dictionary containing the generated
        weightage.
    """

    # Get time's weightage while seperating it from other five
    # parameters.
    time_weight = get_time_weightage(parameter_pref.pop("pred_time"))

    # Gets weightage for other five parameters
    raw_weightage = weight_gen(counter(parameter_pref.values()))

    # Indexing
    # 1. Compress weightage for indexing.
    # 2. Assigns index to the weightage.
    weightage_compressed = counter(raw_weightage, True, "k")
    weights_cor = {}
    for i, item in enumerate(set(parameter_pref.values())):
        weights_cor[item] = weightage_compressed[i]

    # Weightage assignment
    # 1. Assign weightage to the five parameters.
    # 2. Then add time weightage to final result.
    weightage_perf = {k: weights_cor[v] for k, v in parameter_pref.items()}
    weightage_perf.update(time_weight)

    return weightage_perf


def default_weights():
    """This function returns default weights.

    Returns:
        (dict): Dictionary of default weightage
    """
    return get_weightage(
        {
            "accuracy": 3,
            "f1": 3,
            "precision": 3,
            "recall": 3,
            "roc": 3,
            "pred_time": "normal",
        }
    )


def example():
    """Example of weightage"""
    weightage = default_weights()
    print(weightage)


if __name__ == "__main__":
    example()
