import pandas as pd

def z_calculation(data:pd.Series, mean, std) -> pd.Series:
    """
    Function for calculating standardized values from a Series of values
    
    :param data: A Series of values used for calculating z
    :type data: pd.Series
    :param mean: Mean of Series
    :param std: Standard Deviation of Series
    :return: Complete Series of standardized values
    :rtype: pd.Series
    """
    return_lst = []

    for x in data:
        result = round(((x-mean)/std), 4)
        return_lst.append(result)

    return pd.Series(return_lst)
