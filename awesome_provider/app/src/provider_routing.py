from flask import Flask, request
from provider_model import provider_model
import sys

app = Flask(__name__)
#model = None

@app.route('/health', methods=["GET"])
def CheckHealth():
    print("in route")
    isAlive = provider_model.CheckHealth()
    if isAlive:
        return "OK", 200
    else:
        return "Internal Error", 500

@app.route('/provider', methods=["POST"])
def PostProvider():
    data= request.json
    result=provider_model.createProvider(data["name"])
    if result == 0 :
        return "The name is exist ,Choose another one", 404
    return f"{data['name']}"


@app.route('/provider/<int:id>', methods=["PUT"])
def PutProvider(id):
    print("YOHO")
    data= request.json
    result=provider_model.updateProvider(id,data["name"])
    if result == 0 :
        return "Wrong id", 404
    return "put ok" ,200

# @app.route('/put/<int:id>', methods=["PUT"])
# def Check(id):
#     return "put" ,200


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8080)          