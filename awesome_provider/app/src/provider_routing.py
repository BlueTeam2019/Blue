from flask import Flask, request
from provider_model import Model
import sys

from queryHelper import QueryHelper

app = Flask(__name__)
model = None

@app.route('/health', methods=["GET"])
def CheckHealth():
    print("in route")
    isAlive = model.check_health()
    if isAlive:
        return "OK", 200
    else:
        return "Internal Error", 500


if __name__ == '__main__':
    dbUrl = sys.argv[1]
    dbPass = sys.argv[2]
    dbUser = sys.argv[3]
    dbName = sys.argv[4]
    dbPort = sys.argv[5]
    qHelper = QueryHelper(dbUrl, dbUser, dbPass, dbName, dbPort)
    model = Model(qHelper)

    app.run(host='0.0.0.0', debug=True)