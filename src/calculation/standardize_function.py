import pandas as pd

def z_calculation(data:pd.Series, mean, std) -> list:
    return_lst = []

    for x in data:
        return_lst.append((x-mean)/std)
        
    return return_lst
