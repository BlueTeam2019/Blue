import os
from flask import Flask
from model import Model
from model_builder import ModelBuilder

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
    model = ModelBuilder().build()

    app.run(host='0.0.0.0', debug=True)