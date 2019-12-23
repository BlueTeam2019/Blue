#!/usr/bin/env python3

# import csv
# import os
# import io
# import models   # importing the methods from models.py
import mysql.connector
from flask import Flask, request
import pandas as pd
from sqlalchemy import create_engine

MYSQL_USER  = 'root'
MYSQL_PW 	= 'pass'
MYSQL_HOST 	= '0.0.0.0'
MYSQL_PORT	= '8877'
MYSQL_DB	= 'weight'
#@@@@@@@@ DON'T FORGET TO CHANGE THIS PATH @@@@@@@@@@#
IN_DIR      = '/home/develeap/training/devweek/Blue/weight/in/'

app = Flask(__name__)


@app.route("/", methods=['GET'])
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
    # if mysql.connector.errors.DatabaseError:      # ASSERT
        # return mysql.connector.errors.DatabaseError
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
    # 2- check if csv or json, to parse correctly
    filename=request.files['file'].filename
    if not filename:
        return "No file"
    df = pd.read_csv(IN_DIR+filename)

    # 3- maintain a connection to MySQL DB
    # engine = create_engine('mysql+mysqlconnector://root:pass@localhost:8877/weight')
    engine = create_engine('mysql+mysqlconnector://'+MYSQL_USER+':'\
        +MYSQL_PW+'@'+MYSQL_HOST+':'+MYSQL_PORT+'/'+MYSQL_DB, echo=False)
    # 4- send query (INSERT), replacing current table values
    with engine.connect() as conn, conn.begin():
        df.to_sql('containers_registered', conn, if_exists='replace')
    return "fine"

# @app.route("/csv", methods=['POST'])
# def handleCSV():
# # Read file from POST ('file' is a header key)
#     f = request.files['file']
#     if not f:
#         return "No file"
# # Read file as CSV
#     csv_input = pd.read_csv(f)

#     # print("*************csv_input:*************")
#     # print(csv_input.to_dict())
#     # for key in csv_input.to_dict():
#     """ for key in csv_input:
#         # print ("key: '%s',\n value:\n%s" % (key, csv_input[key]))
#         for secondaryKey in csv_input[key]:            
#             print("2ndary is %s" % secondaryKey) """

#     config = {
#         'user': 'root',
#         'password': 'pass',
#         'host': '0.0.0.0',
#         'port': '8877',
#         'database': 'weight',
#         'raise_on_warnings': True
#         }
#     cnx = mysql.connector.connect(**config)
#     # print("************* mysql.connector.connect(**config) *************")
#     # if mysql.connector.errors.DatabaseError:      # ASSERT
#         # print("ERROR DATABASE CONNECTOR")
#         # return mysql.connector.errors.DatabaseError
#     cursor = cnx.cursor()
#     print("************* cnx.cursor() *************")

#     # if not cursor.execute(""" select * from containers_registered """):
#     #     for (id, weight, unit) in cursor:
#     #         print(id, weight, unit)
#     #     csv_input.to_sql(name="containers_registered", con=cnx, index=True, index_label="id")
#     csv_input.to_sql(name="containers_registered", con=cnx, index=True, index_label="id")


#     cursor.close()
#     cnx.close()
            
#     return "OK", 200
            
            



# @app.route("/batch-weight", methods=['POST'])
# def handleFileUpload():    
#     models.batch_up(request.data)

    # msg = 'failed to upload image'
    # # print(request.get_data['image'])
    # if 'image' in request.files:

    #     photo = request.files['image']
    #     # print(photo)

    #     if photo.filename != '':

    #         photo.save(os.path.join('.', photo.filename))
    #         msg = 'image uploaded successfully'
    #     # print(photo)
    # return msg

# if __name__ == '__main__':
    # app.run()
app.run(host="0.0.0.0",port=8082, debug=True)
