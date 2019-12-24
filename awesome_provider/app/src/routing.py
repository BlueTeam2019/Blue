<<<<<<< HEAD
from flask import Flask, request
from provider_model import provider_model
import sys
import datetime

app = Flask(__name__)
#model = None

@app.route('/health', methods=["GET"])
def CheckHealth():
    print("in route")
    isAlive = provider_model.CheckHealth()
    if isAlive:
        return "OK", 200
    else:
        return "Internal Error", 500

@app.route('/provider', methods=["POST"])
def PostProvider():
    data= request.json
    result=provider_model.createProvider(data["name"])
    if result == 1 :
        return "The name is exist ,Choose another one", 404
    return result


@app.route('/provider/<int:id>', methods=["PUT"])
def PutProvider(id):
    #print("YOHO")
    data= request.json
    print(data["name"])
    print(id)
    result=provider_model.updateProvider(id,data["name"])
    # if result == 1 :
    #         return "Wrong id", 404
    # return "put ok" ,200
    return result


@app.route('/truck/<int:id>/', methods=["GET"])
def GetTruck(id ):    
    timeFrom=request.args["from"]
    timeTo=request.args["to"]
    if timeFormat(timeFrom):
        if timeFormat(timeFrom):
            print("ok")        
    print(timeFrom)
    return "OK" ,200



def timeFormat(time):
    date_format = '%Y%m%d%H%M%S'
    try:
        date_obj = datetime.datetime.strptime(time, date_format)
        print(date_obj)
        result=1
    except ValueError:
        print("Incorrect data format, should be YYYYMMDDHHMMSS")
        result=0
    return result    

# @app.route('/put/<int:id>', methods=["PUT"])
# def Check(id):
#     return "put" ,200


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8080)          
=======
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
>>>>>>> ccadbb36047d4ae5581542c5b701ccd6b0bd8684
