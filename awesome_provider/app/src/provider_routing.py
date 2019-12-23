from flask import Flask, request
import provider_model
import sys

app = Flask(__name__)
#model = None

@app.route('/health', methods=["GET"])
def CheckHealth():
    print("in route")
    isAlive = provider_model.provider_model.CheckHealth()
    if isAlive:
        return "OK", 200
    else:
        return "Internal Error", 500 

def sum_two_numbers(num1, num2):
    return num1 + num2
#if __name__ == '__main__':
#    dbUrl = sys.argv[1]
#    dbPass = sys.argv[2]
#    dbUser = sys.argv[3]
#    dbName = sys.argv[4]
#    dbPort = sys.argv[5]

    #model = provider_model(dbUrl, dbUser, dbPass, dbName, dbPort)
app.run(host='0.0.0.0')