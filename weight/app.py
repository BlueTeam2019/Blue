#!/usr/bin/env python3

import os
import pymysql
import pandas as pd
from flask import jsonify
from flask import Flask, request
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

@app.route("/", methods=['GET'])
@app.route("/health", methods=['GET'])
def checkalive():
    try:
        db = getMysqlConnection()
    except Exception:
        return "Error in MySQL connexion", 500
    else:
        cur = db.cursor()
        try:
            query=""" select * from containers_registered; """
            cur.execute(query)
        except Exception:
            return "Error with query: " + query, 500
        else:
            db.commit()
            result = cur.fetchall()
            print(result)
        db.close() 
    return "HOME is where ♥Heart is❤❤❤", 200


@app.route("/batch-weight", methods=['POST'])
def batch_up():
    # 1- receive file (to be parsed) or filename (to be looked in /in)
    filename=request.form.get('file')
    if not filename:    #--if file was uploaded, then save it to /in
        f = request.files['file']
        if not f:
            return "NO FILE was POSTed"
        filename = secure_filename(f.filename)
        f.save(os.path.join(IN_DIR, filename))
    # 2- check if csv or json, to parse correctly
    suffix=filename.split('.')[-1].lower()
    if suffix=='csv':
        df = pd.read_csv(IN_DIR+filename)
    elif suffix=='json':
        df = pd.read_json(IN_DIR+filename)
    # 3- maintain a connection to MySQL DB
    engine = create_engine('mysql+pymysql://'+MYSQL_USER+':'\
        +MYSQL_PW+'@'+MYSQL_HOST+':'+MYSQL_PORT+'/'+MYSQL_DB, echo=False)
    # 4- send query (INSERT), replacing current table values
    with engine.connect() as conn, conn.begin():
        df.to_sql('containers_registered', conn, if_exists='replace')
    return "fine"


@app.route('/session/<id>', methods=['GET'])
def session(id):
    db = getMysqlConnection() # CHANGE
    
                #   origional
                #       getsession = "SELECT JSON_ARRAYAGG(JSON_OBJECT('id', id, 'created', created_at, 'truckid', truckid, 'Bruto', bruto, 'truckTara', truckTara, 'Neto', neto)) from sessions where id='%s'" %id
    getsession = "SELECT * from transactions where id={}".format(id)

        #return id',truckid', 'Bruto')
        #IF OUT  (truckTara, neto)  

    cur = db.cursor()
    cur.execute(getsession)
    output = cur.fetchone()
    db.close()
    if output==None:
        return jsonify({'message':'No session found', 'status':404})

    return_json=jsonify({"id":output['id'],"truck":output['truck'],"bruto":output['bruto']})
        #ONLY for OUT:
    if output['direction']=="out":
        return_json=jsonify({"id":output['id'],"truck":output['truck'],"bruto":output['bruto'],"truckTara":output['truckTara'],"neto":output['neto']})

    return return_json



app.run(host="0.0.0.0", port=ACCESS_PORT, debug=True)
