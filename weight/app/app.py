from flask import Flask, request
import models

# from time import gmtime, strftime     taken from older file
# import time   taken from older file
app = Flask(__name__)

@app.route("/health", methods=['GET'])
def health():
    print("HELLO from APP!")
    if models.checkalive():
        return "OK", 200
    else:
        return "BAD", 500 

app.run(host="0.0.0.0", port=8082, debug=True)