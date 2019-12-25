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
        data = request.get_json()
        is_successful = provider_model.provider_model.register_truck(data)
    except:
        print("Error")

    if is_successful:
        return "OK",200
    else:
        return "Invalid Request", 400

@app.route('/truck/<id>', methods=["PUT"])
def update_truck_provider(id):
    print(id)
    is_successful = False
    try:
        data = request.get_json()
        print(data)
        is_successful = provider_model.provider_model.update_truck_provider(data,id)
    except:
        print("Error")

    if is_successful:
        return "OK",200
    else:
        return "Invalid Request", 400


app.run(host='0.0.0.0', debug=True)