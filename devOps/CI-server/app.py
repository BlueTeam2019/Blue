from flask import Flask

app = Flask(__name__)  # Standard Flask app


@app.route("/", )  # Standard Flask endpoint
def hello_world():
    return "CI server is listening..."


@app.route('/webhook', methods=['POST'])
def webhook(data):
    print("Got push with: {0}".format(data))
    return "CI server webhooked"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
