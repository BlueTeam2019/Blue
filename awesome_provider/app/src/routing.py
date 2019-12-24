import os
from flask import Flask, request
from model import Model


from query_helper import QueryHelper

app = Flask(__name__)


@app.route('/health', methods=["GET"])
def check_health():
    if model.check_health():
        return "OK", 200
    return "Internal Error", 500


if __name__ == '__main__':
    db_url = os.environ['DB_URL']
    db_user = os.environ['DB_USR']
    db_pass = os.environ['DB_PASS']
    db_name = os.environ['DB_NAME']
    db_port = int(os.environ['DB_PORT'])
    do_debug = os.environ.get('DEBUG', False)
    query_helper = QueryHelper(db_url, db_user, db_pass, db_name, db_port)
    model = Model(query_helper)

    app.run(host='0.0.0.0', debug=bool(do_debug))
