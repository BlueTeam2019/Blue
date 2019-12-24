import os
import subprocess
import yaml
from flask import Flask, request
from git import Repo
import shutil

# Standard Flask app
app = Flask(__name__)

# Configuration
git_url = "git@github.com:BlueTeam2019/Blue.git"
repo_dir = "/home/ubuntu/testing/"
weight_path = "/weight/docker-compose_test.yml"
providor_path = "/awesome_provider/docker-compose.yml"
weight_path_prod = "/weight/docker-compose.yml"
providor_path_prod = "/awesome_provider/docker-compose.yml"
master_history_path = "/home/ubuntu/master_hist"


# Standard Flask endpoint
@app.route("/", )
def hello_world():
    return "CI server is listening..."


# webhook to github
@app.route('/webhook', methods=['POST'])
def webhook():
    # parsing post request
    content = request.json
    pusher = content["pusher"]["name"]
    pusher_email = content["pusher"]["email"]
    head_commit = content["head_commit"]["id"]
    branch_name = os.path.basename(content["ref"])

    # creating a local repository for testing
    repo = repo_dir + head_commit
    create_repo_of_commit(git_url, repo, head_commit)

    # building testing build
    build(repo + weight_path, repo + providor_path)

    # testing build and sending reports
    test_result = exec_tests()
    send_report(test_result)

    if branch_name == "master":
        build(repo + weight_path_prod, repo + providor_path_prod)
        shutil.move(repo, master_history_path, copy_function=shutil.copytree)

    clear_test(head_commit)
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
    subprocess.run("docker-compose -f {0} build --no-cache".format(weight_path), shell=True)
    subprocess.run("docker-compose -f {0} up -d ".format(weight_path), shell=True)
    subprocess.run("docker-compose -f {0} build --no-cache".format(provider_path), shell=True)
    subprocess.run("docker-compose -f {0} up -d ".format(provider_path), shell=True)


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
