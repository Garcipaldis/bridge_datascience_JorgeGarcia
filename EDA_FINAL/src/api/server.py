import os
import sys
from flask import Flask, request
import argparse

src_path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(src_path)

from utils.folders_tb import read_json
from utils.apis_tb import give_json

app = Flask(__name__)

@app.route('/info', methods=['GET'])  # http://192.168.0.241:6060/info?token_id=B53814652
def give_id():
    x = request.args['token_id']
    if x == "B53814652":
        return give_json()
    else:
        return "Invalid Token ID"


def main(x):
    if x != 8642:
        print('Wrong password')
        return False
    print("---------STARTING PROCESS---------")
    print(__file__)
    
    # Get the settings fullpath
    # \\ --> WINDOWS
    # / --> UNIX
    # Para ambos: os.sep
    settings_file = os.path.dirname(__file__) + os.sep + "settings.json"
    print(settings_file)
    # Load json from file
    json_readed = read_json(fullpath=settings_file)
    
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
    parser.add_argument("-x", "--x", type=int, help="password")
    args = vars(parser.parse_args())
    x = args['x']
    main(x)