from flask import Flask, request

app = Flask(__name__)  # Standard Flask app


@app.route("/", )  # Standard Flask endpoint
def hello_world():
    return "CI server is listening..."


@app.route('/webhook', methods=['POST'])
def webhook():
    content = request.json
    print("Got push with: {0}".format(content))
    return "CI server webhooked".format(content)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
