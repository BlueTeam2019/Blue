from flask import Flask, request
import provider_model
import sys

app = Flask(__name__)


@app.route('/health', methods=["GET"])
def CheckHealth(self):
    print("in route")
    isAlive = self.model.CheckHealth()
    if isAlive:
        return "OK", 200
    else:
        return "Internal Error", 500 

if __name__ == '__main__':
    dbUrl = sys.argv[1]
    dbPass = sys.argv[2]
    dbUser = sys.argv[3]
    dbName = sys.argv[4]
    dbPort = sys.argv[5]

    self.model = provider_model(dbUrl, dbUser, dbPass, dbName, dbPort)
app.run(host='0.0.0.0')