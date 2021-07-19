import os, sys
from flask import Flask
import json

SEP = os.sep
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ----------------------
# $$$$$$$ FLASK $$$$$$$$
# ----------------------

app = Flask(__name__)  # init

@app.route("/") 
def home():
    return "El flask"

# ----------------------
# $$$$$$$ MAIN $$$$$$$$
# ----------------------

def main():

    print("---------STARTING PROCESS---------")
    print(os.path.dirname(os.path.abspath(__file__)))
    
    # Get the settings fullpath
    settings_file = os.path.dirname(os.path.abspath(__file__)) + SEP + "settings.json"
    # Load json from file 
    with open(settings_file, "r") as json_file_readed:
        json_readed = json.load(json_file_readed)
    
    # Load variables from jsons
    SERVER_RUNNING = json_readed["server_running"]
    
    if SERVER_RUNNING:
        DEBUG = json_readed["debug"]
        HOST = json_readed["host"]
        PORT_NUM = json_readed["port"]
        app.run(debug=DEBUG, host=HOST, port=PORT_NUM)
    else:
        print("Server settings.json doesn't allow to start server. " + "Please, allow it to run it.")
            

main()