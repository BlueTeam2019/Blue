from flask import Flask, request
import mysql.connector


app = Flask(__name__)

@app.route("/", methods=['GET'])
def hello():
    return " I AM BATMAN"


def checkalive():
    alive = True
    config = {
        'user': 'root',
        'password': 'pass',
        'host': 'mysql',
        'port': '3306',
        'database': 'weight',
        'raise_on_warnings': True
        }
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    print("HELLO from MODELS!")

    if cursor.execute(""" select * from containers_registered """):
        alive = False
    else:
        print("alive is: ", alive)
        for (id, weight, unit) in cursor:
            print(id, weight, unit)
    cursor.close()

    cnx.close()
    return alive


@app.route("/health", methods=['GET'])
def health():
    # print("HELLO from APP!")
    if checkalive():
        return "I AM BATMAN ", 200
    else:
        return "BAD", 500 

app.run(host="0.0.0.0",port=5000, debug=True)

