#!/usr/bin/env python3

import os
import mysql.connector
import pandas as pd
from flask import Flask, request
from sqlalchemy import create_engine
from werkzeug.utils import secure_filename

# APP_PORT    = 5000
IN_DIR      = 'in/' # Path to Blue/weight/in folder (batch-weight)

MYSQL_DB	= 'weight'
MYSQL_USER  = 'root'
MYSQL_PW 	= 'pass'
MYSQL_HOST 	= 'mysql'
MYSQL_PORT	= '3306'

app = Flask(__name__)


@app.route("/", methods=['GET'])
@app.route("/health", methods=['GET'])
def checkalive():
    alive = True
    config = {
        'user': MYSQL_USER,
        'password': MYSQL_PW,
        'host': MYSQL_HOST,
        'port': MYSQL_PORT,
        'database': MYSQL_DB,
        'raise_on_warnings': True
        }      # using mysql.connector
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    if cursor.execute(""" select * from containers_registered """):
        alive = False   #  FALSE if SQL not reached
    else:
        print("alive is: ", alive)
        for (id, weight, unit) in cursor:
            print(id, weight, unit)
    cursor.close()

    cnx.close()
    if alive:
        return "HOME is where ♥Heart is❤❤❤", 200
    else:
        return "This is UN-Healthy", 500


@app.route("/batch-weight", methods=['POST'])
def batch_up():
    # 1- receive file (to be parsed) or filename (to be looked in /in)
    filename=request.form.get('file')
    if not filename:    #--if file was uploaded, then save it to /in
        f = request.files['file']
        if not f:
            return "NO FILE was mentioned or uploaded"
        filename = secure_filename(f.filename)
        f.save(os.path.join(IN_DIR, filename))

    suffix=filename.split('.')[-1].lower()

    # 2- check if csv or json, to parse correctly
    if suffix=='csv':
        df = pd.read_csv(IN_DIR+filename)
    elif suffix=='json':
        df = pd.read_json(IN_DIR+filename)

    # 3- maintain a connection to MySQL DB
    engine = create_engine('mysql+mysqlconnector://'+MYSQL_USER+':'\
        +MYSQL_PW+'@'+MYSQL_HOST+':'+MYSQL_PORT+'/'+MYSQL_DB, echo=False)

    # 4- send query (INSERT), replacing current table values
    with engine.connect() as conn, conn.begin():
        df.to_sql('containers_registered', conn, if_exists='replace')
    return "fine"

app.run(host="0.0.0.0", port=5000, debug=True)
