#!/usr/bin/env python3
import os
import pymysql
import pandas as pd
from datetime import datetime
from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from werkzeug.utils import secure_filename

ACCESS_PORT = 5000
IN_DIR      = 'in/' # Path to Blue/weight/in folder (batch-weight)

MYSQL_DB	= 'weight'
MYSQL_USER  = 'root'
MYSQL_PW 	= 'pass'
MYSQL_HOST 	= 'mysql'
MYSQL_PORT	= '3306'

app = Flask(__name__)

def getMysqlConnection():
    return pymysql.connect(host=MYSQL_HOST,user=MYSQL_USER,passwd=MYSQL_PW,\
        db=MYSQL_DB,cursorclass=pymysql.cursors.DictCursor)


@app.route('/item/<string:id_num>', methods=['GET'])
def get_item_id(id_num):
    db = getMysqlConnection()
    cur = db.cursor()

    # from_t1 = request.args.get('from')
    # if not from_t1:
    #      from_t1 = datetime.now().strftime('%Y%m"+"01000000')
    # to_t2 = request.args.get('to')
    # if not to_t2:
    #     to_t2 = datetime.now().strftime('%Y%m%d%H%M%S')

    try:
        id_query = ("SELECT * FROM containers_registered WHERE container_id=" + "'" + id_num + "'")
        cur.execute(id_query)
        row = cur.fetchone()
        if row:
            json_data = {'id': id_num, 'tara': row['weight'] , 'sessions': [] }
            return jsonify(json_data)
        else:
            id_query = ("SELECT * FROM transactions WHERE truck = " + "'" + id_num + "';")
            cur.execute(id_query)
            data = cur.fetchall()
            if data:
                ret_id = []
                for line in data:
                    id, datetime, direction, truck, containers, bruto, truckTara, neto, produce = line
                    last_weight = line['truckTara']
                    ret_id.append(line['id'])
                if not last_weight:
                    last_weight = "N/A"
                json_data = {'id': id_num , 'tara': last_weight , 'sessions' : ret_id }
                return jsonify(json_data)
            else:
                return jsonify("no session found")
    except Exception as e:
        return jsonify("EXCEPTION it is", str(e))
    finally:
        db.close()

app.run(host="0.0.0.0", port=ACCESS_PORT, debug=True)