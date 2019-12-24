from flask import Flask, request
from model import Model
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
    dbUrl = sys.argv[1]
    dbPass = sys.argv[2]
    dbUser = sys.argv[3]
    dbName = sys.argv[4]
    dbPort = sys.argv[5]
    qHelper = QueryHelper(dbUrl, dbUser, dbPass, dbName, dbPort)
    model = Model(qHelper)

    app.run(host='0.0.0.0', debug=False)
