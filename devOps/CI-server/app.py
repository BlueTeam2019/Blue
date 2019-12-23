import os
import subprocess

import yaml
from flask import Flask, request
from git import Repo

app = Flask(__name__)  # Standard Flask app

git_url = "git@github.com:BlueTeam2019/Blue.git"
repo_dir = "/home/ubuntu/testing/"
weight_path = "/weight/docker-compose_test.yml"
providor_path = "/awesome_provider/docker-compose.yml"
weight_path_prod = "/weight/docker-compose.yml"
providor_path_prod = "/awesome_provider/docker-compose.yml"


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
    repo = repo_dir + head_commit
    create_repo_of_commit(git_url, repo, head_commit)

    build(repo + weight_path, repo + providor_path)
    test_result = exec_tests()
    send_report(test_result)
    clear_test(head_commit)
    if branch_name == "maaaster":
        build(repo + weight_path_prod, repo + providor_path_prod)

    return "CI server webhooked".format(content)


def create_repo_of_commit(git_url, repo_dir, commit_hash):
    repo = Repo.clone_from(git_url, repo_dir)
    repo.git.checkout(commit_hash)


def exec_tests():
    return True


def send_report(report):
    return True


def clear_test(commit):
    return True


def build(weight_path, provider_path):
    subprocess.run("docker-compose -f {0} up --build -d".format(weight_path), shell=True)
    subprocess.run("docker-compose -f {0} up --build -d".format(provider_path), shell=True)


def edit_docker_compose_test(path):
    with open(path) as f:
        list_doc = yaml.load(f)

    for sense in list_doc:
        if sense["name"] == "sense2":
            sense["value"] = 1234

    with open("my_file.yaml", "w") as f:
        yaml.dump(list_doc, f)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
