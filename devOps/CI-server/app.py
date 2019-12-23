from flask import Flask, request
from git import Repo
import json

app = Flask(__name__)  # Standard Flask app

git_url = "git@github.com:BlueTeam2019/Blue.git"
repo_dir = "/home/ubuntu/testing"


@app.route("/", )  # Standard Flask endpoint
def hello_world():
    return "CI server is listening..."


@app.route('/webhook', methods=['POST'])
def webhook():
    content = request.json
    print("Got push with: {0}".format(json.dumps(content, indent=2)))
    create_new_repo(git_url, repo_dir)
    return "CI server webhooked".format(content)


def create_new_repo(git_url, repo_dir):
    Repo.clone_from(git_url, repo_dir)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
