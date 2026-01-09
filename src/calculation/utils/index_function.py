import pandas as pd

def index_calculation(*args: pd.Series) -> pd.Series:
    """
    Calculates the mean index for any number of standardized variables.
    
    :param args: Multiple pandas Series (should be standardized)
    :return: A Series containing the calculated index
    """
    # 1. Combine all input Series into a single DataFrame
    # 2. Calculate the mean across the columns (axis=1)
    # 3. Round the result
    
    df = pd.concat(args, axis='columns')
    index_series = df.mean(axis='columns').round(2)
    
    return index_series