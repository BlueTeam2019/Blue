from flask import Flask, request
import provider_model
import sys

app = Flask(__name__)
#model = None

@app.route('/health', methods=["GET"])
def CheckHealth():
    print("in route")
    isAlive = provider_model.provider_model.CheckHealth()
    if isAlive:
        return "OK", 200
    else:
        return "Internal Error", 500 


app.run(host='0.0.0.0')