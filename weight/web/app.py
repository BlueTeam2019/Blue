from flask import Flask, request
import models

# flaskPort=5000
# from time import gmtime, strftime     taken from older file
# import time   taken from older file
app = Flask(__name__)

@app.route("/health", methods=['GET'])
def health():
    # print("HELLO from APP!")
    if models.checkalive():
        return "OK", 200
    else:
        return "BAD", 500 

app.run()