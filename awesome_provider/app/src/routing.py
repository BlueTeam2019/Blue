import os
from flask import Flask, request
import datetime

from model import Model
from query_helper import QueryHelper


app = Flask(__name__)


@app.route('/health', methods=["GET"])
def check_health():
    if model.check_health():
        return "OK", 200
    return "Internal Error", 500


@app.route('/provider', methods=["POST"])
def post_provider():
    data = request.json
    result = model.create_provider(data["name"])
    if not result:
        return "The name is exist ,Choose another one", 404
    return result, 200


@app.route('/provider/<int:id>', methods=["PUT"])
def put_provider(id):
    data = request.json
    result = model.update_provider(id, data["name"])
    if not result[0]:
        return result[1], 404
    return result[1], 200


@app.route('/truck/<int:id>/', methods=["GET"])
def GetTruck(id ):    
    timeFrom=request.args["from"]
    timeTo=request.args["to"]
    if timeFormat(timeFrom)[0]:
        if timeFormat(timeFrom)[0]:
            print("ok")        
    print(timeFrom)
    return "OK" ,200



def timeFormat(time):
    date_format = '%Y%m%d%H%M%S'
    try:
        date_obj = datetime.datetime.strptime(time, date_format)
        print(date_obj)
        return True  , "Succedded"
    except ValueError:
        return  False , "Incorrect data format, should be YYYYMMDDHHMMSS"



# @app.route('/put/<int:id>', methods=["PUT"])
# def Check(id):
#     return "put" ,200


# if __name__ == "__main__":
#     app.run(host="0.0.0.0", debug=True, port=8080)    
# 
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
        


