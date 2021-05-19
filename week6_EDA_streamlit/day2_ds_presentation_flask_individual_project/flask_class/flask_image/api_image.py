from flask import Flask, flash, request, render_template, redirect, url_for
import pandas as pd
import os
import json

UPLOAD_FOLDER = os.sep + "static" + os.sep
app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'hellohello'

@app.route("/")
def home():
    return render_template("upload.html")

@app.route("/", methods = ['POST'])
def upload_image():
    file = request.files['file']
    if file:
        filename = file.filename
        path_to_save = os.path.dirname(__file__) + app.config['UPLOAD_FOLDER'] + filename
        file.save(path_to_save)
        print(path_to_save)
        flash(str(path_to_save))
        flash("Image successfully uploaded and displayed below")
        return render_template('upload.html', filename = filename)
    

@app.route('/shape', methods=["POST"])
def get_shape():
    request_file = request.files['data_file']
    if not request_file:
        return "No file"
    if ".csv" in str(request_file):
        data = pd.read_csv(request_file, error_bad_lines=False)
        rows = data.shape[0]
        columns = data.shape[1]
        return """
        <html>
            <body style="background-color: #d1bfff;">
                <h2>This CSV has {a} columns and {b} rows</h2>
            </body>
        </html>
    """.format(a=rows, b=columns)

@app.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for("static", filename = filename, code = 301))


if __name__ == '__main__':
    # host='127.0.0.1' --> No permite recibir llamadas desde el exterior
    # host='0.0.0.0' --> Permite recibir llamadas desde el exterior
    # si 0.0.0.0 no funciona externamente desde la IP privada de tu PC
    # es que tu ordenador o del dispositivo desde el que se accede 
    # tiene bloqueada la conexión (antivirus / firewall)
    app.run(host='0.0.0.0',port=os.getenv("PORT", 1991), debug=True)