from flask import Flask, request

from bill_helper import BillHelper
from model_builder import ModelBuilder

app = Flask(__name__)


@app.route('/health', methods=["GET"])
def check_health():
    is_alive = model.check_health()
    if is_alive:
        return "OK", 200
    else:
        return "Internal Error", 500



@app.route('/bill/<int:id>', methods=["GET"])
def get_bill(id):
    from_t = request.args['from']
    to_t = request.args['to']
    total_pay, truck_count, session_count, products, provider_name \
        = bill_helper.get_data(id, from_t, to_t)
    return bill_helper.get_json(id, from_t, to_t,
                                total_pay, truck_count,
                                session_count, products,
                                provider_name)




if __name__ == '__main__':
    model = ModelBuilder().build()
    bill_helper = BillHelper(model)
    app.run(host='0.0.0.0', debug=True)
