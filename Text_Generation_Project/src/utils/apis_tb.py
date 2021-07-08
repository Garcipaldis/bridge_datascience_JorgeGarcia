import pandas as pd
import os, sys
from tensorflow import keras

from models import CharacterPreprocessor

root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root)

class FlaskFuncs(CharacterPreprocessor):

    def __init__(self, df):
        CharacterPreprocessor.__init__(self, df)
        self.models = self.get_models()

    def get_predicction(self, model, string, mode='base', quote_len=40, temperature=1):
        
        input_string = string[:quote_len].lower()
        model = self.models[model]

        if mode == 'base':
            self.preprocess()
            return self.generate(model, option=1, quote_len=quote_len, sentence=input_string, temperature=temperature)
        elif mode == 'gan':
            self.preprocess_type2()
            return self.generate(model, option=2, quote_len=quote_len, sentence=input_string, temperature=temperature)

    def get_models(self):
        path = root + os.sep + 'models'
        files = os.listdir(path)

        models = {name:keras.models.load_model(path + os.sep + name) for name in files}

        return models


if __name__ == '__main__':
    df = pd.read_csv(root + os.sep + 'data' + os.sep + 'BASE.csv')
    FF = FlaskFuncs(df)
    string = 'Certainty of death. Small chance of success.'
    print(FF.get_predicction('Base_Quote_Generator.h5', string, temperature=0.2))