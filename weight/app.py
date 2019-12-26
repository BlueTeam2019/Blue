#!/usr/bin/env python3

import re   # regex, re.search
import os   # os.path.join
import csv
import json
import pymysql
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename

ACCESS_PORT = 5000
IN_DIR      = 'in/' # Path to Blue/weight/in folder (batch-weight)
UNIT_COL    = 1     # Column num in CSVs stating unit type(lbs/kg) for batch
WEIGHTUNITS = "(kg)|(lbs)"
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
        # else: # for debugging purposes, examine fetched data. unfinished.
        #     result = cur.fetchall()
        db.close() 
    return "HOME is where ♥Heart is❤❤❤", 200


@app.route("/batch-weight", methods=['POST'])
def batch_up():
    db = getMysqlConnection()
    cur = db.cursor()

    filename=request.form.get('file')
    if not filename:    #--if file was uploaded, then save it to /in
        f = request.files['file']
        if not f:
            return "NO FILE was POSTed"
        filename = secure_filename(f.filename)
        f.save(os.path.join(IN_DIR, filename))

    query = "REPLACE INTO containers_registered(container_id,weight,unit) VALUES (%s, %s, %s)" 
    suffix=filename.split('.')[-1].lower()
    if suffix=='csv':
        with open(os.path.join(IN_DIR, filename), 'r') as f:
            parsed_data = csv.DictReader(f)
            unit = parsed_data.fieldnames[UNIT_COL]
            if not re.search(unit, WEIGHTUNITS, re.IGNORECASE):
                return jsonify({'message':"Unit missing (kg,lbs)", 'status': 404})
            for row in parsed_data:
                cur.execute(query,[row['id'], row[unit], unit])
    elif suffix=='json':
        with open(os.path.join(IN_DIR, filename), 'r') as f:
            parsed_data = json.load(f)
            for row in parsed_data:
                cur.execute(query,[row['id'], row['weight'], row['unit']])  

    return "fine", 200


@app.route('/session/<id>', methods=['GET'])
def session(id):
    db = getMysqlConnection()
    getsession = "SELECT * from transactions where id={}".format(id)
    cur = db.cursor()
    cur.execute(getsession)
    output = cur.fetchone()
    db.close()
    if output==None:
        return jsonify({'message':'No session found', 'status':404})

    if output['direction']=="out":
        ret_json=jsonify({"id":output['id'],"truck":output['truck'],\
            "bruto":output['bruto'],"truckTara":output['truckTara'],"neto":output['neto']})
    else:
        ret_json=jsonify({"id":output['id'],"truck":output['truck'],"bruto":output['bruto']})

    return ret_json


app.run(host="0.0.0.0", port=ACCESS_PORT, debug=True)
