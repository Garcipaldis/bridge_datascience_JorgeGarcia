import pandas as pd

class JsonClass:

    @staticmethod
    def give_json(filepath):
        df = pd.read_csv(filepath)
        return df.to_json()
