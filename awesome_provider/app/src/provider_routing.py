from flask import Flask, request
import provider_model
app = Flask(__name__)

@app.route('/health', methods=["GET"])
def CheckHealth():
    isAlive = provider_model.CheckHealth()
    if isAlive:
        return "OK", 200
    else:
        return "Internal Error", 500 
app.run(host='0.0.0.0',debug=True)
