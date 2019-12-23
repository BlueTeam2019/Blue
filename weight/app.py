from flask import Flask, request
import mysql.connector
import models   # importing the methods from models.py

app = Flask(__name__)

@app.route("/", methods=['GET'])
def hello():
    return "HOME is where ♥Heart is❤❤❤"



@app.route("/health", methods=['GET'])
def health():
    if models.checkalive():
        return "I AM BATMAN ", 200
    else:
        return "BAD", 500 

@app.route("/batch-weight", methods=['POST'])
def handleFileUpload():
    # models.batch_up()

    msg = 'failed to upload image'

    if 'image' in request.files:

        photo = request.files['image']

        if photo.filename != '':

            photo.save(os.path.join('.', photo.filename))
            msg = 'image uploaded successfully'

    return msg


app.run(host="0.0.0.0",port=8082, debug=True)
