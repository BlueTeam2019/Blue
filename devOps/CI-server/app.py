import os
from flask import Flask, request
from git import Repo
import json

app = Flask(__name__)  # Standard Flask app

git_url = "git@github.com:BlueTeam2019/Blue.git"
repo_dir = "/home/ubuntu/testing/"


@app.route("/", )  # Standard Flask endpoint
def hello_world():
    return "CI server is listening..."


@app.route('/webhook', methods=['POST'])
def webhook():
    content = request.json
    pusher = content["pusher"]["name"]
    pusher_email = content["pusher"]["email"]
    head_commit = content["head_commit"]["id"]
    branch_name = os.path.basename(content["ref"])

    print("Got push with: {0},{1},{2},{3}".format(pusher, pusher_email, head_commit, branch_name))
    create_repo_of_commit(git_url, repo_dir + head_commit, head_commit)
    return "CI server webhooked".format(content)


def create_repo_of_commit(git_url, repo_dir, commit_hash):
    repo = Repo.clone_from(git_url, repo_dir)
    repo.git.checkout(commit_hash)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

#create_repo_of_commit(git_url, "/home/itamar/ubuntu/testing", "50f09c64ffb57614a1526bba3a6382148670c020")
