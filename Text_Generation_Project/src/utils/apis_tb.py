import pandas as pd
import os, sys
from tensorflow import keras
from sqlalchemy import create_engine
import pymysql

root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root)

from src.utils.mining_data_tb import Preprocessor
from src.utils.folders_tb import Folders

settings_file = root + os.sep + 'src' + os.sep + "utils" + os.sep + "settings_sql.json"

class FlaskFuncs(Preprocessor, Folders):
    """Class designed to operate with the server.py API script."""

    def __init__(self, df, root, settings_file):
        Preprocessor.__init__(self, df)
        self.root = root
        self.settings_file = settings_file
        self.models = self.get_models()

        loaded_json = self.read_json(self.settings_file)

        self.IP_DNS = loaded_json["IP_DNS"]
        self.PORT = loaded_json["PORT"]
        self.USER = loaded_json["USER"]
        self.PASSWORD = loaded_json["PASSWORD"]
        self.BD_NAME = loaded_json["BD_NAME"]

        self.SQL_ALCHEMY = 'mysql+pymysql://' + self.USER + ':' + self.PASSWORD + '@' + self.IP_DNS + ':' + str(self.PORT) + '/' + self.BD_NAME

    def get_predicction(self, model, string=False, quote_len=40, temperature=1):
        """"Returns a prediction based on the selected model. Each model requires its predefined data preprocessing.
            - Args:
                - model: keras model loaded in self.models.
                - string: Input string. If false, the model predicts with a random input.
                - quote_len: Number of characters/words to show in output. Only affects LSTM models.
                - temperature: Sequence variance distortion. Recommended low values for character based models.
            - Returns:
                - Prediction
        """
        
        if model == '1_Base_Quote_LSTM.h5' or model == '3_Bidirectional_LSTM.h5':
            self.preprocess(option='character', mode='base')
            selection = self.models[model]
            return self.generate(selection, option='character', mode='base', 
                                quote_len=quote_len, sentence=string, temperature=temperature)

        elif model == '2_Word_Base_LSTM.h5':
            self.preprocess(option='word', mode='base', maxlen=5)
            selection = self.models[model]
            return self.generate(selection, option='word', mode='base', 
                                quote_len=quote_len, sentence=string, temperature=temperature)

        elif model == '4_Char_GAN.h5':
            self.preprocess(option='character', mode='gan')
            selection = self.models[model]
            return self.generate(selection, option='character', mode='gan', 
                                quote_len=quote_len, sentence=string, temperature=temperature)

        elif model == '5_Word_GAN.h5':
            self.preprocess(option='word', mode='gan', maxlen=5)
            selection = self.models[model]
            return self.generate(selection, option='word', mode='gan', 
                                quote_len=quote_len, sentence=string, temperature=temperature)

        else:
            return 'Input is not a valid model'

    def get_models(self):
        """Loads models from selected path into a list."""
        path = self.root + os.sep + 'models'
        files = os.listdir(path)

        models = {name:keras.models.load_model(path + os.sep + name) for name in files}

        return models

    def insert_df_to_mysql(self, input_df=None, option=1, table_name=''):
        """Inserts dataframe into MySQL server.
            - Args:
                - input_df: Desired dataframe to insert as a table. If None, the class attribute dataframe will be inserted.
                - option: 1 for inserting class attribute dataframe and 2 for using the input_df.
                - table_name: required if option 2 is selected."""

        engine = create_engine(self.SQL_ALCHEMY)
        if option == 1:
            df = self.data
            df.to_sql('jorge_garcia_navarro', engine, index=False, if_exists='replace')
        elif option == 2:
            df = input_df
            df.to_sql(table_name, engine, index=False, if_exists='replace')

        return 'Dataframe correctly inserted into MySQL Server.'

    def give_json(self):
        """ Reads a csv file with pandas and returns a json.
        """
        return self.data.to_json()

    def connect(self):
        # Open database connection
        self.db = pymysql.connect(host=self.IP_DNS,
                                user=self.USER, 
                                password=self.PASSWORD, 
                                database=self.BD_NAME, 
                                port=self.PORT)
        # prepare a cursor object using cursor() method
        self.cursor = self.db.cursor()
        print("Connected to MySQL server [" + self.BD_NAME + "]")
        return self.db

    def close(self):
        # disconnect from server
        self.db.close()
        print("Close connection with MySQL server [" + self.BD_NAME + "]")

    def execute_get_sql(self, sql):
        """SELECT"""
        results = None
        print("Executing:\n", sql)
        try:
            # Execute the SQL command
            self.cursor.execute(sql)
            # Fetch all the rows in a list of lists.
            results = self.cursor.fetchall()
        except Exception as error:
            print(error)
            print ("Error: unable to fetch data")
        
        return results

if __name__ == '__main__':
    df = pd.read_csv(root + os.sep + 'data' + os.sep + 'BASE.csv', index_col=0)
    FF = FlaskFuncs(df, root, settings_file)
    string = 'Certainty of death. Small chance of success.'
    print(FF.get_predicction('Base_Quote_LSTM.h5', string, temperature=0.2))
    FF.insert_df_to_mysql()