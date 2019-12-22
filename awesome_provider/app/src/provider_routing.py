from flask import Flask, request
import provider_model
import sys

app = Flask(__name__)
data = None

@app.route('/health', methods=["GET"])
def CheckHealth():
    isAlive = provider_model.CheckHealth()
    if isAlive:
        return "OK", 200
    else:
        return "Internal Error", 500 


if __name__ == '__main__':
    dbUrl = app.varg[1]
    dbPass = app.varg[2]
    dbUser = app.varg[3]
    dbName = app.varg[4]

    data = provider_model(dbUrl, dbUser, dbPass, dbName)

    app.run(host='0.0.0.0',debug=True)

