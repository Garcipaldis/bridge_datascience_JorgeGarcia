import os
import sys
import pandas as pd
from flask import Flask, request
import argparse

root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root)

from src.utils.folders_tb import Folders
from src.utils.apis_tb import FlaskFuncs

settings_file = root + os.sep + 'src' + os.sep + "utils" + os.sep + "settings_sql.json"
dfpath = root + os.sep + 'data' + os.sep + 'BASE.csv'
app = Flask(__name__)

df = pd.read_csv(dfpath)
funcs = FlaskFuncs(df, root, settings_file)

@app.route('/info', methods=['GET'])  # http://localhost:6060/info?token_id=B53814652
def give_id():
    x = request.args['token_id']
    if x == "B53814652":
        return funcs.give_json()
    else:
        return "Invalid Token ID"

@app.route('/predict', methods=['GET'])  # http://localhost:6060/predict?token_id=B53814652&model=Base_Quote_LSTM.h5&sentence=0
def predict():
    x = request.args['token_id']
    model = request.args['model']
    string = request.args['sentence']
    if string == '0':
        string = False
    if x == "B53814652":
        return funcs.get_predicction(model, string, temperature=0.3)
    else:
        return "Invalid Token ID"

@app.route('/insert-sql', methods=['GET'])  # http://localhost:6060/insert-sql?token_id=B53814652
def insert_mysql():
    x = request.args['token_id']
    if x == "B53814652":
        return funcs.insert_df_to_mysql()
    else:
        return "Invalid Token ID"


def main():
    print("---------STARTING PROCESS---------")
    print(__file__)
    
    # Get the settings fullpath
    # \\ --> WINDOWS
    # / --> UNIX
    # Para ambos: os.sep
    settings_file = os.path.dirname(__file__) + os.sep + "settings.json"
    print(settings_file)
    # Load json from file
    json_readed = Folders.read_json(settings_file)
    
    # Load variables from jsons
    SERVER_RUNNING = json_readed["server_running"]
    print("SERVER_RUNNING", SERVER_RUNNING)
    if SERVER_RUNNING:
        DEBUG = json_readed["debug"]
        HOST = json_readed["host"]
        PORT_NUM = json_readed["port"]
        app.run(debug=DEBUG, host=HOST, port=PORT_NUM)
    else:
        print("Server settings.json doesn't allow to start server. " + 
            "Please, allow it to run it.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-x", "--x", type=str, help="password")
    args = vars(parser.parse_args())
    x = args['x']
    if x != 'Jorge':
        print('Wrong password')
    else:
        main()