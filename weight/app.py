#!/usr/bin/env python3

import os
import pymysql
import pymysql.cursors
from datetime import datetime
import pandas as pd
from flask import jsonify
from flask import Flask, request, render_template
from sqlalchemy import create_engine
from werkzeug.utils import secure_filename

ACCESS_PORT = 8082   # internal port: 5000
IN_DIR      = 'in/' # Path to Blue/weight/in folder (batch-weight)

MYSQL_DB	= 'weight'
MYSQL_USER  = 'root'
MYSQL_PW 	= 'pass'
MYSQL_HOST 	= 'localhost'
MYSQL_PORT	= '3306'

app = Flask(__name__)

def getMysqlConnection():
    return pymysql.connect(host=MYSQL_HOST,user=MYSQL_USER,passwd=MYSQL_PW,
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
    cur.fetchall
    db.close()
    if output==None:
        return jsonify({'message':'No session found', 'status':404})

    return_json=jsonify({"id":output['id'],"truck":output['truck'],"bruto":output['bruto']})
        #ONLY for OUT:
    if output['direction']=="out":
        return_json=jsonify({"id":output['id'],"truck":output['truck'],"bruto":output['bruto'],"truckTara":output['truckTara'],"neto":output['neto']})

    return return_json


def calculate_neto(bruto,trackTara,list_containers):
        sum_containers=0
        list_containers=list_containers.split(',')
        db = getMysqlConnection()
        cur = db.cursor()
        for item in list_containers:
            query = f'select * from containers_registered where container_id={item}'
            print(f"calcQuery:{query}")
            cur.execute(query)
            res=cur.fetchone()
            # cur.fetchall
            cur.close()
            if res == None:
                return None
            if res["weight"]==None:
                return None
            if res["unit"]=="lbs":
                sum_containers+= float(res["weight"])*float(0.453592)
            else:
                sum_containers+=float(res["weight"])
        return float(bruto)-float(trackTara)-float(sum_containers)

@app.route('/weight', methods=['POST'])
def post_weight():
    
    #connection to db
    db = getMysqlConnection()

    #set datatime to the current time
    datetimenow = datetime.now().strftime('%Y%m%d%H%M%S')
    #get data from form
    direction=request.form.get('direction', "none")
    containers=request.form.get('containers')
    truck=request.form.get('truck')
    currentWeight=request.form.get('currentWeight')
    unit=request.form.get('unit')
    if unit=="lbs":
        currentWeight=currentWeight*float(0.453592)
    produce=request.form.get('produce')
    force=request.form.get('force', False)
    

     
    #validation 
    if(direction=="in" or direction=="none") and (containers is None or produce is None):
        return "ERROR - no containers or produce"
    if(truck is None or currentWeight is None or unit is None):
        return "ERROR - missing parameters"
    
    #get last session id of truckID
    query="select max(id) as id from transactions where truck={} group by truck".format(truck)
    cur = db.cursor()
    cur.execute(query)
    lastSessionID=cur.fetchone()
    cur.fetchall()
    #get session of last session id
    if lastSessionID:
        
        query="select * from transactions where id={}".format(lastSessionID['id'])
        print(f"Query is:{query}")
        cur = db.cursor()
        cur.execute(query)
        last_session = cur.fetchone()
        print(query)
        # lastSession = cur
        #cur.close()
    else:
        last_session=None
    #direction is in (or none)
    #return "{}".format(lastSession)
    if direction=="in" or direction=="none":
        if last_session is None or last_session["direction"]=="out":
            query="insert into transactions (direction, datetime, truck, containers, bruto, produce) values ('{}','{}','{}','{}','{}','{}');".format(direction, datetimenow, truck, containers, currentWeight, produce)
            cur = db.cursor()
            cur.execute(query)
            print(query)
        elif last_session["direction"]=="in" or last_session["direction"]=="none":
            #check force
            if force:
                query="update transactions set direction='{}', datetime='{}', truck='{}', containers='{}', bruto{}, produce='{}' where id={};".format(direction, datetimenow, truck, containers, currentWeight, produce, lastSessionID)
                #cur = db.cursor()
                cur.execute(query)
                #cur.close()
                print(query)
            else:
                return "ERROR - in after in"
    elif direction=="out":
        if last_session is None:
            return "ERROR - out when there is no session"
        neto=calculate_neto(last_session["bruto"], currentWeight, last_session["containers"])
        if last_session["direction"]=="out":
            if force:
                query="update transactions set datetime={}, truckTara={}, neto={}, produce={} where id={}".format(datetimenow, currentWeight, neto, produce, lastSessionID['id'])
                #cur = db.cursor()
                print(query)
                try:
                    cur.execute(query)
                except Exception:
                    print(Exception)
                #cur.close()
                print(query)
            else:
                return "ERROR - out after out"
        else:
            if produce is None:
                produce=last_session["produce"]
            query=f"insert into transactions(direction, datetime, truck, containers, bruto, truckTara, neto, produce) values ('{direction}','{datetimenow}','{last_session['truck']}','{last_session['containers']}','{last_session['bruto']}','{currentWeight}','{neto}','{produce}');"
            #cur = db.cursor()
            print(query)
            cur.execute(query)
            #cur.close()
    
    getsession = "SELECT JSON_ARRAYAGG(JSON_OBJECT('id', id, 'created', created_at, 'truckid', truckid, 'Bruto', bruto, 'truckTara', truckTara, 'Neto', neto)) from sessions where id='%s'" %id
    current_session_query = "select max(id) as id from transactions where truck={} group by truck".format(truck)
    cur = db.cursor()
    cur.execute(current_session_query)
    tmp = cur.fetchone()
    current_session_id = tmp['id']
    cur.fetchall()
    output = None
    try:
        getsession = "SELECT * from transactions where id={}".format(current_session_id)
        print(getsession)
        cur.execute(getsession)
        output = cur.fetchone()
        cur.fetchall()
    except Exception:
        print(Exception)
    if output==None:
        return jsonify({'message':'No session found', 'status':404})
    return_json=jsonify({"id":output['id'],"truck":output['truck'],"bruto":output['bruto']})
    if output['direction']=="out":
        return_json=jsonify({"id":output['id'],"truck":output['truck'],"bruto":output['bruto'],"truckTara":output['truckTara'],"neto":output['neto']})
    db.close()
    return return_json
        
                      



    









app.run(host="0.0.0.0", port=ACCESS_PORT, debug=True)
