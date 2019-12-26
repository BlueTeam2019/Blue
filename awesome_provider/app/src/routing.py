import os

import requests
from flask import Flask, request, send_file

from bill_helper import BillHelper
from model_builder import ModelBuilder
from routing_handler import validate_time_format

app = Flask(__name__)


@app.route('/health', methods=["GET"])
def check_health():
    if model.check_health():
        return "OK", 200
    return "Infernal error", 500

@app.route('/bill/<int:id>', methods=["GET"])
def get_bill(id):
    time_from = request.args["from"]
    time_to = request.args["to"]
    valid_time_from_format = validate_time_format(time_from)
    valid_time_to_format = validate_time_format(time_to)
    if not valid_time_from_format[0]:
        return f"from: {valid_time_from_format[1]}", 404
    if not valid_time_to_format[0]:
        return f"To:{valid_time_to_format[1]}", 404

    total_pay, truck_count, session_count, products, provider_name \
    = bill_helper.get_data(id, time_from, time_to)
    return bill_helper.get_json(id, time_from, time_to,
                            total_pay, truck_count,
                            session_count, products,
                            provider_name)

@app.route('/provider', methods=["POST"])
def post_provider():
    data = request.json
    result = model.create_provider(data["name"])
    if not result:
        return "The name already exist, Choose another one", 401
    return result, 200


@app.route('/provider/<int:id>', methods=["PUT"])
def put_provider(id):
    data = request.json
    result = model.update_provider(id, data["name"])
    if not result[0]:
        return result[1], 404
    return result[1], 200


@app.route('/rates', methods=['GET', 'POST'])
def rates_post():
    if request.method == 'POST':
        file = request.files.get('file')
        if not file or not file.filename:
            return '400: No file specified.\nMake sure you send the file under `file` key, e.g., `file: file-name`.'
        resp = model.post_rates_to_db(file)
        if resp == -1:
            return '500: Server Error'

        return f'200: OK\nNumber of records updated : {resp}'
        
    return send_file("../in/rates.xlsx", as_attachment=True)

    # return '''<!doctype html>
    # <title>Upload an excel file</title>
    # <h1>Excel file upload (csv, tsv, csvz, tsvz only)</h1>
    # <form action="" method=post enctype=multipart/form-data>
    # <p><input type=file name=file><input type=submit value=Upload>
    # </form>
    # '''


@app.route('/truck', methods=["POST"])
def register_truck():
    try:
        data = request.get_json()
        if model.register_truck(data):
            return "OK",200

    except Exception as e:
        print(f"Error: {e}")

    return "Invalid Request", 400


@app.route('/truck/<id>', methods=["PUT"])
def update_truck_provider(id):
    try:
        data = request.get_json()
        if model.update_truck_provider(data, id):
            return "OK",200

    except Exception as e:
        print(f"Error: {e}")

    return "Invalid Request", 400


@app.route('/truck/<id>/', methods=["GET"])
def get_truck(id):
    time_from = request.args["from"]
    time_to = request.args["to"]
    valid_time_from_format = validate_time_format(time_from)
    valid_time_to_format = validate_time_format(time_to)
    if not valid_time_from_format[0]:
        return f"from: {valid_time_from_format[1]}", 404
    if not valid_time_to_format[0]:
        return f"To:{valid_time_to_format[1]}", 404
    #if[os.environ['MOCK_TRUCK'] == "FALSE":
    #return requests.get(f"{os.environ['WEIGHT_URL']}/item/{id}?from={time_from}&to={time_to}")
    return "ok", 200


if __name__ == '__main__':
    do_debug = os.environ.get('DEBUG', False)
    weight_url = os.environ.get('WEIGHT_URL')
    model = ModelBuilder().build()
    bill_helper = BillHelper(weight_url ,model)

    app.run(host='0.0.0.0', debug=bool(do_debug))
