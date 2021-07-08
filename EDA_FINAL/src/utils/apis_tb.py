import pandas as pd

class JsonClass:

    @staticmethod
    def give_json(filepath):
        """ Reads a csv file with pandas and returns a json.
            - Args:
                - filepath: Path where the csv file is located.
        """
        df = pd.read_csv(filepath)
        return df.to_json()