import os
import pandas as pd

root_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

def give_json(filepath=f'{root_path}/data/MAIN_DATASET.csv'):
    df = pd.read_csv(filepath)
    return df.to_json()

if __name__ == '__main__':
    root_path = os.path.dirname(os.path.dirname(__file__))
    filepath = f'{root_path}/api/static/MAIN_DATASET.csv'
    give_json(filepath=filepath)