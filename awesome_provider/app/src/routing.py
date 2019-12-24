from flask import Flask, request
from model import Model
import os
import sys

from query_helper import QueryHelper

app = Flask(__name__)


@app.route('/health', methods=["GET"])
def check_health():
    is_alive = model.check_health()
    if is_alive:
        return "OK", 200
    else:
        return "Internal Error", 500


if __name__ == '__main__':
    dbUrl = os.environ['DB_URL']
    dbPass = os.environ['DB_USR']
    dbUser = os.environ['DB_PASS']
    dbName = os.environ['DB_NAME']
    dbPort = os.environ['DB_PORT']
    qHelper = QueryHelper(dbUrl, dbUser, dbPass, dbName, dbPort)
    model = Model(qHelper)

    app.run(host='0.0.0.0', debug=True)
