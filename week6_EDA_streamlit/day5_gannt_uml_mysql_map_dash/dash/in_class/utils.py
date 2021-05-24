import os, sys 

_dir = os.path.dirname
sep = os.sep
data_path = _dir(_dir(__file__)) + sep + "data" + sep + "googleplaystore.csv"

def change_m(x):
    if "M" in x:
        return x.replace("M", "000")
    else:
        return x

def change_dollar(x):
    if "$" in x:
        return x.replace("$", "000")
    elif "Everyone" in x:
        return 0
    else:
        return x