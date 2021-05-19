from flask import Flask, flash, request, render_template, redirect, url_for
import pandas as pd
import os
import json

UPLOAD_FOLDER = os.sep + "static" + os.sep
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'hellohello'



options = {"Genre_list":["hola", "adios"],
"Platform_list":[1,2,3,4,5,6],
"Publisher_list":['Clara', 'Borja', 'Gabriel']}

@app.route("/")
def home():
    return render_template("upload.html", 
                        Genre_list = options["Genre_list"],
                        Platform_list= options["Platform_list"], 
                        Publisher_list= options["Publisher_list"])
    
@app.route("/upload_form", methods = ['POST', 'GET'])
def upload_form():
    if request.method == 'POST':
        genre_res = request.form['Genre']
        platform_res= request.form['Platform']
        publisher_res = request.form['Publisher']
        all_returned = str(genre_res) + str(platform_res) + str(publisher_res)
        return json.dumps({"genre": genre_res,
                            "platform": platform_res,
                            "publisher": publisher_res,
                            "all_returned": all_returned})

if __name__ == '__main__':
    # host='127.0.0.1' --> No permite recibir llamadas desde el exterior
    # host='0.0.0.0' --> Permite recibir llamadas desde el exterior
    # si 0.0.0.0 no funciona externamente desde la IP privada de tu PC
    # es que tu ordenador o del dispositivo desde el que se accede 
    # tiene bloqueada la conexión (antivirus / firewall)
    app.run(host='0.0.0.0',port=os.getenv("PORT", 1991), debug=True)