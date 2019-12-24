from flask import Flask, request
import provider_model
import sys

app = Flask(__name__)

@app.route('/health', methods=["GET"])
def CheckHealth():
    print("in route")
    isAlive = provider_model.provider_model.CheckHealth()
    if isAlive:
        return "OK", 200
    else:
        return "Internal Error", 500 

@app.route('/truck', methods=["POST"])
def register_truck():
    is_successful = False
    try:
        is_successful = provider_model.provider_model.register_truck(request.get_json())
    except:
        print("Error")

    if is_successful:
        return "OK",200
    else:
        return "Invalid Request", 400

app.run(host='0.0.0.0', debug=True)