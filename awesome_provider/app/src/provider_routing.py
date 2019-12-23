from flask import Flask
from provider_model import ProviderModel


app = Flask(__name__)


@app.route('/health', methods=["GET"])
def health():
    print("in route")
    if ProviderModel().check_health():
        return "OK", 200
    else:
        return "Internal Error", 500 


app.run(host='0.0.0.0')
